import json
import datetime
from typing import Pattern
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from student_management_app.django_forms.forms import (
    AddCustomUserForm,
    DocumentFileForm,
)
from school_apps.parents.forms import (
    ParentForm,
    ParentCustomUserForm,
)

from student_management_app.models import (
    CustomUser,
    Staff,
    Student,
    Parent,
    DocumentFile,
    Student,
)

from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required


@permission_required("student_management_app.add_parent", raise_exception=True)
def add_parent(request):
    if request.method == "POST":
        custom_form = ParentCustomUserForm(request.POST)
        parent_form = ParentForm(request.POST, request.FILES)

        if custom_form.is_valid() and parent_form.is_valid():
            username = custom_form.cleaned_data["username"]
            email = custom_form.cleaned_data["email"]
            password = custom_form.cleaned_data["password"]
            full_name = custom_form.cleaned_data["full_name"]

            if request.FILES.get("image"):
                image_url = request.FILES["image"]
            else:
                image_url = None

            try:
                group = Group.objects.get(name="Parent")

                user = CustomUser.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    full_name=full_name,
                    user_type=group,
                )

                user.parent.local_guardian_name = parent_form.cleaned_data[
                    "local_guardian_name"
                ]
                user.parent.mother_name = parent_form.cleaned_data[
                    "mother_name"
                ].capitalize()
                user.parent.father_profession = parent_form.cleaned_data[
                    "father_profession"
                ]
                user.parent.mother_profession = parent_form.cleaned_data[
                    "mother_profession"
                ]
                user.parent.address = parent_form.cleaned_data["address"]
                user.parent.father_phone = parent_form.cleaned_data["father_phone"]
                user.parent.mother_phone = parent_form.cleaned_data["mother_phone"]
                user.parent.local_guardian_phone = parent_form.cleaned_data[
                    "local_guardian_phone"
                ]

                if image_url is not None:
                    user.parent.image = image_url

                user.save()
                # adding user to particular group.ie role
                user.groups.add(group)

                messages.success(request, "Successfully Added Parent")
                return redirect("admin_app:manage_parent")

            except BaseException:
                messages.error(request, "Failed to Add Parent")
                return redirect("admin_app:add_parent")

    else:
        custom_form = ParentCustomUserForm()
        parent_form = ParentForm()

    context = {"custom_form": custom_form, "parent_form": parent_form}
    return render(request, "parents/add_parent.html", context)


@permission_required("student_management_app.view_parent",
                     raise_exception=True)
def manage_parent(request):
    parents = Parent.objects.all()
    context = {"parents": parents}
    return render(request, "parents/manage_parent.html", context)


@permission_required("student_management_app.change_parent",
                     raise_exception=True)
def edit_parent(request, parent_id):
    parent_form_instance = get_object_or_404(Parent, parent_user=parent_id)
    custom_form_instance = get_object_or_404(CustomUser, pk=parent_id)

    if request.method == "POST":
        parent_form = ParentForm(
            request.POST, request.FILES, instance=parent_form_instance
        )
        custom_form = ParentCustomUserForm(
            request.POST, instance=custom_form_instance)

        try:
            if parent_form.is_valid() and custom_form.is_valid():
                parent_form.save()
                custom_form.save()
                messages.success(request, "Successfully Edited Parent")
                return redirect("admin_app:manage_parent")

        except BaseException:
            messages.error(request, "Failed to Update Parent")
            return redirect("admin_app:add_parent")
    else:
        parent_form = ParentForm(instance=parent_form_instance)
        custom_form = ParentCustomUserForm(instance=custom_form_instance)

    context = {"parent_form": parent_form, "custom_form": custom_form}
    return render(request, "parents/edit_parent.html", context)


@permission_required("student_management_app.delete_parent",
                     raise_exception=True)
def delete_parent(request, parent_id):
    try:
        # i am using custom user so i use staff_user_id instead of normal
        # parent id = staff_id
        parent = get_object_or_404(Parent, parent_user=parent_id)
        parent.delete()
        messages.success(
            request, f"{parent.parent_user.username} is Deleted Successfully"
        )
        return redirect("admin_app:manage_parent")
    except BaseException:
        messages.error(request, "Failed To Delete Parent")
        return redirect("admin_app:manage_parent")


