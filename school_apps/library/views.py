from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db import transaction
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.forms import widgets
from django.forms import inlineformset_factory
from datetime import datetime
from student_management_app.models import Semester
from .models import *
from .forms import *
from django.contrib.auth.models import User
from school_apps.library.models import LibraryMemberProfile



def category_list(request):
    category_list = Category.objects.all()
    return render(request, 'catalog/book_category/category_list.html', {'category_list': category_list})


def CategoryAddView(request):
  
    form = CategoryAddForm()
    if request.method == 'POST':
        form = CategoryAddForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('library:category_list')
    context = {
        'form': form
    }
    return render(request, 'catalog/book_category/category_add.html', context=context)


def CategoryFullView(request, pk):
  
    category_instance = Category.objects.get(id=pk)
    form = CategoryAddForm(instance= category_instance)
    context = {
        'form':form
    }
    return render(request, 'catalog/book_category/category_detail.html', context=context)

def CategoryUpdateView(request, pk):
  
    category_instance = Category.objects.get(id=pk)
    form = CategoryAddForm(instance=category_instance)
    if request.method == 'POST':
        form = CategoryAddForm(data=request.POST, files=request.FILES, instance=category_instance)
        if form.is_valid():
            form.save()
            return redirect('library:category_list')
    context = {
        'form' : form 
    }
    return render(request, 'catalog/book_category/category_update.html', context=context)

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'catalog/confirm_delete.html'
    success_url = reverse_lazy('category_list')


def book_list(request):
    book_list = BookEntry.objects.all().order_by('-isbn')
    category_list = Category.objects.all()
    context = {
        'category_list':category_list,
        'book_list': book_list
    }
    return render(request, 'catalog/book_info/book_list.html', context)
    

def add_book(request):
  
    form = BookAddForm()
    if request.method == 'POST':
        form = BookForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('library:book_list')
    context = {
        'form':form
    }
    return render(request, 'catalog/book_info/add_book.html', context=context)


def edit_book(request, pk):
  
    book_instance = BookEntry.objects.get(isbn=pk)
    form = BookAddForm(instance= book_instance)
    if request.method == 'POST':
        form = BookForm(data=request.POST, files=request.FILES, instance=book_instance)
        if form.is_valid():
            form.save()
            return redirect('library:book_list')
    context = {
        'form':form
    }
    return render(request, 'catalog/book_info/book_edit.html', context=context)



def book_list(request):
    book_list = BookEntry.objects.all()
    return render(request, 'catalog/book_info/book_list.html', {'book_list':book_list})



def view_book(request, pk):
  
    book_instance = BookEntry.objects.get(isbn=pk)
    form = BookAddForm(instance= book_instance)
    context = {
        'form':form
    }
    return render(request, 'catalog/book_info/book_detail.html', context=context)



class BookDeleteView(DeleteView):
    model = BookEntry
    template_name = 'catalog/confirm_delete.html'
    success_url = reverse_lazy('library:book_list')



def member_list(request):
    memberlist = LibraryMemberProfile.objects.all()

    return render(request, 'catalog/member_list.html', {'memberlist': memberlist})



def add_member(request):
    form = AddMemberForm()
    if request.method == 'POST':
        form = AddMemberForm(request.POST, request.FILES)
        member_id = request.POST['member']
        student_instance = Student.objects.get(pk=member_id)
        library_number = f'{student_instance.stu_id}-{student_instance.join_year}' 
        if form.is_valid():   
            instance = form.save(commit = False)
            instance.library_card_no = library_number
            instance.save()
            
            return redirect('library:member_list')
    context = {
        'form':form,
        'classes':Semester.objects.all()
    }
    return render(request, 'catalog/add_member.html', context=context)



def edit_member(request, pk):
   
    member_instance = LibraryMemberProfile.objects.get(id=pk)
    form = AddMemberForm(instance=member_instance)
    if request.method == 'POST':
        form = AddMemberForm(request.POST, request.FILES, instance=member_instance)
        if form.is_valid():   
            form.save()
            return redirect('library:member_list')
    context = {
        'form':form,
        'member_instance':member_instance
    }
    return render(request, 'catalog/add_member.html', context=context)



