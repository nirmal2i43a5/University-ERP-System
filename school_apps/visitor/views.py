from email.mime import text
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic.edit import UpdateView
from .forms import VisitorForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, UpdateView
from .models import Visitor
from student_management_app.models import (
    Course,
    CustomUser,
    Subject,
    Staff,
    SessionYear,
    Student,
    DocumentFile,
    Parent,
    Semester,
)
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required


@permission_required("visitor.add_visitor", raise_exception=True)
def visitorform(request):
    enquiry_form = VisitorForm
    context = {"form": enquiry_form}
    if request.method == "GET":
        return render(request, "visitor/visitorform.html", context)
    else:
        enquiry_response = VisitorForm(request.POST)
        if enquiry_response.is_valid():
            print("In is valid")
            enquiry_response.save()
            messages.success(request, "Visitor details recorded.")
            print("valid message")
        else:
            messages.error(request, "Something went wrong.")
        return HttpResponseRedirect(reverse("visitor:visitorform"))


class VisitorListView(PermissionRequiredMixin, ListView):
    permission_required = "visitor.view_visitor"
    model = Visitor
    context_object_name = "visitor"


class VisitorDetailView(PermissionRequiredMixin, DetailView):
    template_name = "visitor/visitor_detail.html"
    model = Visitor
    context_object_name = "visitor"


def printform(request, pk):
    try:
        selected_visitor = Visitor.objects.get(pk=pk)
    except BaseException:
        return HttpResponseRedirect(reverse("visitor:visitorform"))

    return render(request, "visitor/printform.html",
                  {"visitor": selected_visitor})
