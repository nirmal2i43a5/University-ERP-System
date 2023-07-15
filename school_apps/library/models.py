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
    member=models.ForeignKey(Student, on_delete=models.CASCADE, related_name='library_member_details')
    status = models.CharField(max_length=30, choices=profile_status_choice, default='pending',blank=True, null=True)
    library_card_no = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.member} - Card No : {self.library_card_no}'


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
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True, blank=True)
    isbn = models.IntegerField(primary_key=True)
    quantity = models.IntegerField(null=True, blank=True)

    author = models.CharField(max_length=100,null=True, blank=True)
    summary = models.TextField(max_length=1000,null=True, blank=True)
    # genre = models.TextField(max_length=20, help_text="For example: science, History, Technical, Enclyclopedia, etc.", null=True)
    language = models.TextField(max_length=20,blank=True, null=True)
    price = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}(ISBN: {self.isbn})'

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
    issue_member = models.ForeignKey(LibraryMemberProfile, on_delete=models.CASCADE)
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
    book_issue = models.ForeignKey(BookIssue, on_delete=models.CASCADE,related_name='bookreturns')

    # title = models.ForeignKey(BookEntry, on_delete=models.CASCADE)
    # isbn = models.CharField(max_length=200)
    quantity = models.IntegerField()
    is_returned = models.BooleanField(default=False)
    return_date = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return str(self.title)

class BookRenew(models.Model):
    book_issue = models.ForeignKey(BookIssue, on_delete=models.CASCADE,related_name='bookrenew')
    member_id = models.ForeignKey(LibraryMemberProfile, on_delete=models.CASCADE)
    renew_date = models.DateTimeField(auto_now_add=True)
    expirydate = models.DateField(default=get_expiry)
    is_renewed = models.BooleanField(default=False)

    # def __str__(self):
    #     return str(self.title) + "[" + str(self.isbn) + ']'


class Fine(models.Model):
    member = models.ForeignKey(LibraryMemberProfile, on_delete=models.CASCADE,blank=True, null=True)
    book = models.ForeignKey(BookEntry, on_delete=models.CASCADE,blank=True, null=True)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    # fine_date = models.DateField()
    payment_date =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Fine for {self.member} - Book: {self.book}"

'''
id 
memebr id 
book id
fine amount 
fine status(paid or)
fine date  = The date when the fine was incurred.
payment date = The date when the fine was paid (if applicable).

'''

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
    