def member_detail(request, pk):
  
    member_instance = LibraryMemberProfile.objects.get(id=pk)
    form = MemberDetailForm(instance= member_instance)
    context = {
        'form':form
    }
    return render(request, 'catalog/member_detail.html', context=context)  



class MemberDeleteView(DeleteView):
    model = LibraryMemberProfile
    template_name = 'catalog/confirm_delete.html'
    success_url = reverse_lazy('member_list')


# ----------------------------- Book issue CRUD views ------------------------------------------
def book_issue_list(request):
    book_issue = BookIssue.objects.all()

    return render(request, 'catalog/book_issued_list.html', {'book_issue': book_issue,
                                                             })



# class BookIssueCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
#     model = Issue
#     template_name = "catalog/issue_info/book_issue_form.html"
#     fields = '__all__'
#     success_message = "Book Issued added successfully."

#     def get_success_message(self, cleaned_data):
#         print(cleaned_data)
#         print('Book added successfully!')
#         return "Book Issued Successfully! "

#     def get_context_data(self, **kwargs):
#         data = super(BookIssueCreateView, self).get_context_data(**kwargs)
#         if self.request.POST:
#             data['items'] = BookIssueFormset(self.request.POST)
#         else:
#             data['items'] = BookIssueFormset()
#         return data

#     def form_valid(self, form):
#         context = self.get_context_data()
#         items = context['items']
#         with transaction.atomic():
#             if items.is_valid():
#                 items.instance = form.save(commit=False)
#                 for i in items:
#                     title=i.cleaned_data['bookissue_set-0-title']
#                     qt=i.cleaned_data['quantity']
#                     book_quantity = BookEntry.objects.get(title=title)
#                     if book_quantity.quantity < qt:
#                         form.errors['value']='Your entered quantity exceeds book quantity'
#                         return self.form_invalid(form)
#                     else:
#                         book_quantity.quantity -=qt
#                         book_quantity.save()
#                         form.save()
#                         items.save()
#                 # sold_item.save()
#         return super(BookIssueCreateView, self).form_valid(form)

#     def get_initial(self):
#         initial=super(BookIssueCreateView,self).get_initial()
#         initial['member']=LibraryMemberProfile.objects.get(pk=self.kwargs['pk'])
#         return initial


# def issue_member_list(request):
#     member_ids = BookIssue.objects.values_list('issue_member', flat=True).distinct()

#     members = LibraryMemberProfile.objects.filter(id__in=member_ids)
#     context = {
#     'members':members
#     }

#     return render(request, 'catalog/issue_member_list.html', context=context)

def renew_issue(request):
    member_ids = BookIssue.objects.values_list('issue_member', flat=True).distinct()

    members = LibraryMemberProfile.objects.filter(id__in=member_ids)
    context = {
    'members':members
    }

    return render(request, 'catalog/renew_issue.html', context=context)

def return_issue(request):
    member_ids = BookIssue.objects.values_list('issue_member', flat=True).distinct()

    members = LibraryMemberProfile.objects.filter(id__in=member_ids)
    context = {
    'members':members
    }

    return render(request, 'catalog/return_issue.html', context=context)
    
def issue_list_for_return(request,pk):
    member = LibraryMemberProfile.objects.get(pk = pk)
    book_issue = member.bookissue_set.all()
    # for book_issue in book_issue:
    #     book_issue_instance = BookIssue.objects.get(pk = book_issue.pk)
    #     return_status = book_issue_instance.bookreturn_set.values_list('is_returned', flat=True)
    

    context = {
    'book_issue':book_issue,
    'member':member
    }
    return render(request, 'catalog/issue_list_for_return.html', context=context)


def book_issue(request):
  
    form = BookIssueForm()
    if request.method == 'POST':
        form = BookIssueForm(request.POST, request.FILES)
        if form.is_valid():
            # member_id = form.cleaned_data['member']
            book_instance=form.cleaned_data['title']
            quantity=form.cleaned_data['quantity']
            book_quantity = BookEntry.objects.get(isbn=book_instance.isbn)
            if book_quantity.quantity < quantity:
                messages.error(request, f'Your entered quantity exceeds book quantity.There is only {book_quantity.quantity} books left')

                return redirect('library:book_issue')

            else:
                book_quantity.quantity -= quantity
                book_quantity.save()
                form.save()
                messages.success(request, 'Book issued successfully')
            return redirect('library:book_issue_list')
    context = {
        'form':form,
         'classes':Semester.objects.all()

    }
    return render(request, 'catalog/book_issue.html', context=context)


