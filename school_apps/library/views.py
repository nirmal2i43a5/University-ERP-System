from django.utils import timezone
from django.db.models import Prefetch, Subquery
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import DeleteView
from django.views.generic import DetailView
from student_management_app.models import Semester
from .models import *
from .forms import *
from school_apps.library.models import LibraryMemberProfile
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import LibraryMemberProfile, BookIssue, LibraryFine
from datetime import datetime


@permission_required("library.view_category", raise_exception=True)
def category_list(request):
    category_list = Category.objects.all()
    return render(
        request,
        "catalog/book_category/category_list.html",
        {"category_list": category_list},
    )


@permission_required("library.add_category", raise_exception=True)
def add_category(request):
    form = CategoryAddForm()
    if request.method == "POST":
        form = CategoryAddForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect("library:category_list")
    context = {"form": form}
    return render(
        request,
        "catalog/book_category/category_add.html",
        context=context)


@permission_required("library.view_category", raise_exception=True)
def view_category(request, pk):
    category_instance = Category.objects.get(id=pk)
    form = CategoryAddForm(instance=category_instance)
    context = {"form": form}
    return render(
        request, "catalog/book_category/category_detail.html", context=context
    )


@permission_required("library.change_category", raise_exception=True)
def update_category(request, pk):
    category_instance = Category.objects.get(id=pk)
    form = CategoryAddForm(instance=category_instance)
    if request.method == "POST":
        form = CategoryAddForm(
            data=request.POST, files=request.FILES, instance=category_instance
        )
        if form.is_valid():
            form.save()
            return redirect("library:category_list")
    context = {"form": form}
    return render(
        request, "catalog/book_category/category_update.html", context=context
    )


class CategoryDeleteView(PermissionRequiredMixin, DeleteView):
    model = Category
    template_name = "catalog/confirm_delete.html"
    success_url = reverse_lazy("category_list")
    permission_required = "library.delete_category"


@permission_required("library.add_bookentry", raise_exception=True)
def add_book(request):
    form = BookAddForm()
    if request.method == "POST":
        form = BookForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect("library:book_list")
    context = {"form": form}
    return render(request, "catalog/book_info/add_book.html", context=context)


@permission_required("library.change_bookentry", raise_exception=True)
def edit_book(request, pk):
    book_instance = BookEntry.objects.get(isbn=pk)
    form = BookAddForm(instance=book_instance)
    if request.method == "POST":
        form = BookForm(
            data=request.POST,
            files=request.FILES,
            instance=book_instance)
        if form.is_valid():
            form.save()
            return redirect("library:book_list")
    context = {"form": form}
    return render(request, "catalog/book_info/book_edit.html", context=context)


@permission_required("library.view_bookentry", raise_exception=True)
def book_list(request):
    book_list = BookEntry.objects.all()
    return render(request,
                  "catalog/book_info/book_list.html",
                  {"book_list": book_list})


@permission_required("library.view_bookentry", raise_exception=True)
def view_book(request, pk):
    book_instance = BookEntry.objects.get(isbn=pk)
    form = BookAddForm(instance=book_instance)
    context = {"form": form}
    return render(
        request,
        "catalog/book_info/book_detail.html",
        context=context)


class BookDeleteView(PermissionRequiredMixin, DeleteView):
    model = BookEntry
    template_name = "catalog/confirm_delete.html"
    success_url = reverse_lazy("library:book_list")
    permission_required = "library.delete_bookentry"


@permission_required("library.view_librarymemberprofile", raise_exception=True)
def member_list(request):
    memberlist = LibraryMemberProfile.objects.all()
    return render(request,
                  "catalog/member_list.html",
                  {"memberlist": memberlist})


