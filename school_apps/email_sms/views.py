from django.shortcuts import render
import requests
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.contrib import messages
from django.shortcuts import  render, redirect
from django.http import JsonResponse,HttpResponse
from student_management_app.models import (Section,  ExtraUser, Student,Staff)


def student_send_bulk_email(request):
	student_bulk_email = []
	students_email = Student.objects.values_list(
		'student_user__email', flat=True)
	for email in students_email:
		student_bulk_email.append(email)

	if request.method == 'POST':
		# try:
		files = request.FILES.getlist('file')
		subject = request.POST.get('subject', None)
		message = request.POST.get('message', None)
		context = {
			'message':message,
		}
		template = get_template('bulk_email/email_message.html').render(context)
	

		email = EmailMessage(
			subject,
			template,
			'nirmalpandey27450112@gmail.com',  # sender
			student_bulk_email,  # receiver
		)

		for file in files:
			email.attach(file.name, file.read(), file.content_type)
   
		email.content_subtype = 'html'
		email.send()
		email.fail_silently = False
  
		messages.success(request, 'Message is  successfully sent.')
		return redirect('email_sms:student_send_bulk_email')
		# except:
		# 	messages.error(request, 'Failed to Sent message.')
		# 	return redirect('email_sms:send_bulk_email')

	return render(request, 'bulk_email/form.html', {'title': 'Student Message'})


def teacher_send_bulk_email(request):
	teacher_bulk_email = []
	teachers_email = Staff.objects.values_list(
		'staff_user__email', flat=True)
	for email in teachers_email:
		teacher_bulk_email.append(email)

	if request.method == 'POST':
		# try:
		files = request.FILES.getlist('file')
		subject = request.POST.get('subject', None)
		message = request.POST.get('message', None)
		context = {
			'message':message,
		}
		template = get_template('bulk_email/email_message.html').render(context)
	

		email = EmailMessage(
			subject,
			template,
			'nirmalpandey27450112@gmail.com',  # sender
			teacher_bulk_email,  # receiver
		)

		for file in files:
			email.attach(file.name, file.read(), file.content_type)
   
		email.content_subtype = 'html'
		email.send()
		email.fail_silently = False
  
		messages.success(request, 'Message is  successfully sent.')
		return redirect('email_sms:teacher_send_bulk_email')
		# except:
		# 	messages.error(request, 'Failed to Sent message.')
		# 	return redirect('email_sms:send_bulk_email')

	return render(request, 'bulk_email/form.html', {'title': 'Teacher  Message'})



def particular_user_email(request):

	if request.method == 'POST':
		# try:
		files = request.FILES.getlist('file')
		subject = request.POST.get('subject', None)
		message = request.POST.get('message', None)
		to_email = request.POST.get('email', None)
		context = {
			'message':message,
		}
		template = get_template('bulk_email/email_message.html').render(context)
	

		email = EmailMessage(
			subject,
			template,
			'nirmalpandey27450112@gmail.com',  # sender
			[to_email],  # receiver
		)

		for file in files:
			email.attach(file.name, file.read(), file.content_type)
   
		email.content_subtype = 'html'
		email.send()
		email.fail_silently = False
  
		messages.success(request, 'Message is  successfully sent.')
		return redirect('email_sms:user_send_bulk_email')
		# except:
		# 	messages.error(request, 'Failed to Sent message.')
		# 	return redirect('email_sms:send_bulk_email')

	return render(request, 'bulk_email/particular_user.html', {'title': 'User  Message'})




def send_sms(request):
	section = Section.objects.filter(course_category = request.user.adminuser.course_category)
	if request.method =='POST':
		for item in request.POST.items():
			print(item)
		return HttpResponse("ok")
	
	context = {
		'section':section
	}
	return render(request, 'sms/send_sms.html', context=context)

def send_sms_ajax(request):
	# print(list(request.GET.items()))
	section_string = request.GET['section']
	section_string = section_string.replace("[","").replace("]","").replace(","," ").replace("\"","")
	section_list = section_string.split(" ")
	sections = []
	for item in section_list:
		sections.append(Section.objects.get(pk=int(item)))
	
	students=[]

	for item in sections:
		students.append(list(item.student_set.all()))
	
	final_list = [item for sublist in students for item in sublist]
	student_list = []
	for item in final_list:
		if len(item.contact)==10:
			student_list.append(item.contact)
	
	teacher = request.GET['teacher']
	staff=request.GET['staff']
	teacher_list = []
	staff_list = []

	if teacher == 'true':
		for item in Staff.objects.all():
			if len(item.contact)==10:
				teacher_list.append(item.contact)
	
	if staff=='true':
		for item in ExtraUser.objects.all():
			if len(item.contact)==10:
				staff_list.append(item.contact)
	
	final_list = []
	for item in student_list:
		final_list.append(item)
	for item in teacher_list:
		final_list.append(item)
	for item in staff_list:
		final_list.append(item)
	
	message = request.GET['msg']

	r = requests.post(
		"http://api.sparrowsms.com/v2/login/",
		data={
			'username':'info@gci.edu.np',
			'password':'Global@123@info'
		})

	status_code = r.status_code
	response = r.text
	response_json = r.json()

	token=response_json['token']
	print(token)
	identity='GCIsms'

	sms_request = requests.post(
		"http://api.sparrowsms.com/v2/sms/",
            data={'token' : token,
                  'from'  : identity,
                  'to'    : '<comma_separated 10-digit mobile numbers>',
                  'text'  : 'SMS Message to be sent'})

	status_code = sms_request.status_code
	response = sms_request.text
	response_json = sms_request.json()

	return JsonResponse({'a':'b'})