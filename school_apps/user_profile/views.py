"""this views can be access by both student and staff"""

from django.template import Context
from django.template.loader import get_template
from django.http.request import HttpRequest
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render, redirect
from school_apps.user_profile.forms import LoginForm, UserRoleForm,CustomSetPasswordForm
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import Group
from django.contrib.auth.forms import PasswordChangeForm
from student_management_app.django_forms.forms import (
	AddCustomUserForm, StaffForm, EditCustomUserForm
)
from school_apps.student.forms import StudentForm
from student_management_app.django_forms.administrative_forms import SystemAdminForm
from django.views import View
from django.contrib.auth.decorators import login_required, permission_required
from student_management_app.models import (CourseCategory, Student,Staff,CustomUser)
from school_apps.parents.forms import ParentForm

def logoutView(request):
	logout(request)
	# request.sesssion.flush
	return redirect('login')


def loginView(request):

	form = LoginForm()

	if request.method == "POST":
		username = request.POST.get("username")
		password = request.POST.get("password")
		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			group = None

			if request.user.groups.exists():
				group = request.user.groups.all()[0].name

			if group == 'Super-Admin':
				return redirect('main_home')
			elif group:
				return redirect('home')
			else:
				# i case i choose wrong role based on username and password
				messages.error(request, "Invalid User")
				return redirect('login')

		else:
			# in case of username and password error
			messages.error(request, "Invalid Login Details")
			return redirect('login')

	return render(request, 'profile/login.html', {'form': form})





@login_required
def change_other_password(request):
	user_id = request.GET.get('user_id')
	print(user_id,"=============views inside----------")
	user_id = CustomUser.objects.filter(id = user_id)
	password_reset_form = CustomSetPasswordForm(user_id)

	if request.method == 'POST':
		slug = request.POST.get('user')
		print(slug,"----------I amslg-----------------")
		user_id = CustomUser.objects.get(id = slug)
		password_reset_form = CustomSetPasswordForm(user_id, data=request.POST)

		if password_reset_form.is_valid():
			password_reset_form.save(user_id)
			update_session_auth_hash(request, password_reset_form.user)  # Important!

			messages.success(request, "Your Password is Successfully Change")
			return redirect('change_other_password')
	context =  {
     			'title':'Reset Password',
             'reset_form': password_reset_form}
	return render(request, 'user_reset_password/change_other_password.html',context)


@login_required
def user_change_password(request):
	# user_role_form = UserRoleForm()
	# username = request.GET.get('user')
	password_reset_form = SetPasswordForm(request.user)

	if request.method == 'POST':
		# i dont see instance when changing password
		# username = request.POST['user']
		password_reset_form = SetPasswordForm(request.user, data=request.POST)

		if password_reset_form.is_valid():
			password_reset_form.save()
			update_session_auth_hash(request, password_reset_form.user)  # Important!

			messages.success(request, "Your Password is Successfully Change")
			return redirect('change_password')
	context =  {
         'title':'Reset Password',
     			# 'user_role_form': user_role_form,
             'reset_form': password_reset_form}
	return render(request, 'user_reset_password/change_password.html',context)


def password_change_form(request):
	if request.method == 'POST' and 'change_pass_button' in request.POST:
    		# i dont see instance when changing password
		PassForm = PasswordChangeForm(user=request.user, data=request.POST)

		if PassForm.is_valid():
			PassForm.save()
			update_session_auth_hash(request, PassForm.user)  # Important!

			messages.success(request, "Your password is successfully updated.Now you can login with your new password.")
			return redirect('login')



# @permission_required('student_management_app.change_student', raise_exception=True)
def UpdateStudentProfile(request):

	custom_form = EditCustomUserForm(instance=request.user)
	student_form = StudentForm(instance=request.user.student)
	PassForm = PasswordChangeForm(request.user)

	if request.method == 'POST' and 'student_submit' in request.POST:
		custom_form = EditCustomUserForm(request.POST, instance=request.user)
		student_form = StudentForm(
			request.POST, request.FILES, instance=request.user.student)

		if custom_form.is_valid() and student_form.is_valid():
			custom_form.save()  # call to password set method in modelform
			student_form.save()

			messages.success(request, "Your record is successfully updated")
			return redirect('student_profile_update')

	password_change_form(request)

	return render(request, 'profile/edit_student_profile.html', {'custom_form': custom_form, 'student_form': student_form, 'PassForm': PassForm})



