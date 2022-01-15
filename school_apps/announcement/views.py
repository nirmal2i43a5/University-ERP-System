
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.http import HttpResponse
from school_apps.announcement.forms import HolidayForm, NoticeForm
from school_apps.announcement.models import (
                            Holiday, Notice
                                             
                                           )
from django.contrib.auth.decorators import login_required, permission_required  
from school_apps.notifications.utilities import create_notification
from schedule.models import Event

@permission_required('announcement.add_holiday', raise_exception=True)
def add_holiday(request):
    if request.method == 'POST':
        form = HolidayForm(request.POST, request.FILES)
        try:     
            if form.is_valid():
                form.save()
                messages.success(request, "Holiday is Added Successfully.")
                return redirect('admin_app:manage_holiday')
        except:
            messages.error(request, "Failed to Add Holiday.")
            return redirect('admin_app:add_holiday')
            
    else:
        form = HolidayForm()
   
    context = {'form':form}
    return render(request, "announcements/holidays/add_holiday.html", context)


@permission_required('announcement.change_holiday', raise_exception=True)
def edit_holiday(request, holiday_id):
    holiday_instance = get_object_or_404(Holiday, id = holiday_id)
    if request.method == 'POST':
        form = HolidayForm(request.POST, request.FILES, instance = holiday_instance)
   
        try:     
            if form.is_valid():
                form.save()
                messages.success(request, "Holiday is Updated Successfully.")
                return redirect('admin_app:manage_holiday')
        except:
            messages.error(request, "Failed to Updated Holiday.")
            return redirect('admin_app:edit_holiday')
            
    else:
        form = HolidayForm(instance = holiday_instance)
   
    context = {'form':form}
    return render(request, "announcements/holidays/edit_holiday.html", context)


@permission_required('announcement.view_holiday', raise_exception=True)
def manage_holiday(request):
    holidays = Holiday.objects.all()
    context = {'holidays': holidays}
    return render(request, 'announcements/holidays/manage_holiday.html', context)



@permission_required('announcement.delete_holiday', raise_exception=True)
def delete_holiday(request, holiday_id):
    try:
        holiday = get_object_or_404(Holiday, id = holiday_id)
        holiday.delete()
        messages.success(request, f' Holiday is Deleted Successfully')
        return redirect('admin_app:manage_holiday')
    except:
        messages.error(request, 'Failed To Delete Holiday')
        return redirect('admin_app:manage_holiday')



@permission_required('announcement.add_notice', raise_exception=True)
def add_notice(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES)
        try:     
            if form.is_valid():
                instance = form.save(commit = False)
                
                try:
                    #if one notice is already active then it will become inactive if i add new one
                    notice_item = get_object_or_404(Notice, status=True)
                    notice_item.status=False
                    notice_item.save()
                except:
                    instance.save()
                instance.save()
                title = form.cleaned_data['title']
                user=request.user
                create_notification(request, post=title,notification_type=1,created_by=user,type='notice')
                
                messages.success(request, "Notice is Added Successfully.")
                return redirect('admin_app:manage_notice')
        except:
            messages.error(request, "Failed to Add Notice.")
            return redirect('admin_app:add_notice')
    else:
        form = NoticeForm()
   
    context = {'form':form,'title':'Notice'}
    return render(request, "announcements/notices/add_notice.html", context)


@permission_required('announcement.change_notice', raise_exception=True)
def edit_notice(request, notice_id):
    notice_instance = get_object_or_404(Notice, id = notice_id)
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES, instance = notice_instance)
   
        try:     
            if form.is_valid():
                form.save()
                messages.success(request, "Notice is Updated Successfully.")
                return redirect('admin_app:manage_notice')
        except:
            messages.error(request, "Failed to Updated Notice.")
            return redirect('admin_app:edit_notice')
            
    else:
        form = NoticeForm(instance = notice_instance)
   
    context = {'form':form,'title':'Notice'}
    return render(request, "announcements/notices/edit_notice.html", context)


@permission_required('announcement.delete_notice', raise_exception=True)
def delete_notice(request, notice_id):
    try:
        notice = get_object_or_404(Notice, id = notice_id)
        notice.delete()
        messages.success(request, f' Notice is Deleted Successfully')
        return redirect('admin_app:manage_notice')
    except:
        messages.error(request, 'Failed To Delete Notice')
        return redirect('admin_app:manage_notice')


# @permission_required('announcement.view_notice', raise_exception=True)
def manage_notice(request):
    notices = Notice.objects.all()
    context = {'notices': notices,'title':'Manage Notice'}
    return render(request, 'announcements/notices/manage_notice.html', context)



def update_notice(request):
    if request.is_ajax():        
        id=request.GET.get('id')
        st=get_object_or_404(Notice,pk=id)
        
        if st.status == False:
            st.status=True
            # notice = get_object_or_404(Notice, status=True)
            # notice.status=False#make previous inactive
            # notice.save()
            st.save()
        else:
            st.status=False
            st.save()
            
        notice_data = Notice.objects.all()
    return render(request, 'announcements/notices/notice_list.html', {'notices':notice_data})#because of design fluctuation i am rendering to notice_list.html


