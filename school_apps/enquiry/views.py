import requests
from email.mime import text
from django.http.response import HttpResponse,JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic.edit import UpdateView
from .forms import ApplicationUpdateForm, EnquiryForm, EnquiryUpdateForm, ApplicationForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, UpdateView
from .models import Application, Enquiry
from student_management_app.models import (
    Course, CustomUser, Subject, Staff, SessionYear, Student,
    DocumentFile, Parent, Semester
)
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import  permission_required
import datetime

# Create your views here.
#Enquiry views
@permission_required('enquiry.add_enquiry', raise_exception=True)
def enquiryform(request):
    enquiry_form = EnquiryForm
    context = {'form':enquiry_form}
    if request.method == 'GET':
        print("In If")
        return render (request, 'enquiry/enquiryform.html', context)
    else:
        enquiry_response = EnquiryForm(request.POST, request.FILES)
        print("In Else")
        if enquiry_response.is_valid():
            print("In is valid")
            enquiry_response.save()
            messages.success(request, "Your enquiry has been submitted successfully.")
            print("valid message")
        else:
            messages.error(request, "Something went wrong.")
        return HttpResponseRedirect(reverse('enquiry:enquiryform'))
    
class EnquiryListView(PermissionRequiredMixin,ListView):
    permission_required  = 'enquiry.view_enquiry'
    model = Enquiry
    context_object_name = 'enquiry'
    

class EnquiryDetailView(DetailView):
    template_name='enquiry/enquiry_detail.html'
    model=Enquiry
    context_object_name = 'enquiry'


class EnquiryUpdateView(UpdateView):
    model=Enquiry
    form_class=EnquiryUpdateForm
    template_name='enquiry/enquiry_edit.html'

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(reverse('enquiry:enquiry_list'))

def send_application_email(request, pk, email):
    enquiry_obj = Enquiry.objects.get(pk=pk)
    html_content = render_to_string('enquiry/application_form_email_template.html', {'enquiry':enquiry_obj,})
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        "Admission Form",
        text_content,
        settings.EMAIL_HOST_USER,
        [enquiry_obj.email]
    )

    email.attach_alternative(html_content, "text/html")
    email.send()
    enquiry_obj.application_sent = True
    enquiry_obj.save()

    messages.success(request, "Application form sent.")
    return HttpResponseRedirect(reverse('enquiry:enquiry_list'))


def send_entrance_info (request, pk):
    enquiry_obj = Enquiry.objects.get(pk=pk)
    date = request.POST['entrance_date']
    html_content = render_to_string('enquiry/entrance_info_email_template.html', {'enquiry':enquiry_obj,'date':date})
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        "Entrance Exam information",
        text_content,
        settings.EMAIL_HOST_USER,
        [enquiry_obj.email]
    )

    email.attach_alternative(html_content, "text/html")
    email.send()
    enquiry_obj.application_sent = True
    enquiry_obj.save()

    messages.success(request, "Application form sent.")
    return HttpResponseRedirect(reverse('enquiry:enquiry_list'))


def send_entrance_results(request, pk):
    enquiry_obj = Enquiry.objects.get(pk=pk)
    date = request.POST['entrance_date']
    html_content = render_to_string('enquiry/entrance_result_email_template.html', {'enquiry':enquiry_obj, 'date':date})
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        "Entrance Result",
        text_content,
        settings.EMAIL_HOST_USER,
        [enquiry_obj.email]
    )

    email.attach_alternative(html_content, "text/html")
    email.send()
    enquiry_obj.entrance_result_sent = True
    enquiry_obj.save()

    messages.success(request, "Entrance result sent.")
    return HttpResponseRedirect(reverse('enquiry:enquiry_list'))

def send_interview_results(request, pk):
    enquiry_obj = Enquiry.objects.get(pk=pk)
    html_content = render_to_string('enquiry/interview_result_email_template.html', {'enquiry':enquiry_obj})
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        "Interview Result",
        text_content,
        settings.EMAIL_HOST_USER,
        [enquiry_obj.email]
    )

    email.attach_alternative(html_content, "text/html")
    email.send()
    enquiry_obj.interview_result_sent = True
    enquiry_obj.save()

    messages.success(request, "Entrance result sent.")
    return HttpResponseRedirect(reverse('enquiry:enquiry_list'))