def book_issue_edit(request, issue_id):
    book_instance = BookIssue.objects.get(id=issue_id)
   
    if request.method == 'POST':
        form = BookIssueEditForm(request.POST,instance=book_instance)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            book_instance=form.cleaned_data['title']
            book_quantity = BookEntry.objects.get(isbn=book_instance.isbn)
            if book_quantity.quantity < quantity:
                messages.error(request, f'Your entered quantity exceeds book quantity.There is only {book_quantity.quantity} books left')
                return redirect('library:book_issue_edit',issue_id=issue_id)

            else:
                book_quantity.quantity -= quantity
                book_quantity.save()
                form.save()
                messages.success(request, 'Book issued Updated successfully')

            return redirect('library:book_issue_list')
    else:
        form = BookIssueEditForm(instance=book_instance)
        # formset = ItemFormset(instance=book_instance)

    return render(request, 'catalog/book_issue_edit.html', {'form': form, 
                                                            # 'formset': formset
                                                            }
                                                            )



class book_issue_detail(LoginRequiredMixin,DetailView):
    model = Issue
    template_name = 'catalog/book_issue_detail.html'

    def get_context_data(self, **kwargs):
        context = super(book_issue_detail, self).get_context_data(**kwargs)
        return context



class BookIssueDeleteView(DeleteView):
    model = BookIssue
    template_name = 'catalog/confirm_delete.html'
    success_url = reverse_lazy('library:book_issue_list')


# ----------------------------- Book return CRUD views ------------------------------------------
def book_return_list(request):
    book_return = BookReturn.objects.all()
    return render(request, 'catalog/book_return_list.html', {'book_return': book_return})




def book_return(request,pk):
   

    if request.method == 'POST':

        quantity = request.POST.get('quantity')
        bookissue_id = request.POST.get('bookissue_id')
        isbn = request.POST.get('book_id')

        book_issue_instance = BookIssue.objects.get(pk=bookissue_id)
        book_quantity = BookEntry.objects.get(pk=isbn)

        if book_quantity.quantity < int(quantity):
            messages.error(request, f'Your entered quantity exceeds book quantity.There is only {book_quantity.quantity} books left')
            return redirect('library:issue_list_for_return',pk)
        else:
            book_quantity.quantity += int(quantity)
            book_issue_instance.quantity -= int(quantity)
            book_quantity.save()
            book_issue_instance.save()
            book_return = BookReturn.objects.create(book_issue = book_issue_instance, quantity = quantity,is_returned = True)
            book_return.save()
            messages.success(request, 'Book returned successfully')

        return redirect('library:issue_list_for_return',pk)
   
    return render(request, 'catalog/issue_list_for_return.html')





def book_return_edit(request, pk):
  
    book_instance = BookReturn.objects.get(id=pk)
    form = BookReturnForm(instance=book_instance)
    if request.method == 'POST':
        form = BookReturnForm(data=request.POST, files=request.FILES, instance=book_instance)
        if form.is_valid():
            form.save()
            return redirect('library:book_return_list')
    context = {
        'form':form
    }
    return render(request, 'catalog/book_return_edit.html', context=context)



def book_return_detail(request, pk):
  
    book_instance = BookReturn.objects.get(id=pk)
    form = BookReturnForm(instance= book_instance)
    context = {
        'form':form
    }
    return render(request, 'catalog/book_return_detail.html', context=context)  



class BookReturnDeleteView(DeleteView):
    model = BookReturn
    template_name = 'catalog/confirm_delete.html'
    success_url = reverse_lazy('library:book_return_list')


# ----------------------------- Book renew CRUD views ------------------------------------------
def book_renew_list(request):
    book_renew = BookRenew.objects.all()
    return render(request, 'catalog/book_renew_list.html', {'book_renew':book_renew})


