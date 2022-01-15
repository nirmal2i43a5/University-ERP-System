import json
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from student_management_app.django_forms.forms import (
                                           AddCustomUserForm, DocumentFileForm, EditCustomUserForm,AddSystemAdminForm
                                          )
                                                                      
from student_management_app.django_forms.administrative_forms import SystemAdminForm

from student_management_app.models import (
                                        	 CourseCategory, CustomUser, AdminUser , DocumentFile
                                           )

from django.contrib.auth.models import Group, Permission
from django.contrib.auth.decorators import login_required, permission_required  



@permission_required('student_management_app.add_adminuser', raise_exception=True)
def add_admin(request):
    
    if request.method == 'POST':
        
        custom_form = AddSystemAdminForm(request.POST)
        admin_form = SystemAdminForm(request.POST, request.FILES)

        if custom_form.is_valid() and admin_form.is_valid():
            email = custom_form.cleaned_data["email"]
            user_type = custom_form.cleaned_data["user_type"]
            print(user_type,"--------------------")
            print(type(user_type),":::::::::::::::::::::;;;")
            full_name = custom_form.cleaned_data["full_name"]
            
            address = admin_form.cleaned_data["address"]
            contact = admin_form.cleaned_data['contact']
            gender = admin_form.cleaned_data['gender']
            religion = admin_form.cleaned_data['religion']
            
            date_of_birth = str(request.POST.get('dob'))
            
            if date_of_birth:
                dob =  datetime.datetime.strptime(date_of_birth, "%Y-%m-%d").date()
            else:
                dob = None
            joining_date = str(request.POST.get('join_date'))
            
            if joining_date:
                join_date =  datetime.datetime.strptime(joining_date, "%Y-%m-%d").date()
            else:
                join_date = None
            
            if request.FILES.get('image'):
                image_url = request.FILES['image']
            else:
                image_url = None

            # try:
            fname = full_name.split()[0]
            system_admin_username = fname.lower()
            role = Group.objects.get(name = user_type)
            user = CustomUser.objects.create_user( username=system_admin_username, password='password', email=email,
                    full_name = full_name,is_active = True, is_staff = True, is_superuser = True, user_type=role)
            


            if user_type == Group.objects.get(name =  'Admin'):
                user.adminuser.course_category = get_object_or_404(CourseCategory, course_name = "A-Level")
            if user_type == Group.objects.get(name =  'Bachelor-Admin'):
                user.adminuser.course_category = get_object_or_404(CourseCategory, course_name = "Bachelor")
            if user_type == Group.objects.get(name =  'Master-Admin'):
                user.adminuser.course_category = get_object_or_404(CourseCategory, course_name = "Master")
                
            if user_type == Group.objects.get(name = 'Super-Admin'):
                user.adminuser.course_category = get_object_or_404(CourseCategory, course_name = "Master")
                user.adminuser.save()
                

            user.adminuser.address = address  
            user.adminuser.contact = contact
            user.adminuser.gender = gender  
            user.adminuser.religion = religion
            user.adminuser.dob = dob 
            user.adminuser.join_date = join_date
            if image_url != None:
                user.adminuser.image = image_url

            user.save()
            print(user.adminuser.course_category,"====")
            user.groups.add(role)
            # permissions_list = Permission.objects.all()
            # role.permissions.set(permissions_list)
            messages.success(request, "Successfully Added System Admin")
            return redirect('admin_app:manage_system_admin')

            # except:
            #     messages.error(request, "Failed to Add System Admin")
            #     return redirect('admin_app:add_system_admin')
        # else:
        #     return HttpResponse("<h1>Invalid Form data</h1>")
    else:
        custom_form = AddSystemAdminForm()
        admin_form = SystemAdminForm()

    context = {
            'title':'Add Admin',
             'custom_form': custom_form,
               'admin_form': admin_form}
    return render(request, 'system_admins/add_system_admin.html', context)



@permission_required('student_management_app.view_adminuser', raise_exception=True)
def manage_system_admin(request):
    
    system_admins = AdminUser.objects.all()
    context = {'system_admins': system_admins,'title':'Manage Admin'}
    return render(request, 'system_admins/manage_system_admin.html', context)


@permission_required('student_management_app.change_adminuser', raise_exception=True)
def edit_system_admin(request, admin_id):
    admin_form_instance = get_object_or_404(AdminUser, admin_user=admin_id)
    custom_form_instance = get_object_or_404(CustomUser,pk = admin_id)
    
    if request.method == 'POST':
        admin_form = AddSystemAdminForm(request.POST, request.FILES, instance=custom_form_instance)
        custom_form = SystemAdminForm(request.POST, instance = admin_form_instance)
        
        try:
            if admin_form.is_valid() and custom_form.is_valid():
                admin_form.save()
                custom_form.save()
                messages.success(request, "Successfully Edited Admin")
                return redirect('admin_app:manage_system_admin')
            
        except:

            messages.error(request, "Failed to Update Admin")
            return redirect('admin_app:edit_system_admin')
    else:
        admin_form = AddSystemAdminForm(instance=custom_form_instance)
        custom_form = SystemAdminForm(instance = admin_form_instance)

    context = {'admin_form':admin_form, 'custom_form':custom_form,'title':'Edit Admin'}
    return render(request, 'system_admins/edit_system_admin.html', context)



@permission_required('student_management_app.delete_adminuser', raise_exception=True)
def delete_system_admin(request, admin_id):
    try:
        system_admin = get_object_or_404(AdminUser, admin_user = admin_id)#i am using custom user so i use staff_user_id instead of normal system_admin id = staff_id
        system_admin.admin_user.delete()
        messages.success(request, f'{system_admin.admin_user.username} is Deleted Successfully')
        return redirect('admin_app:manage_system_admin')
    except:
        messages.error(request, 'Failed To Delete System Admin')
        return redirect('admin_app:manage_system_admin')