# this is for ajax part (my ajax is success with title with title but file
# cannot upload so i am using above views for )
@csrf_exempt
@permission_required("student_management_app.add_parent_document",
                     raise_exception=True)
def add_parent_document(request, parent_id):  # for ajax part
    parent = get_object_or_404(Parent, pk=parent_id)

    if request.method == "POST":
        form = DocumentFileForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            document_id = request.POST["documentid"]  # this is hidden field
            print(document_id)
            title = request.POST.get("title")
            file = request.FILES["file"]
            # if there is no product id then it has to insert data clicking on
            # save button
            if (document_id == ""):
                document = form.save(commit=False)

                # when i add_file then it must be the file of particular
                # student with their respective id and i can retrieve this
                # using _set see in view_student views function
                document.parent = parent

            else:  # if not id then edit data clicking on save button
                document = form.save(commit=False)
                document.id = document_id  # for updating particular field
                document.parent = parent

            # when i add_file then it must be the file of particular student
            # with their respective id and i can retrieve this using _set see
            # in view_student views function
            document.save()
            # this filter data to show in ajax but commit filter for database
            document_value = DocumentFile.objects.filter(
                parent=parent).values()
            document_data = list(document_value)  # change to json
            print(document_data)
            return JsonResponse(
                {
                    "status": "True",
                    "document_data": document_data,
                    "message": "Document is Successfully Saved",
                },
                safe=False,
            )
        else:
            return JsonResponse({"status": 0})


# logic for student_profile and add_submit data with modal form

# class ParentView(View):
#     def get(self, request, *args, **kwargs):
#         # children = get_object_or_404(Student, pk = kwargs['pk'])
#         try:
# parent = get_object_or_404(Parent, id = kwargs['parent_id'])#this is the
# student_id  come from student not from customuser<check in view click>

#         except:
#             return render(request, '404.html')

#         #retrieve DocumentFile upload for particualr student using foreign key
#         parent_files =  parent.documentfile_set.all()

#         #this is for adding document form that is in view_student
#         form = DocumentFileForm()

#         context = {'parent':parent,
#                 'parent_files':parent_files,
#                 'form':form,
#                 'childrens':children
#                 }
#         return render(request, 'parents/views/main_view.html',context)


@permission_required("student_management_app.view_parent_profile",
                     raise_exception=True)
def view_parent(request, parent_id):
    try:
        # this is the  student_id  come from student not from customuser<check
        # in view click>
        parent = get_object_or_404(Parent, pk=parent_id)
    except BaseException:
        return render(request, "404.html")

    children = parent.student_set.all()

    # retrieve DocumentFile upload for particualr student using foreign key
    parent_files = parent.documentfile_set.all()

    # this is for adding document form that is in view_student
    form = DocumentFileForm()

    context = {
        "parent": parent,
        "parent_files": parent_files,
        "form": form,
        "childrens": children,
    }
    return render(request, "parents/views/main_view.html", context)


# this is for edit student document(for edit it also goes to else part in add)
@csrf_exempt
@permission_required(
    "student_management_app.edit_parent_document", raise_exception=True
)
def edit_parent_document(request):
    id = request.POST.get("documentid")
    if request.method == "POST":
        id = request.POST.get("documentid")

    document = get_object_or_404(DocumentFile, pk=id)

    # you can't serialize the object, because it's an Image. You have to
    # serialize the string representation of it's path.
    file_data = json.dumps(str(document.file))

    document_data = {
        "id": document.id,
        "title": document.title,
        "file": file_data}
    """i cant see file but cant see title instance while click edit button .because i am not passing--
    "file":file as it gives file field cannt be json serailize.so ,I will solve this problem in future
    """
    return JsonResponse(document_data, safe=False)


@permission_required(
    "student_management_app.delete_parent_document", raise_exception=True
)
def delete_parent_document(request, parent_id, document_id):
    try:
        # i am using custom user so i use staff_user_id instead of normal
        # document id = staff_id
        document = get_object_or_404(DocumentFile, pk=document_id)
        document.delete()
        messages.success(request, f"Document is Deleted Successfully")
        return redirect("admin_app:view_parent", parent_id)
    except BaseException:
        messages.error(request, "Failed To Delete Document")
        return redirect("admin_app:view_parent", parent_id)
