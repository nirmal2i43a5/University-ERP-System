from django.shortcuts import render, get_object_or_404, redirect

from student_management_app.models import CustomUser
from school_apps.customusers.forms import UserUpdateForm

# Create your views here.


from django.contrib.auth.decorators import login_required, permission_required


@permission_required("student_management_app.view_customuser",
                     raise_exception=True)
def manage_customuser(request):
    customusers = CustomUser.objects.all()
    context = {"title": "CustomUser", "customusers": customusers}
    return render(request, "customusers/manage.html", context)


@permission_required("student_management_app.change_customuser",
                     raise_exception=True)
def edit_customuser(request, pk):
    user_instance = get_object_or_404(CustomUser, pk=pk)
    form = UserUpdateForm(instance=user_instance)

    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user_instance)
        form.save()
        return redirect("customuser:manage_customuser")

    context = {"form": form}
    return render(request, "customusers/edit.html", context)
