from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages


from student_management_app.django_forms.administrative_forms import (
    ComplainForm,
)
from student_management_app.models import Complain


from django.contrib.auth.decorators import permission_required


@permission_required("student_management_app.view_complain",
                     raise_exception=True)
def manage_complain(request):
    complains = Complain.objects.all()
    context = {"complains": complains, "title": "Manage Complain"}
    return render(
        request,
        "administrator/complains/manage_complain.html",
        context)


@permission_required("student_management_app.add_complain",
                     raise_exception=True)
def add_complain(request):
    form = ComplainForm()
    if request.method == "POST":
        form = ComplainForm(request.POST, request.FILES)

        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Successfully Added Complain.")
                return redirect("complain:manage_complain")
        except BaseException:
            messages.error(request, "Failed To  Added Complain.")
            return redirect("complain:add_complain")

    context = {"form": form, "title": "Complain"}
    return render(
        request,
        "administrator/complains/add_complain.html",
        context)


@permission_required("student_management_app.change_complain",
                     raise_exception=True)
def edit_complain(request, complain_id):
    try:
        complain = get_object_or_404(Complain, id=complain_id)
    except BaseException:
        return render(request, "404.html")

    form = ComplainForm(instance=complain)
    if request.method == "POST":
        form = ComplainForm(request.POST, request.FILES, instance=complain)

        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Successfully Update Complain.")
                return redirect("complain:manage_complain")

        except BaseException:
            messages.error(request, "Failed To  Update Complain.")
            return redirect("complain:edit_complain", complain_id)

    context = {"form": form, "title": "Complain"}
    return render(
        request,
        "administrator/complains/edit_complain.html",
        context)


@permission_required("student_management_app.delete_complain",
                     raise_exception=True)
def delete_complain(request, complain_id):
    try:
        # i am using custom user so i use staff_user_id instead of normal
        # complain id = staff_id
        complain = get_object_or_404(Complain, id=complain_id)
        complain.delete()
        messages.success(request, f"Complain is Deleted Successfully")
        return redirect("complain:manage_complain")
    except BaseException:
        messages.error(request, "Failed To Delete Complain")
        return redirect("complain:manage_complain")