@permission_required("library.add_librarymemberprofile", raise_exception=True)
def add_member(request):
    form = AddMemberForm()
    if request.method == "POST":
        form = AddMemberForm(request.POST, request.FILES)
        member_id = request.POST["member"]
        student_instance = Student.objects.get(pk=member_id)
        library_number = f"{student_instance.stu_id}-{student_instance.join_year}"
        if LibraryMemberProfile.objects.filter(
                member=student_instance).exists():
            messages.error(request, "Member already exist")
            return redirect("library:member_list")
        else:
            if form.is_valid():
                instance = form.save(commit=False)
                instance.library_card_no = library_number
                instance.save()
                messages.success(request, "Member added successfully")

                return redirect("library:member_list")
    context = {"form": form, "classes": Semester.objects.all()}
    return render(request, "catalog/add_member.html", context=context)


@permission_required("library.change_librarymemberprofile",
                     raise_exception=True)
def edit_member(request, pk):
    member_instance = LibraryMemberProfile.objects.get(id=pk)
    form = AddMemberForm(instance=member_instance)
    if request.method == "POST":
        form = AddMemberForm(
            request.POST,
            request.FILES,
            instance=member_instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Member updated successfully")

            return redirect("library:member_list")
    context = {"form": form, "member_instance": member_instance}
    return render(request, "catalog/add_member.html", context=context)


@permission_required("library.view_librarymemberprofile", raise_exception=True)
def member_detail(request, pk):
    member_instance = LibraryMemberProfile.objects.get(id=pk)
    form = MemberDetailForm(instance=member_instance)
    context = {"form": form}
    return render(request, "catalog/member_detail.html", context=context)


class MemberDeleteView(PermissionRequiredMixin, DeleteView):
    model = LibraryMemberProfile
    template_name = "catalog/confirm_delete.html"
    success_url = reverse_lazy("library:member_list")
    # success_message = 'Member deleted successfully'
    permission_required = "library.delete_librarymemberprofile"


@permission_required("library.view_bookissue", raise_exception=True)
def book_issue_list(request):
    book_issue = BookIssue.objects.all()
    return render(
        request,
        "catalog/book_issued_list.html",
        {
            "book_issue": book_issue,
        },
    )


@permission_required("library.view_bookrenew", raise_exception=True)
def renew_issue(request):
    member_ids = BookIssue.objects.values_list(
        "issue_member", flat=True).distinct()
    members = LibraryMemberProfile.objects.filter(id__in=member_ids)
    context = {"members": members}

    return render(request, "catalog/renew_issue.html", context=context)


@permission_required("library.view_bookreturn", raise_exception=True)
def return_issue(request):
    member_ids = BookIssue.objects.values_list(
        "issue_member", flat=True).distinct()

    members = LibraryMemberProfile.objects.filter(id__in=member_ids)
    context = {"members": members}

    return render(request, "catalog/return_issue.html", context=context)


@permission_required("library.add_bookreturn", raise_exception=True)
def issue_list_for_return(request, pk):
    member = LibraryMemberProfile.objects.get(pk=pk)
    book_issue = member.bookissue_set.all()
    context = {"book_issue": book_issue, "member": member}
    return render(
        request,
        "catalog/issue_list_for_return.html",
        context=context)


@permission_required("library.add_bookissue", raise_exception=True)
def book_issue(request):
    form = BookIssueForm()
    if request.method == "POST":
        form = BookIssueForm(request.POST, request.FILES)
        if form.is_valid():
            book_instance = form.cleaned_data["title"]
            quantity = form.cleaned_data["quantity"]
            book_quantity = BookEntry.objects.get(isbn=book_instance.isbn)
            if book_quantity.quantity < quantity:
                messages.error(
                    request,
                    f"Your entered quantity exceeds book quantity.There is only {book_quantity.quantity} books left",
                )

                return redirect("library:book_issue")

            else:
                book_quantity.quantity -= quantity
                book_quantity.save()
                form.save()
                messages.success(request, "Book issued successfully")
            return redirect("library:book_issue_list")
    context = {"form": form, "classes": Semester.objects.all()}
    return render(request, "catalog/book_issue.html", context=context)


@permission_required("library.change_bookissue", raise_exception=True)
def book_issue_edit(request, issue_id):
    book_instance = BookIssue.objects.get(id=issue_id)

    if request.method == "POST":
        form = BookIssueEditForm(request.POST, instance=book_instance)
        if form.is_valid():
            quantity = form.cleaned_data["quantity"]
            book_instance = form.cleaned_data["title"]
            book_quantity = BookEntry.objects.get(isbn=book_instance.isbn)
            if book_quantity.quantity < quantity:
                messages.error(
                    request,
                    f"Your entered quantity exceeds book quantity.There is only {book_quantity.quantity} books left",
                )
                return redirect("library:book_issue_edit", issue_id=issue_id)

            else:
                book_quantity.quantity -= quantity
                book_quantity.save()
                form.save()
                messages.success(request, "Book issued Updated successfully")

            return redirect("library:book_issue_list")
    else:
        form = BookIssueEditForm(instance=book_instance)

    return render(
        request,
        "catalog/book_issue_edit.html",
        {
            "form": form,
        },
    )


class book_issue_detail(PermissionRequiredMixin, DetailView):
    model = Issue
    template_name = "catalog/book_issue_detail.html"
    permission_required = "library.view_bookissue"

    def get_context_data(self, **kwargs):
        context = super(book_issue_detail, self).get_context_data(**kwargs)
        return context


class BookIssueDeleteView(PermissionRequiredMixin, DeleteView):
    model = BookIssue
    template_name = "catalog/confirm_delete.html"
    success_url = reverse_lazy("library:book_issue_list")
    permission_required = "library.delete_bookissue"


@permission_required("library.view_bookreturn", raise_exception=True)
def book_return_list(request):
    book_return = BookReturn.objects.all()
    return render(
        request, "catalog/book_return_list.html", {"book_return": book_return}
    )


@permission_required("library.add_bookreturn", raise_exception=True)
def book_return(request, pk):
    if request.method == "POST":
        quantity = request.POST.get("quantity")
        bookissue_id = request.POST.get("bookissue_id")
        isbn = request.POST.get("book_id")

        book_issue_instance = BookIssue.objects.get(pk=bookissue_id)
        book_quantity = BookEntry.objects.get(pk=isbn)

        if book_quantity.quantity < int(quantity):
            messages.error(
                request,
                f"Your entered quantity exceeds book quantity.There is only {book_quantity.quantity} books left",
            )
            return redirect("library:issue_list_for_return", pk)
        else:
            book_quantity.quantity += int(quantity)
            book_issue_instance.quantity -= int(quantity)
            book_quantity.save()
            book_issue_instance.save()
            book_return = BookReturn.objects.create(
                book_issue=book_issue_instance, quantity=quantity, is_returned=True)
            book_return.save()
            messages.success(request, "Book returned successfully")

        return redirect("library:issue_list_for_return", pk)

    return render(request, "catalog/issue_list_for_return.html")


@permission_required("library.change_bookreturn", raise_exception=True)
def book_return_edit(request, pk):
    book_instance = BookReturn.objects.get(id=pk)
    form = BookReturnForm(instance=book_instance)
    if request.method == "POST":
        form = BookReturnForm(
            data=request.POST, files=request.FILES, instance=book_instance
        )
        if form.is_valid():
            form.save()
            return redirect("library:book_return_list")
    context = {"form": form}
    return render(request, "catalog/book_return_edit.html", context=context)


@permission_required("library.view_bookreturn", raise_exception=True)
def book_return_detail(request, pk):
    book_instance = BookReturn.objects.get(id=pk)
    form = BookReturnForm(instance=book_instance)
    context = {"form": form}
    return render(request, "catalog/book_return_detail.html", context=context)


class BookReturnDeleteView(PermissionRequiredMixin, DeleteView):
    model = BookReturn
    template_name = "catalog/confirm_delete.html"
    success_url = reverse_lazy("library:book_return_list")
    permission_required = "library.delete_bookreturn"


@permission_required("library.view_bookrenew", raise_exception=True)
def book_renew_list(request):
    book_renew = BookRenew.objects.all()
    return render(request,
                  "catalog/book_renew_list.html",
                  {"book_renew": book_renew})


@permission_required("library.add_bookrenew", raise_exception=True)
def issue_list_for_renew(request, pk):
    member = LibraryMemberProfile.objects.get(pk=pk)
    all_book_issues = member.bookissue_set.all()
    prefetch = Prefetch(
        "bookrenew",
        queryset=BookRenew.objects.order_by("-expirydate").only(
            "expirydate", "is_renewed"
        ),
        to_attr="latest_renewal",
    )

    # Apply the prefetch to BookIssue queryset
    book_issues = all_book_issues.prefetch_related(prefetch)

    # Access latest expiry date and is_renewed status for each BookIssue
    book_renew_details = []
    for book_issue in book_issues:
        latest_renewal = (
            book_issue.latest_renewal[0] if book_issue.latest_renewal else None
        )
        print(latest_renewal)
        expiry_date = latest_renewal.expirydate if latest_renewal else None
        is_renewed = latest_renewal.is_renewed if latest_renewal else None

        # print(days_late_to_renew,"********************88")
        book_renew_details.append(
            {
                "expiry_date": expiry_date,
                "is_renewed": is_renewed,
                #    'days_late_to_renew':days_late_to_renew
            }
        )
    print(book_renew_details)

    context = {
        "book_issue": zip(all_book_issues, book_renew_details),
        # 'book_issue':book_issues,
        "member": member,
    }
    return render(request, "catalog/add_book_renew.html", context=context)


@permission_required("library.add_bookrenew", raise_exception=True)
def book_renew(request, pk):
    if request.method == "POST":
        bookissue_id = request.POST.get("bookissue_id")
        member_instance = LibraryMemberProfile.objects.get(pk=pk)
        book_issue_instance = BookIssue.objects.get(pk=bookissue_id)
        book_renew = BookRenew.objects.create(
            book_issue=book_issue_instance,
            member_id=member_instance,
            is_renewed=True)
        book_renew.save()
        book_issue_instance.expirydate = book_renew.expirydate
        book_issue_instance.save()
        messages.success(request, "Book renewed successfully")
        return redirect("library:issue_list_for_renew", pk)
    return render(request, "catalog/issue_list_for_renew.html")


@permission_required("library.change_bookrenew", raise_exception=True)
def book_renew_edit(request, pk):
    book_instance = BookRenew.objects.get(id=pk)
    form = BookRenewForm(instance=book_instance)

    if request.method == "POST":
        form = BookRenewForm(
            data=request.POST, files=request.FILES, instance=book_instance
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Book renew edited successfully")

            return redirect("library:book_renew_list")
    context = {"form": form}
    return render(request, "catalog/book_renew_edit.html", context=context)


@permission_required("library.view_bookrenew", raise_exception=True)
def book_renew_detail(request, pk):
    book_instance = BookRenew.objects.get(id=pk)
    form = BookRenewForm(instance=book_instance)
    context = {"form": form}
    return render(request, "catalog/book_renew_detail.html", context=context)


class BookRenewDeleteView(PermissionRequiredMixin, DeleteView):
    model = BookRenew
    template_name = "catalog/confirm_delete.html"
    success_url = reverse_lazy("library:book_renew_list")
    permission_required = "library.delete_bookrenew"


# @permission_required('library.add_libraryfine', raise_exception=True)
# def add_library_fine(request):
#         # Get the current date
#     current_date = datetime.now().date()

#     # Get all LibraryMemberProfile objects using an iterator
#     users = LibraryMemberProfile.objects.iterator()

#     # Loop through each user
#     for user in users:
#         # Get the books issued by the user
#         issued_books = BookIssue.objects.filter(member_id=user)

#         # Check the expiry date of each book and create fines if needed
#         for issued_book in issued_books:
#             if issued_book.expirydate < current_date:
#                 # Create the LibraryFine instance for the overdue book
#                 fine = LibraryFine.objects.create(
#                     fine_member=user,
#                     book=issued_book.book,
#                     fine_amount=10.00,  # Set the default fine amount as needed
#                     is_paid=False,  # Set the default is_paid value as needed
#                 )
#     # form = LibraryFineForm()
#     # if request.method == 'POST':
#     #     form = LibraryFineForm(request.POST, request.FILES)
#     #     if form.is_valid():
#     #         form.save()
#     #         messages.success(request, 'Fine created successfully')

#     #         return redirect('library:library_fine_list')
#     context = {
#         # 'form':form,
#         # 'classes':Semester.objects.all()
#     }
#     return render(request, 'catalog/fines/add_fine.html', context=context)


@permission_required("library.change_libraryfine", raise_exception=True)
def edit_library_fine(request, pk):
    library_fine_instance = LibraryFine.objects.get(id=pk)

    form = UpdateLibraryFineForm(instance=library_fine_instance)
    if request.method == "POST":
        form = UpdateLibraryFineForm(
            request.POST, request.FILES, instance=library_fine_instance
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Fine edited successfully")

            return redirect("library:library_fine_list")
    context = {
        "form": form,
        "classes": Semester.objects.all(),
        "fine_instance": library_fine_instance,
    }
    return render(request, "catalog/fines/edit_fine.html", context=context)


@permission_required("library.view_libraryfine", raise_exception=True)
def library_fine_list(request):
    library_fine = LibraryFine.objects.all()
    return render(
        request, "catalog/fines/fine_list.html", {"library_fine": library_fine}
    )


class LibraryFineDeleteView(PermissionRequiredMixin, DeleteView):
    model = LibraryFine
    template_name = "catalog/confirm_delete.html"
    success_url = reverse_lazy("library:library_fine_list")
    permission_required = "library.delete_libraryfine"


@permission_required("library.add_libraryfine", raise_exception=True)
def set_default_fine(request):
    fine_instance = SetFine.objects.get(pk=1)
    form = SetFineForm(instance=fine_instance)
    if request.method == "POST":
        form = SetFineForm(request.POST, instance=fine_instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Fine set successfully")
            return redirect("library:set_default_fine")
    context = {
        "form": form,
    }
    return render(request, "catalog/fines/set_fine.html", context=context)


@permission_required("library.add_libraryfine", raise_exception=True)
def add_library_fine(request):
    if request.method == "POST":
        current_date = datetime.now().date()

        # Get all LibraryMemberProfile objects who have issued books
        users_with_issued_books = LibraryMemberProfile.objects.filter(
            bookissue__isnull=False
        ).distinct()

        # Loop through each user with issued books
        for user in users_with_issued_books:
            # Get the books issued by the user
            issued_books = BookIssue.objects.filter(issue_member=user)

            # Process each issued book and update/create fines as needed
            for issued_book in issued_books:
                if issued_book.expirydate < current_date:
                    # Calculate the fine amount for the overdue book
                    fine_amount = (
                        current_date - issued_book.expirydate
                    ).days * 5.00  # Assuming Rs. 5 per day

                    # Check if a fine already exists for this book
                    try:
                        fine = LibraryFine.objects.get(
                            book_issue=issued_book, fine_member=user
                        )
                        fine.fine_amount = fine_amount
                        fine.payment_date = current_date
                        fine.save()
                    except LibraryFine.DoesNotExist:
                        fine = LibraryFine.objects.create(
                            fine_member=user,
                            book_issue=issued_book,
                            fine_amount=fine_amount,
                            is_paid=False,
                            # payment_date=current_date
                        )
        messages.success(request, "Fine created successfully")

    return render(request, "catalog/fines/add_fine.html")
