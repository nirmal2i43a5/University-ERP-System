from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages


from student_management_app.django_forms.administrative_forms import (
                                                                      CertificateTemplateForm)
from student_management_app.models import (
                                        	  Student,
                                         CertificateTemplate

                                         )

from django.views import View
from schedule.views import FullCalendarView
from django.contrib.auth.models import Group

from django.contrib.auth.decorators import  permission_required   


@permission_required('student_management_app.add_certificatetemplate', raise_exception=True)  
def add_certificate_template(request):
    form = CertificateTemplateForm()
    if request.method == 'POST':
        form = CertificateTemplateForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                print("i am valid")
                form.save()
                messages.success(request, "Successfully Added Certificate Template.")
                return redirect('admin_app:manage_certificate_template')
        except:
            messages.error(request, "Failed To  Added Certificate Template.")
            return redirect('admin_app:add_certificate_template')

    context = {'form': form,'title':'Certificate'  }
    return render(request, 'certificate_templates/add_certificate.html', context)


@permission_required('student_management_app.change_certificatetemplate', raise_exception=True)  
def edit_certificate_template(request, certificate_template_id):
    try:
        certificate_template = get_object_or_404(
            CertificateTemplate, id=certificate_template_id)
    except:
        return render(request, '404.html')

    form = CertificateTemplateForm(instance=certificate_template)
    if request.method == 'POST':
        form = CertificateTemplateForm(
            request.POST, request.FILES, instance=certificate_template)

        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Successfully Update Template.")
                return redirect('admin_app:manage_certificate_template')

        except:
            messages.error(request, "Failed To  Update Template.")
            return redirect('admin_app:edit_certificate_template', certificate_template_id)

    context = {'form': form,'title':'Certificate'   }
    return render(request, 'certificate_templates/edit_certificate.html', context)


@permission_required('student_management_app.view_certificatetemplate', raise_exception=True)  
def manage_certificate_template(request):
    certificate_templates = CertificateTemplate.objects.all()
    context = {'certificate_templates': certificate_templates,
               'title':'Manage Certificate'  
               }
    return render(request, 'certificate_templates/manage_certificate.html', context)


@permission_required('student_management_app.print_character_certificate', raise_exception=True)  
def print_character_certificate(request,certificate_id, student_id):
    certificate = get_object_or_404(CertificateTemplate, pk = certificate_id)
    student = get_object_or_404(Student, pk = student_id)
    context = {
        'title':'Character Certificate',
        'student':student,
        'certificate':certificate
    }
    return render(request, 'certificate_templates/character_certificate.html', context)


@permission_required('student_management_app.delete_certificatetemplate', raise_exception=True)  
def delete_certificate_template(request, certificate_template_id):
    try:
        # i am using custom user so i use staff_user_id instead of normal certificate_template id = staff_id
        certificate_template = get_object_or_404(
            CertificateTemplate, id=certificate_template_id)
        certificate_template.delete()
        messages.success(request, f'Template is Deleted Successfully')
        return redirect('admin_app:manage_certificate_template')
    except:
        messages.error(request, 'Failed To Delete Template')
        return redirect('admin_app:manage_certificate_template')