from re import S
from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import get_random_id
import uuid
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
from student_management_app.models import CustomUser,Student
from django.contrib.auth.models import Group




gender_choice = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others'),
)
profile_status_choice = (
    ('pending', 'pending'),
    ('approved', 'approved'),
    ('rejected', 'rejected'),
)
user_type_choice = (
    ('Student', 'Student'),
    ('Staff', 'Staff'),
    ('Public User', 'Public User'),
)


class LibraryMemberProfile(models.Model):
    member=models.ForeignKey(Student, on_delete=models.CASCADE, related_name='library_member_details', null=True, blank=True)
    status = models.CharField(max_length=30, choices=profile_status_choice, default='pending')
    library_card_no = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# @receiver(post_save, sender=LibraryMemberProfile)
# def postsave_data(sender, instance, created, *args, **kwargs):
#     if created:
#         if instance.user_type == 'Staff':
#             try:
#                 max_num = 4
#                 instance.borrowed_books = max_num + instance.borrowed_books
#                 instance.save()
#             except Exception as e:
#                 print("error occured:::: ", e)

#         elif instance.user_type == 'Student':
#             try:
#                 max_num = 5
#                 instance.borrowed_books = max_num + instance.borrowed_books
#                 instance.borrowed_books.save()
#             except Exception as e:
#                 print("error occured:::: ", e)

#         elif instance.user_type == 'Public User':
#             try:
#                 max_num = 2
#                 instance.borrowed_books = max_num + instance.borrowed_books
#                 instance.save()
#             except Exception as e:
#                 print("error occured:::: ", e)

#         else:
#             print("Given Instances does not match")

class Issue(models.Model):
    member=models.ForeignKey(LibraryMemberProfile, on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.member)

    @property
    def total_qty(self):
        order_items = BookIssue.objects.filter(issue_id=self.id)
        total_qty = 0
        for order_item in order_items:
            total_qty = (order_item.quantity + total_qty)
        return total_qty


    def get_absolute_url(self):
        return reverse('book_issue_detail', kwargs={'pk': self.pk})

class Return(models.Model):
    member=models.ForeignKey(LibraryMemberProfile, on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.member)

class Category(models.Model):
    name = models.CharField(max_length=50, help_text="For example: science, History, Technical, Enclyclopedia, etc.", null=True)
    created_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    

class BookEntry(models.Model):
    class Meta:
        verbose_name_plural = 'Book Entry'
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    summary = models.TextField(max_length=1000)
    isbn = models.IntegerField(primary_key=True)
    # genre = models.TextField(max_length=20, help_text="For example: science, History, Technical, Enclyclopedia, etc.", null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    language = models.TextField(max_length=20)
    quantity = models.IntegerField()
    price = models.FloatField(null=True, blank=True)
    # pic = models.ImageField(blank=True, null=True, upload_to='book_image')
    # published_year = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @staticmethod
    def get_all_books():
        return BookEntry.objects.all()

    @staticmethod
    def get_all_books_by_id(category_id):
        if category_id:
            return BookEntry.objects.filter(category=category_id)
        # else:
        #     return BookEntry.get

def get_expiry():
    return datetime.today() + timedelta(days=1)

class BookIssue(models.Model):
    class Meta:
        verbose_name_plural = 'Book Issue'
    issue_id = models.ForeignKey(Issue, on_delete=models.CASCADE)
    title = models.ForeignKey(BookEntry, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=200)
    quantity = models.IntegerField()
    # member_name = models.CharField(max_length=200)
    # member_id = models.ForeignKey(LibraryMemberProfile, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(auto_now_add=True)
    expirydate = models.DateField(default=get_expiry)
    
    def __str__(self):
        return str(self.title) + "[" + str(self.isbn) + ']'



class BookReturn(models.Model):
    issue_id = models.ForeignKey(Issue, on_delete=models.CASCADE,null=True)
    title = models.ForeignKey(BookEntry, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=200)
    quantity = models.IntegerField()
    return_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)

class BookRenew(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.ForeignKey(BookIssue, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    member_name = models.CharField(max_length=200)
    member_id = models.ForeignKey(LibraryMemberProfile, on_delete=models.CASCADE)
    renew_date = models.DateTimeField(auto_now_add=True)
    expirydate = models.DateField(default=get_expiry)

    def __str__(self):
        return str(self.title) + "[" + str(self.isbn) + ']'




class Barcode(models.Model):
    name = models.CharField(max_length=100)
    barcode = models.ImageField(upload_to = 'barcode_images/', blank = True)
    country_id = models.CharField(max_length=2)
    manufacturer_id = models.CharField(max_length=6)
    product_id = models.CharField(max_length=5)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        ISBN = barcode.get_barcode_class('isbn13')
        isbn = ISBN(f'{self.country_id}{self.manufacturer_id}{self.product_id}', writer=ImageWriter())
        buffer = BytesIO()
        isbn.write(buffer)
        self.barcode.save(f'{self.name}.png', File(buffer), save=False)
        return super().save(*args, **kwargs)
    