def send_confirmation_email(request, pk):
    enquiry_obj = Enquiry.objects.get(pk=pk)
    html_content = render_to_string('enquiry/confirmation_email_template.html', {'enquiry':enquiry_obj})
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        "Confirmation Email",
        text_content,
        settings.EMAIL_HOST_USER,
        [enquiry_obj.email]
    )

    email.attach_alternative(html_content, "text/html")
    email.send()
    enquiry_obj.interview_result_sent = True
    enquiry_obj.save()

    messages.success(request, "Entrance result sent.")
    return HttpResponseRedirect(reverse('enquiry:enquiry_list'))


def show_modal(request):
    enq_object = Enquiry.objects.get(pk= request.GET['id'])
    context = {'item':enq_object}
    return render  (request, 'enquiry/mail_modal_body.html', context)

def application_form(request):
    app_form = ApplicationForm
    
    if request.method=="POST":
        admission_form = ApplicationForm(request.POST, request.FILES)
        if admission_form.is_valid():
            admission_form.save()
            # API Call: send -> (name, email, category)

            # CBT: create new student(name, email, category)
            messages.success(request,"Admission form submitted.")
        else:
            messages.error(request,"Something went wrong.")
    return render(request, 'enquiry/application_form.html', {'form':app_form, 'form_check':True})

def application_form_enquiry(request, pk, email):
    enquiry_obj = Enquiry.objects.get(pk=pk, email=email)

    if Application.objects.filter(enquiry = enquiry_obj).exists():
        return render(request, 'enquiry/application_form.html', {'form_check':False})
    else:        
        app_form = ApplicationForm(initial={
            'name':enquiry_obj.name,
            'temporary_address':enquiry_obj.address,
            'home_phone':enquiry_obj.home_contact,
            'contact_no':enquiry_obj.mobile_no,
            'email':enquiry_obj.email,
            'enquiry':enquiry_obj
        })
        
        if request.method=="POST":
            admission_form = ApplicationForm(request.POST, request.FILES)
            if admission_form.is_valid():
                admission_form.save()
                enquiry_obj.status='APL'
                enquiry_obj.save()
                messages.success(request,"Admission form submitted.")
            else:
                messages.error(request,"Something went wrong.")
        return render(request, 'enquiry/application_form.html', {'form':app_form, 'form_check':True})



def enroll(request, pk):
    enq_object = Enquiry.objects.get(pk=pk)
    application_obj = Application.objects.get(email = enq_object.email)

    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Application views

class ApplicationListView(PermissionRequiredMixin, ListView):
    permission_required = 'enquiry.view_application'
    model = Application
    context_object_name = 'application'


class ApplicationDetailView(DetailView):
    template_name='enquiry/application_detail.html'
    model=Application
    context_object_name = 'application'

class ApplicationUpdateView(UpdateView):
    model=Application
    form_class=ApplicationUpdateForm
    template_name='enquiry/enquiry_edit.html'

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(reverse('enquiry:application_list'))

def show_app_modal(request):
    enq_object = Application.objects.get(pk= request.GET['id'])
    context = {'item':enq_object}
    return render  (request, 'enquiry/app_mail_modal_body.html', context)

def send_app_entrance_info (request, pk):
    enquiry_obj = Application.objects.get(pk=pk)
    date = request.POST['entrance_date']
    html_content = render_to_string('enquiry/entrance_info_email_template.html', {'enquiry':enquiry_obj,'date':date})
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        "testemail",
        text_content,
        settings.EMAIL_HOST_USER,
        [enquiry_obj.email]
    )

    email.attach_alternative(html_content, "text/html")
    email.send()
    enquiry_obj.application_sent = True
    enquiry_obj.save()

    messages.success(request, "Entrance exam info sent.")
    return HttpResponseRedirect(reverse('enquiry:application_list'))


def send_app_entrance_results(request, pk):
    enquiry_obj = Application.objects.get(pk=pk)
    date = request.POST['entrance_date']
    html_content = render_to_string('enquiry/entrance_result_email_template.html', {'enquiry':enquiry_obj, 'date':date})
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        "testemail",
        text_content,
        settings.EMAIL_HOST_USER,
        [enquiry_obj.email]
    )

    email.attach_alternative(html_content, "text/html")
    email.send()
    enquiry_obj.entrance_result_sent = True
    enquiry_obj.save()

    messages.success(request, "Entrance result sent.")
    return HttpResponseRedirect(reverse('enquiry:application_list'))