def UpdateParentProfile(request):
	custom_form = EditCustomUserForm(instance=request.user)
	parent_form = ParentForm(instance=request.user.parent)
	PassForm = PasswordChangeForm(request.user)

	if request.method == 'POST' and 'parent_submit' in request.POST:
		custom_form = EditCustomUserForm(request.POST, instance=request.user)
		parent_form = ParentForm(
			request.POST, request.FILES, instance=request.user.parent)

		if custom_form.is_valid() and parent_form.is_valid():
			custom_form.save()  # call to password set method in modelform
			parent_form.save()

			messages.success(request, "Your record is successfully updated")
			return redirect('parent_profile_update')

	password_change_form(request)
 
	context =  {
     		'custom_form': custom_form, 
             'parent_form': parent_form, 
             'PassForm': PassForm
             }
 
	return render(request, 'profile/edit_parent_profile.html',context)


# @permission_required('student_management_app.change_staff', raise_exception=True)
def UpdateTeacherProfile(request):

	custom_form = EditCustomUserForm(instance=request.user)
	teacher_form = StaffForm(instance=request.user.staff)
	PassForm = PasswordChangeForm(request.user)

	if request.method == 'POST' and 'teacher_submit' in request.POST:
		custom_form = EditCustomUserForm(request.POST, instance=request.user)
		teacher_form = StaffForm(
			request.POST, request.FILES, instance=request.user.staff)

		if custom_form.is_valid() and teacher_form.is_valid():
			custom_form.save()  # call to password set method in modelform
			teacher_form.save()
			messages.success(request, "Your record is successfully updated")
			return redirect('teacher_profile_update')

	password_change_form(request)

	context = {
		'custom_form': custom_form,
		'teacher_form': teacher_form,
		'PassForm': PassForm
	}
	return render(request, 'profile/edit_teacher_profile.html', context)


@permission_required('student_management_app.change_adminuser', raise_exception=True)
def UpdateAdminProfile(request):
	course_category = request.user.adminuser.course_category
	if request.user.is_superuser:
		custom_form = EditCustomUserForm(instance=request.user)
		admin_form = SystemAdminForm(instance=request.user.adminuser)
		PassForm = PasswordChangeForm(request.user)

		if request.method == 'POST':# and 'admin_submit' in request.POST:
			custom_form = EditCustomUserForm(request.POST, instance=request.user)
			admin_form = SystemAdminForm(request.POST, request.FILES, instance=request.user.adminuser)
			if custom_form.is_valid() and admin_form.is_valid():
				custom_form.save()  # call save to forms.py
				admin_instance = admin_form.save(commit = False)
    
				'''While updating admin course_cagegory is flush.So,I again assign course category after profile update'''
				admin_instance.course_category = course_category
				admin_instance.save()
    
				messages.success(request, "Your record is successfully updated")
				return redirect('admin_profile_update')


		'''For password change view check above override views'''
		password_change_form(request)

		context = {
			'custom_form': custom_form,
			'admin_form': admin_form,
			'PassForm': PassForm
		}

		return render(request, 'profile/edit_admin_profile.html', context)



	# if request.user.is_superuser and request.user.adminuser:	
	# 	print("-------I am here2")
	# 	custom_form = EditCustomUserForm(instance=request.user)
	# 	admin_form = SystemAdminForm(instance=request.user.adminuser)
	# 	PassForm = PasswordChangeForm(request.user)

	# 	if request.method == 'POST' and 'admin_submit' in request.POST:
	# 		custom_form = EditCustomUserForm(request.POST, instance=request.user)
	# 		# error with request.user.adminuser
	# 		admin_form = SystemAdminForm(request.POST, request.FILES, instance=request.user.adminuser)
	# 		if custom_form.is_valid() and admin_form.is_valid():
	# 			custom_form.save()  # call save to forms.py
	# 			admin_form.save()
	# 			messages.success(request, "Your record is successfully updated")
	# 			return redirect('login')

	# 	password_change_form(request)

	# 	context = {
	# 		'custom_form': custom_form,
	# 		'admin_form': admin_form,
	# 		'PassForm': PassForm
	# 	}

	# 	return render(request, 'profile/edit_admin_profile.html', context)


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
		return redirect('student_send_bulk_email')
		# except:
		# 	messages.error(request, 'Failed to Sent message.')
		# 	return redirect('send_bulk_email')

	return render(request, 'bulk_email/form.html', {'title': 'Student  Message'})


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
		return redirect('teacher_send_bulk_email')
		# except:
		# 	messages.error(request, 'Failed to Sent message.')
		# 	return redirect('send_bulk_email')

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
		return redirect('user_send_bulk_email')
		# except:
		# 	messages.error(request, 'Failed to Sent message.')
		# 	return redirect('send_bulk_email')

	return render(request, 'bulk_email/particular_user.html', {'title': 'User  Message'})
