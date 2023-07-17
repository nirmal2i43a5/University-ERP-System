from django.shortcuts import render, redirect
from django.contrib import messages
from school_apps.announcement.forms import HolidayForm, NoticeForm
from student_management_app.models import Complain, CertificateTemplate


def complain_log(request):
    complains_logs = Complain.history.all()
    context = {
        "title": "Complain Log",
        "complains_logs": complains_logs,
    }
    return render(
        request, "administrator/loghistory/individuals/complain.html", context
    )


def delete_complain_log(request):
    Complain.history.all().delete()
    messages.success(request, "Complain logs are deleted successfully.")
    return redirect("administrator:complain_log")


def certificate_log(request):
    certificates_logs = CertificateTemplate.history.all()

    context = {
        "title": "Certificate Log",
        "certificates_logs": certificates_logs,
    }
    return render(
        request,
        "administrator/loghistory/individuals/certificate.html",
        context)


def delete_certificate_log(request):
    CertificateTemplate.history.all().delete()
    messages.success(request, "Certificate logs are deleted successfully.")
    return redirect("announcement:certificate_log")


def all_administrator_log(request):
    complains_logs = Complain.history.all()
    certificates_logs = CertificateTemplate.history.all()
    context = {
        "title": "Event Log",
        "complains_logs": complains_logs,
        "certificates_logs": certificates_logs,
    }
    return render(request, "administrator/loghistory/allhistory.html", context)


def delete_all_log(request):
    Event.history.all().delete()
    CertificateTemplate.history.all().delete()
    messages.success(request, "Announcement logs are deleted successfully.")
    return redirect("announcement:event_log")