def send_app_interview_results(request, pk):
    enquiry_obj = Application.objects.get(pk=pk)
    html_content = render_to_string('enquiry/interview_result_email_template.html', {'enquiry':enquiry_obj})
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        "testemail",
        text_content,
        settings.EMAIL_HOST_USER,
        [enquiry_obj.email]
    )

    email.attach_alternative(html_content, "text/html")
    email.send()
    enquiry_obj.interview_result_sent = True
    enquiry_obj.save()

    messages.success(request, "Entrance result sent.")
    return HttpResponseRedirect(reverse('enquiry:application_list'))

def send_app_confirmation_email(request, pk):
    enquiry_obj = Application.objects.get(pk=pk)
    html_content = render_to_string('enquiry/confirmation_email_template.html', {'enquiry':enquiry_obj})
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        "testemail",
        text_content,
        settings.EMAIL_HOST_USER,
        [enquiry_obj.email]
    )

    email.attach_alternative(html_content, "text/html")
    email.send()
    enquiry_obj.interview_result_sent = True
    enquiry_obj.save()

    messages.success(request, "Entrance result sent.")
    return HttpResponseRedirect(reverse('enquiry:application_list'))


def app_enroll(request, pk):
    application_obj = Application.objects.get(pk=pk)

    join_year = datetime.datetime.now().year
    course_id = application_obj.course.pk
    dept_id = application_obj.course.department.pk
    student_count = Student.objects.filter(join_year=join_year,
                                            bachelor_course = application_obj.course,
                                            ).count()
    
    student_username = str(join_year)+str(dept_id).zfill(2)+str(course_id).zfill(2)+str(student_count).zfill(4)

    print(student_count)

    f_name= application_obj.name.split()[0]

    parent_role = Group.objects.get(name='Parent')
    father_username = "p_" +  f_name

    Father_object = CustomUser.objects.create_user(
            username=father_username, 
            password='password', 
            user_type=parent_role, 
            full_name = application_obj.father_name
        )
        
    Father_object.parent.father_name = application_obj.father_name
    Father_object.parent.father_profession = application_obj.father_occupation
    Father_object.parent.father_office = application_obj.father_office
    Father_object.parent.father_phone = application_obj.father_phone
    Father_object.parent.father_email = application_obj.father_email
    Father_object.parent.mother_name = application_obj.mother_name
    Father_object.parent.mother_profession = application_obj.mother_occupation
    Father_object.parent.mother_office = application_obj.mother_office
    Father_object.parent.mother_phone = application_obj.mother_phone 
    Father_object.parent.mother_email =application_obj.mother_email
    
    sem = Semester.objects.get(name = join_year)
    role = Group.objects.get(name = 'Student')

    customuser_object = CustomUser.objects.create_user(username = student_username,
                                                        password='password', 
                                                        email=application_obj.email,
                                                        user_type=role,
                                                        full_name=application_obj.name)

    customuser_object.student.roll_no = student_username
    print('before', customuser_object.student)
    # customuser_object.student.roll_no = roll_no
    customuser_object.student.gender = application_obj.sex
    # customuser_object.student.shift = shift
    customuser_object.student.semester = sem
    customuser_object.student.course = application_obj.course
    customuser_object.student.contact = application_obj.contact_no
    customuser_object.student.permanent_address = application_obj.permanent_address
    customuser_object.student.temporary_address = application_obj.temporary_address
    customuser_object.student.dob = application_obj.dob
    customuser_object.student.guardian = Father_object.parent
    customuser_object.student.join_year = join_year
    customuser_object.save()
    print('after', customuser_object.student,'\n')
    customuser_object.student.save()
    customuser_object.groups.add(role)

    messages.success(request,"Student enrolled")    
    return redirect('admin_app:manage_student')
    # return HttpResponse(str(student_count) + " " + str(application_obj.course))


def enquiry_students_api(request):
    students = Application.objects.all().values()
    return JsonResponse(list(students),safe=False)


def enquiry_api_test(request):
    url = 'https://mis.gci.edu.np/enquiry/enquiry_students/api/'
    datas = requests.get(url).json()
    student_emails = []
    for data in datas:
        student_emails.append(data['student_user_id'])
    print(student_emails)   
    pass
    # for i in range(0,2):
    
    #     r = requests.get(url).json()
    
    #     corona_datas = {
    #                 'country_name':r['countries_stat'][i]['country_name'],
    #                 'total_cases':r['countries_stat'][i]['cases'],
                   
    #         }
        
    
    # context = {
       
               
    #            }
    # return render(request,'covid19.html',context)
    
    
   