from django.db.models import Prefetch, Subquery
def issue_list_for_renew(request,pk):
    member = LibraryMemberProfile.objects.get(pk = pk)
    all_book_issues = member.bookissue_set.all()
    prefetch = Prefetch(
    'bookrenew',
    queryset=BookRenew.objects.order_by('-expirydate').only('expirydate', 'is_renewed'),
    to_attr='latest_renewal'
)

# Apply the prefetch to BookIssue queryset
    book_issues = all_book_issues.prefetch_related(prefetch)

    # Access latest expiry date and is_renewed status for each BookIssue
    book_renew_details = []
    for book_issue in book_issues:
        latest_renewal = book_issue.latest_renewal[0] if book_issue.latest_renewal else None
        print(latest_renewal)
        expiry_date = latest_renewal.expirydate if latest_renewal else None
        is_renewed = latest_renewal.is_renewed if latest_renewal else None
    
            # print(days_late_to_renew,"********************88")
        book_renew_details.append({"expiry_date": expiry_date, "is_renewed": is_renewed,
                                #    'days_late_to_renew':days_late_to_renew
                                   })
    print(book_renew_details)
    
    context = {
        'book_issue': zip(all_book_issues,book_renew_details),
    # 'book_issue':book_issues,
    'member':member
    }
    return render(request, 'catalog/add_book_renew.html', context=context)
    

  
def book_renew(request,pk):

    if request.method == 'POST':

        bookissue_id = request.POST.get('bookissue_id')
        member_instance = LibraryMemberProfile.objects.get(pk = pk)
        book_issue_instance = BookIssue.objects.get(pk=bookissue_id)
        book_renew = BookRenew.objects.create(book_issue = book_issue_instance, member_id = member_instance,is_renewed = True)
        book_renew.save()
        print(book_renew.expirydate)
        book_issue_instance.expirydate = book_renew.expirydate
        book_issue_instance.save()
        print(book_issue_instance.expirydate)
        messages.success(request, 'Book renewed successfully')

        return redirect('library:issue_list_for_renew',pk)


    return render(request, 'catalog/issue_list_for_renew.html')



def book_renew_edit(request, pk):
  
    book_instance = BookRenew.objects.get(id=pk)
    form = BookRenewForm(instance=book_instance)
    if request.method == 'POST':
        form = BookRenewForm(data=request.POST, files=request.FILES, instance=book_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book renew edited successfully')

            return redirect('library:book_renew_list')
    context = {
        'form':form
    }
    return render(request, 'catalog/book_renew_edit.html', context=context)



def book_renew_detail(request, pk):
  
    book_instance = BookRenew.objects.get(id=pk)
    form = BookRenewForm(instance= book_instance)
    context = {
        'form':form
    }
    return render(request, 'catalog/book_renew_detail.html', context=context)  



class BookRenewDeleteView(DeleteView):
    model = BookRenew
    template_name = 'catalog/confirm_delete.html'
    success_url = reverse_lazy('library:book_renew_list')



def add_library_fine(request):
    form = LibraryFineForm()
    if request.method == 'POST':
        form = LibraryFineForm(request.POST, request.FILES)
        if form.is_valid():   
            form.save()
            messages.success(request, 'Fine created successfully')

            return redirect('library:library_fine_list')
    context = {
        'form':form,
        'classes':Semester.objects.all()
    }
    return render(request, 'catalog/fines/add_fine.html', context=context)



def edit_library_fine(request,pk):
    library_fine_instance = LibraryFine.objects.get(id=pk)

    form = UpdateLibraryFineForm(instance = library_fine_instance)
    if request.method == 'POST':
        form = UpdateLibraryFineForm(request.POST, request.FILES,instance = library_fine_instance)
        if form.is_valid():   
            form.save()
            messages.success(request, 'Fine edited successfully')

            return redirect('library:library_fine_list')
    context = {
        'form':form,
        'classes':Semester.objects.all(),
        'fine_instance':library_fine_instance
    }
    return render(request, 'catalog/fines/edit_fine.html', context=context)


def library_fine_list(request):
    library_fine = LibraryFine.objects.all()
    return render(request, 'catalog/fines/fine_list.html', {'library_fine': library_fine})



class LibraryFineDeleteView(DeleteView):
    model = LibraryFine
    template_name = 'catalog/confirm_delete.html'
    success_url = reverse_lazy('library:library_fine_list')

