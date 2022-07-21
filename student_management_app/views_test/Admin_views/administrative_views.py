import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import  JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from student_management_app.django_forms.forms import (
                                          SessionYearForm, AddCustomUserForm
                                          )

from student_management_app.django_forms.administrative_forms import (GroupForm, ComplainForm, SocialLinkForm,
                                                                      CertificateTemplateForm, SystemAdminForm)
from student_management_app.models import (
                                        	  Staff, SessionYear, Student, StudentGroup, Course, Subject, CustomUser,
                                           Complain, SocialLink, CertificateTemplate, AdminUser

                                         )

from django.views import View
from schedule.views import FullCalendarView
from django.contrib.auth.models import Group

from django.contrib.auth.decorators import login_required, permission_required  


@permission_required('student_management_app.add_sessionyear', raise_exception=True)   
# this view also add and manage session content
def add_manage_session_year(request):
    form = SessionYearForm()
    if request.method == 'POST':
        form = SessionYearForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Successfully Added Session Year.")
                return redirect('admin_app:add_manage_session')

                # return render(request,'admin_templates/administrator/sessions/add_session.html', context)

        except:
            messages.error(request, "Failed To  Added Session Year.")
            return redirect('admin_app:add_manage_session')

    context = {'form': form,
               'sessions': SessionYear.objects.all(),
               'title':'SessionYear'
               }
    return render(request, 'admin_templates/administrator/sessions/add_session.html', context)



@permission_required('student_management_app.change_sessionyear', raise_exception=True)   
def edit_session(request, session_id):
    try:
        session_instance = get_object_or_404(SessionYear, id=session_id)
    except:
        return render(request, '404.html')

    form = SessionYearForm(instance=session_instance)

    if request.method == 'POST':
        form = SessionYearForm(request.POST, instance=session_instance)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Successfully Edited Session Year.")
                return redirect('admin_app:add_manage_session')


        except:
            messages.error(request, "Failed To  Edit Session Year.")
            return redirect('admin_app:edit_session', session_id)

    context = {'form': form,
                  'title':'SessionYear'}
    return render(request, 'admin_templates/administrator/sessions/edit_session.html', context)


@permission_required('student_management_app.delete_sessionyear', raise_exception=True)   
def delete_session(request, session_id):
    try:
        # i am using custom user so i use staff_user_id instead of normal session id = staff_id
        session = get_object_or_404(SessionYear, id=session_id)
        session.delete()
        messages.success(request, f'Session is Deleted Successfully')
        return redirect('admin_app:add_manage_session')
    except:
        messages.error(request, 'Failed To Delete Session')
        return redirect('admin_app:add_manage_session')


@permission_required('student_management_app.view_sessionyear', raise_exception=True)   
def add_manage_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Group is Added Successfully.")
                return redirect('admin_app:add_manage_group')
        except:
            messages.error(request, "Failed to Add Group.")
            return redirect('admin_app:add_manage_group')
    else:
        form = GroupForm()

    groups = StudentGroup.objects.all()
    context = {'form': form, 'groups': groups}
    return render(request, 'admin_templates/administrator/students_groups/manage_group.html', context)


@permission_required('student_management_app.change_group', raise_exception=True)   
def edit_group(request, group_id):
    group_instance = get_object_or_404(StudentGroup, id=group_id)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group_instance)

        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Group is Updated Successfully.")
                return redirect('admin_app:add_manage_group')
        except:
            messages.error(request, "Failed to Updated Group.")
            return redirect('admin_app:edit_group')

    else:
        form = GroupForm(instance=group_instance)

    context = {'form': form}
    return render(request, "admin_templates/administrator/students_groups/edit_group.html", context)


@permission_required('student_management_app.delete_group', raise_exception=True)  
def delete_group(request, group_id):
    try:
        group = get_object_or_404(StudentGroup, id=group_id)
        group.delete()
        messages.success(request, f' Group is Deleted Successfully')
        return redirect('admin_app:add_manage_group')
    except:
        messages.error(request, 'Failed To Delete Group ')
        return redirect('admin_app:add_manage_group')


