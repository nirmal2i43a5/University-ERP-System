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
from .models import *
from .forms import *
from django.contrib.auth.models import User
from school_apps.library.models import LibraryMemberProfile



def category_list(request):
    category_list = Category.objects.all()
    return render(request, 'catalog/book_category/category_list.html', {'category_list': category_list})


def CategoryAddView(request):
    if not request.user.is_superuser:
        return redirect('login')
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
    if not request.user.is_superuser:
        return redirect('login')
    category_instance = Category.objects.get(id=pk)
    form = CategoryAddForm(instance= category_instance)
    context = {
        'form':form
    }
    return render(request, 'catalog/book_category/category_detail.html', context=context)

def CategoryUpdateView(request, pk):
    if not request.user.is_superuser:
        return redirect('login')
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
    if not request.user.is_superuser:
        return redirect('login')
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
    if not request.user.is_superuser:
        return redirect('login')
    book_instance = BookEntry.objects.get(isbn=pk)
    form = BookAddForm(instance= book_instance)
    if request.method == 'POST':
        form = BookForm(data=request.POST, files=request.FILES, instance=book_instance)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    context = {
        'form':form
    }
    return render(request, 'catalog/book_info/book_edit.html', context=context)



def book_list(request):
    book_list = BookEntry.objects.all()
    return render(request, 'catalog/book_info/book_list.html', {'book_list':book_list})



def view_book(request, pk):
    if not request.user.is_superuser:
        return redirect('login')
    book_instance = BookEntry.objects.get(isbn=pk)
    form = BookAddForm(instance= book_instance)
    context = {
        'form':form
    }
    return render(request, 'catalog/book_info/book_detail.html', context=context)



class BookDeleteView(DeleteView):
    model = BookEntry
    template_name = 'catalog/confirm_delete.html'
    success_url = reverse_lazy('book_list')



def member_list(request):
    memberlist = LibraryMemberProfile.objects.all()

    return render(request, 'catalog/member_list.html', {'memberlist': memberlist})



def add_member(request):
    form = AddMemberForm()
    if request.method == 'POST':
        form = AddMemberForm(request.POST, request.FILES)
        if form.is_valid():   
            form.save()
            return redirect('library:member_list')
    context = {
        'form':form,
    }
    return render(request, 'catalog/add_member.html', context=context)



def edit_member(request, pk):
    if not request.user.is_superuser:
        return redirect('login')
    member_instance = LibraryMemberProfile.objects.get(id=pk)
    form = EditMemberForm(instance=member_instance)
    if request.method == 'POST':
        form = EditMemberForm(request.POST, request.FILES, instance=member_instance)
        if form.is_valid():   
            form.save()
            return redirect('library:member_list')
    context = {
        'form':form,
    }
    return render(request, 'catalog/edit_member.html', context=context)



def member_detail(request, pk):
    if not request.user.is_superuser:
        return redirect('login')
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
    book_issue = Issue.objects.all()
    return render(request, 'catalog/book_issued_list.html', {'book_issue': book_issue})



class BookIssueCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Issue
    template_name = "catalog/issue_info/book_issue_form.html"
    fields = '__all__'
    success_message = "Book Issued added successfully."

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        print('Book added successfully!')
        return "Book Issued Successfully! "

    def get_context_data(self, **kwargs):
        data = super(BookIssueCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['items'] = BookIssueFormset(self.request.POST)
        else:
            data['items'] = BookIssueFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        items = context['items']
        with transaction.atomic():
            if items.is_valid():
                items.instance = form.save(commit=False)
                for i in items:
                    title=i.cleaned_data['title']
                    qt=i.cleaned_data['quantity']
                    book_quantity = BookEntry.objects.get(title=title)
                    if book_quantity.quantity < qt:
                        form.errors['value']='Your entered quantity exceeds book quantity'
                        return self.form_invalid(form)
                    else:
                        book_quantity.quantity -=qt
                        book_quantity.save()
                        form.save()
                        items.save()
                # sold_item.save()
        return super(BookIssueCreateView, self).form_valid(form)

    def get_initial(self):
        initial=super(BookIssueCreateView,self).get_initial()
        initial['member']=LibraryMemberProfile.objects.get(pk=self.kwargs['pk'])
        return initial



# def book_issue(request):
#     if not request.user.is_superuser:
#         return redirect('login')
#     form = BookIssueForm()
#     if request.method == 'POST':
#         form = BookIssueForm(request.POST, request.FILES)
#         if form.is_valid():
#             title=form.cleaned_data['issue_book_name']
#             qt=form.cleaned_data['quantity']
#             print(title)
#             print(qt)
#             book_quantity = BookEntry.objects.get(title=title)
#             if book_quantity.quantity < qt:
#                 form.errors['value']='Your entered quantity exceeds book quantity'
#                 return self.form_invalid(form)
#             else:
#                 book_quantity.quantity -=qt
#                 book_quantity.save()
#                 form.save()
#             return redirect('library:book_issue_list')
#     context = {
#         'form':form
#     }
#     return render(request, 'catalog/book_issue.html', context=context)


def book_issue_edit(request, issue_id):
    book_instance = Issue.objects.get(id=issue_id)
    form = IssueForm(request.POST,instance=book_instance)
    ItemFormset = inlineformset_factory(Issue, BookIssue, form=IssueForm, extra=0)
    if request.method == 'POST':
        formset = ItemFormset(data = request.POST, files = request.FILES, instance=book_instance)
        if form.is_valid():
            form.save()
            formset.save()
            return redirect('library:book_issue_list')
    else:
        form = IssueForm(instance=book_instance)
        formset = ItemFormset(instance=book_instance)

    return render(request, 'catalog/book_issue_edit.html', {'form': form, 'formset': formset})



class book_issue_detail(LoginRequiredMixin,DetailView):
    model = Issue
    template_name = 'catalog/book_issue_detail.html'

    def get_context_data(self, **kwargs):
        context = super(book_issue_detail, self).get_context_data(**kwargs)
        return context



class BookIssueDeleteView(DeleteView):
    model = Issue
    template_name = 'catalog/confirm_delete.html'
    success_url = reverse_lazy('library:book_issue_list')


# ----------------------------- Book return CRUD views ------------------------------------------
def book_return_list(request):
    book_return = Issue.objects.all()
    return render(request, 'catalog/book_return_list.html', {'book_return': book_return})



def book_return(request):
    book_return = BookReturn.objects.all()
    return render(request, 'catalog/return_info/book_return.html', {'book_return': book_return})



class BookReturnView(LoginRequiredMixin,DetailView,CreateView):
    model = Issue
    fields='__all__'
    template_name = 'catalog/book_return_update.html'

    def get_context_data(self, **kwargs):
        data = super(BookReturnView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['items'] = BookIssueReturnFormset(self.request.POST)
        else:
            data['items'] = BookIssueReturnFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        print(context)
        member_id=LibraryMemberProfile.objects.get(pk=self.kwargs['pk'])
        user_id=User.objects.get(username=member_id)
        member_id=LibraryMemberProfile.objects.get(member=user_id)
        # issue_id = Issue.objects.get(member_id=member_id)
        items = context['items']
        with transaction.atomic():
            if items.is_valid():
                items.instance = form.save()
                items.save()
                for i in items:
                    title = i.cleaned_data['title']
                    qt=i.cleaned_data['quantity']
                    isbn=i.cleaned_data['isbn']
                    # issue_item_id = BookIssue.objects.filter(issue_id_id=issue_id, isbn=isbn)
                    # for i in issue_item_id:
                    #     i.quantity -= qt
                    #     i.save()
                    issued_item=BookEntry.objects.get(title=title)
                    issued_item.quantity +=qt
                    issued_item.save()
        return super(BookReturnView, self).form_valid(form)

    # def get_initial(self):
    #     initial=super(BookReturnView,self).get_initial()
    #     initial['member']=LibraryMemberProfile.objects.get(pk=self.kwargs['pk'])
    #     return initial


# def book_return(request):
#     if not request.user.is_superuser:
#         return redirect('login')
#     form = BookReturnForm()
#     if request.method == 'POST':
#         form = BookReturnForm(request.POST, request.FILES)
#         if form.is_valid():
#             title=form.cleaned_data['title']
#             qt=form.cleaned_data['quantity']
#             print(title)
#             print(qt)
#             book_quantity = BookEntry.objects.get(title=title)
#             if book_quantity.quantity < qt:
#                 form.errors['value']='Your entered quantity exceeds book quantity'
#                 return self.form_invalid(form)
#             else:
#                 book_quantity.quantity += qt
#                 book_quantity.save()
#                 form.save()
#             return redirect('library:book_return_list')
#     context = {
#         'form':form
#     }
#     return render(request, 'catalog/add_book_return.html', context=context)



def book_return_edit(request, pk):
    if not request.user.is_superuser:
        return redirect('login')
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
    if not request.user.is_superuser:
        return redirect('login')
    book_instance = BookReturn.objects.get(id=pk)
    form = BookReturnForm(instance= book_instance)
    context = {
        'form':form
    }
    return render(request, 'catalog/book_return_detail.html', context=context)  



class BookReturnDeleteView(DeleteView):
    model = BookReturn
    template_name = 'catalog/confirm_delete.html'
    success_url = reverse_lazy('book_return_list')


# ----------------------------- Book renew CRUD views ------------------------------------------
def book_renew_list(request):
    book_renew = BookRenew.objects.all()
    return render(request, 'catalog/book_renew_list.html', {'book_renew':book_renew})



def book_renew(request):
    if not request.user.is_superuser:
        return redirect('login')
    form = BookRenewForm()
    if request.method == 'POST':
        form = BookRenewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('library:book_renew_list')
    context = {
        'form':form
    }
    return render(request, 'catalog/add_book_renew.html', context=context)



def book_renew_edit(request, pk):
    if not request.user.is_superuser:
        return redirect('login')
    book_instance = BookRenew.objects.get(id=pk)
    form = BookRenewForm(instance=book_instance)
    if request.method == 'POST':
        form = BookRenewForm(data=request.POST, files=request.FILES, instance=book_instance)
        if form.is_valid():
            form.save()
            return redirect('library:book_renew_list')
    context = {
        'form':form
    }
    return render(request, 'catalog/book_renew_edit.html', context=context)



def book_renew_detail(request, pk):
    if not request.user.is_superuser:
        return redirect('login')
    book_instance = BookRenew.objects.get(id=pk)
    form = BookRenewForm(instance= book_instance)
    context = {
        'form':form
    }
    return render(request, 'catalog/book_renew_detail.html', context=context)  



class BookRenewDeleteView(DeleteView):
    model = BookRenew
    template_name = 'catalog/confirm_delete.html'
    success_url = reverse_lazy('book_renew_list')



