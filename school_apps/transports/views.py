"""This views contains all the logic for admin work"""
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q

from school_apps.academic.forms import ClassFormSearch
from school_apps.transports.forms import TransportForm
from student_management_app.models import Student

from school_apps.transports.models import Transport
from django.contrib.auth.decorators import login_required, permission_required


@permission_required("transports.add_transport", raise_exception=True)
def add_transport(request):
    if request.method == "POST":
        form = TransportForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Transport is Added Successfully.")
                return redirect("admin_app:manage_transport")
        except BaseException:
            messages.error(request, "Failed to Add Transport.")
            return redirect("admin_app:add_transport")
    else:
        form = TransportForm()

    context = {"form": form, "title": "Transport"}
    return render(request, "transports/add_transport.html", context)


@permission_required("transports.change_transport", raise_exception=True)
def edit_transport(request, transport_id):
    transport_instance = get_object_or_404(Transport, id=transport_id)
    if request.method == "POST":
        form = TransportForm(
            request.POST,
            request.FILES,
            instance=transport_instance)

        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Transport is Updated Successfully.")
                return redirect("admin_app:manage_transport")
        except BaseException:
            messages.error(request, "Failed to Updated Transport.")
            return redirect("admin_app:edit_transport")

    else:
        form = TransportForm(instance=transport_instance)

    context = {"form": form, "title": "Transport"}
    return render(request, "transports/edit_transport.html", context)


@permission_required("transports.delete_transport", raise_exception=True)
def delete_transport(request, transport_id):
    try:
        transport = get_object_or_404(Transport, id=transport_id)
        transport.delete()
        messages.success(
            request,
            f" Transport route {transport.route_name} is Deleted Successfully")
        return redirect("admin_app:manage_transport")
    except BaseException:
        messages.error(request, "Failed To Delete Transport route")
        return redirect("admin_app:manage_transport")


@permission_required("transports.view_transport", raise_exception=True)
def manage_transport(request):
    transports = Transport.objects.all()
    context = {"transports": transports, "title": "Mange Transport"}
    return render(request, "transports/manage_transport.html", context)


# student search based on class
def transport_member(request):
    students = Student.objects.all()
    # this is for rendering search field in same page
    search_form = ClassFormSearch(user=request.user)
    query = request.GET.get("semester")
    if query:
        search_students = Student.objects.filter(semester=query)
        context = {"students": search_students, "form": search_form}
        return render(
            request,
            "transports/manage_transport_member.html",
            context)

    context = {"students": students, "form": search_form, "status": True}
    return render(request, "transports/manage_transport_member.html", context)