@permission_required('student_management_app.add_complain', raise_exception=True)  
def add_complain(request):
    form = ComplainForm()
    if request.method == 'POST':
        form = ComplainForm(request.POST, request.FILES)
        
        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Successfully Added Complain.")
                return redirect('admin_app:manage_complain')
        except:
            messages.error(request, "Failed To  Added Complain.")
            return redirect('admin_app:add_complain')

    context = {'form': form,
               'title':'Complain'}
    return render(request, 'admin_templates/administrator/complains/add_complain.html', context)


# this code can be use for all other field that is based on user_role and user
@csrf_exempt
def user_role(request):#from add_complain and other field
    role = request.POST.get('role')
    # filter all user based on role
    user = CustomUser.objects.filter(user_type=role).values()
    user_data = list(user)
    return JsonResponse(user_data, safe=False)


@permission_required('student_management_app.view_complain', raise_exception=True)  
def manage_complain(request):
    complains = Complain.objects.all()
    context = {'complains': complains,  'title':'Manage Complain'}
    return render(request, 'admin_templates/administrator/complains/manage_complain.html', context)


@permission_required('student_management_app.change_complain', raise_exception=True)  
def edit_complain(request, complain_id):
    try:
        complain = get_object_or_404(Complain, id=complain_id)
    except:
        return render(request, '404.html')

    form = ComplainForm(instance=complain)
    if request.method == 'POST':
        form = ComplainForm(request.POST, request.FILES, instance=complain)

        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Successfully Update Complain.")
                return redirect('admin_app:manage_complain')

        except:
            messages.error(request, "Failed To  Update Complain.")
            return redirect('admin_app:edit_complain', complain_id)

    context = {'form': form,  'title':'Complain' }
    return render(request, 'admin_templates/administrator/complains/edit_complain.html', context)


@permission_required('student_management_app.delete_complain', raise_exception=True)  
def delete_complain(request, complain_id):
    try:
        # i am using custom user so i use staff_user_id instead of normal complain id = staff_id
        complain = get_object_or_404(Complain, id=complain_id)
        complain.delete()
        messages.success(request, f'Complain is Deleted Successfully')
        return redirect('admin_app:manage_complain')
    except:
        messages.error(request, 'Failed To Delete Complain')
        return redirect('admin_app:manage_complain')



@permission_required('student_management_app.add_sociallink', raise_exception=True)  
def add_sociallink(request):
    form = SocialLinkForm()
    if request.method == 'POST':
        form = SocialLinkForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Successfully Added SocialLink.")
                return redirect('admin_app:manage_sociallink')
        except:
            messages.error(request, "Failed To  Added SocialLink.")
            return redirect('admin_app:add_sociallink')

    context = {'form': form,'title':'Sociallink' }
    return render(request, 'admin_templates/administrator/social_links/add_sociallink.html', context)

@permission_required('student_management_app.change_sociallink', raise_exception=True)  
def edit_sociallink(request, sociallink_id):
    try:
        sociallink = get_object_or_404(SocialLink, id=sociallink_id)
    except:
        return render(request, '404.html')

    form = SocialLinkForm(instance=sociallink)
    if request.method == 'POST':
        form = SocialLinkForm(request.POST, instance=sociallink)

        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Successfully Update Sociallink.")
                return redirect('admin_app:manage_sociallink')

        except:
            messages.error(request, "Failed To  Update Sociallink.")
            return redirect('admin_app:edit_sociallink', sociallink_id)

    context = {'form': form,'title':'Sociallink'  }
    return render(request, 'admin_templates/administrator/social_links/edit_sociallink.html', context)



@permission_required('student_management_app.view_sociallink', raise_exception=True)  
def manage_sociallink(request):
    sociallinks = SocialLink.objects.all()
    context = {'sociallinks': sociallinks,'title':'Manage Sociallink' }
    return render(request, 'admin_templates/administrator/social_links/manage_sociallink.html', context)


@permission_required('student_management_app.delete_sociallink', raise_exception=True)  
def delete_sociallink(request, sociallink_id):
    try:
        # i am using custom user so i use staff_user_id instead of normal sociallink id = staff_id
        sociallink = get_object_or_404(SocialLink, id=sociallink_id)
        sociallink.delete()
        messages.success(request, f'Sociallink is Deleted Successfully')
        return redirect('admin_app:manage_sociallink')
    except:
        messages.error(request, 'Failed To Delete Sociallink')
        return redirect('admin_app:manage_sociallink')



