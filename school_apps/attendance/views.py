import json
import datetime
from django import urls
from django.shortcuts import render,redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse,JsonResponse
from httplib2 import Http
from student_management_app.models import( Student, Semester, Section, Subject,Staff,CourseCategory,Course,
                                          ExtraUser)
from .models import Attendance, AttendanceReport
from student_management_app.models import CustomUser
from .forms import (AttendanceFormSearch,FilterMonthlyAttendance, StudentAttendanceDetailsSearch,StudentAttendanceEditDetailsSearch,AttendanceDetailsSearch,AttendanceStatusForm,AttendanceForm )
from django.views.decorators.csrf import  csrf_exempt
from django.contrib.auth.models import Group
from school_apps.academic.forms import StudentFormSearch,StudentSearch
from django.contrib.auth.decorators import login_required, permission_required


@permission_required('attendance.add_attendancereport', raise_exception=True)
def get_students(request):
    
    status_form = AttendanceStatusForm()
    form  = AttendanceFormSearch()
 
    
    if request.method == 'POST':
        form  = AttendanceFormSearch(request.POST)
        course_category_id = request.POST.get('course_category')
        course_id = request.POST.get('filter_course')
        section = request.POST.get('section')
        subject = request.POST.get('subject')
        semester_id = request.POST.get('filter_semester')
        attendance_date = request.POST.get('attendance_date')
        
        course_category_instance = get_object_or_404(CourseCategory, pk = course_category_id)
        course_instance  = Course.objects.filter(pk = course_id).first() if course_id else None   
        section_instance  = get_object_or_404(Section, pk = section) if section else None
        subject_instance  =  Subject.objects.filter(pk = subject).first() if subject else None 
        semester = get_object_or_404(Semester, pk = semester_id)
        
        if course_category_instance == get_object_or_404(CourseCategory, course_name = 'School'):
            students = Student.objects.filter(
                                            #   course_category = course_category_instance, 
                                              semester = semester,
                                              section = section_instance, 
                                              student_user__is_active = 1
                                              ).order_by('student_user__username')
         
       
       
        if course_category_instance in CourseCategory.objects.filter(course_name__in = ['Plus-Two','Bachelor','Master']):
            students = Student.objects.filter(semester = semester, 
                                              course = course_instance, 
                                              student_user__is_active = 1
                                              ).order_by('student_user__username')
            
    
            
        return render(request,'attendances/students/take_attendance.html', {
                                                                            'form':form,
                                                                            'students':students,
                                                                            'semester':semester,
                                                                            'section':section_instance,
                                                                            'course':course_instance,
                                                                            'course_category':course_category_instance,
                                                                            'subject':subject_instance,
                                                                            'today_date':datetime.date.today,
                                                                                   # 'attendance_instances':zip(attendance_instances,student_attendance)
                                                                            # 'student_attendance':student_attendance
                                                                            })
    return render(request,'attendances/students/take_attendance.html', {
                                                                        'form':form,
                                                                        'today_date':datetime.date.today
                                                                        })



@csrf_exempt
def save_student_attendance(request):
    
    course_category_id = request.POST.get('course_category_id')
    course_category_instance = get_object_or_404(CourseCategory, pk = course_category_id)
    attendance_object = str(request.POST.get('attendance_date'))
    attendance_date = datetime.datetime.strptime(attendance_object, "%Y-%m-%d").date() 
    semester_id = request.POST.get('semester_id')
    semester = Semester.objects.get(pk=semester_id)
    section = request.POST.get('section_id')
    section_instance  = get_object_or_404(Section, pk = section) if section else None
    student_ids = request.POST.get('student_ids')
    json_student=json.loads(student_ids)
    subject = request.POST.get('subject_id')
    
    
    if course_category_instance in CourseCategory.objects.filter(course_name__in = ['School','Plus-Two']):
        
        attendance_instance = Attendance.objects.filter(semester=semester,
                                                      
                                                        section = section_instance,
                                                        attendance_date=attendance_date)
        today_date = datetime.datetime.today().strftime('%Y-%m-%d')
        if attendance_date.strftime('%Y-%m-%d') < today_date or attendance_date.strftime('%Y-%m-%d') > today_date:
            return JsonResponse({'status': 'False Date Select', 'message': 'Sorry, You cannot take attendance for past and future date.'}, safe=False)

            # print("Please choose today date")
        if attendance_instance.exists():
            return JsonResponse({'status': 'Attendance Already Exists', 'message': 'Attendance is already created for this date.Please select another date. Please select today date.'}, safe=False)
        else:
            attendance=Attendance(semester=semester,  section = section_instance, attendance_date=attendance_date)
            attendance.save()

            for stud in json_student:#FETCH EACH STUDENT AND ASSIGN DATA FOT THEM 
                student=Student.objects.get(student_user=stud['id'])
                attendance_report=AttendanceReport(student = student, attendance = attendance, status=stud['status'])   
                attendance_report.save()
        return JsonResponse({'status': 'Save Success', 'message': 'Attendance is successfully saved.'}, safe=False)

            
            
    if course_category_instance in CourseCategory.objects.filter(course_name__in = ['Bachelor','Master']):
        
           
        section = Section.objects.get(pk=section)
        subject = Subject.objects.get(pk=subject)
            # print(attendance_date,"::::::::------------------------------------::::::::::::;;")
            
        attendance_instance = Attendance.objects.filter(semester=semester,
                                                        section=section, 
                                                        subject=subject, 
                                                        attendance_date=attendance_date)
        if attendance_date.strftime('%Y-%m-%d') < datetime.datetime.today().strftime('%Y-%m-%d') or attendance_date.strftime('%Y-%m-%d') > datetime.datetime.today().strftime('%Y-%m-%d'):
            return JsonResponse({'status': 'False Date Select', 'message': 'Sorry, You cannot take attendance for past and future date.'}, safe=False)

            # print("Please choose today date")
        if attendance_instance.exists():
            return JsonResponse({'status': 'Attendance Already Exists', 'message': 'Attendance is already created for this date.Please select another date. Please select today date.'}, safe=False)
        else:
            attendance = Attendance(
                                        semester=semester,
                                        section=section, 
                                        subject=subject, 
                                        attendance_date=attendance_date
                                )
            attendance.save()
            for stud in json_student:
                student=Student.objects.get(student_user=stud['id'])
                attendance_report=AttendanceReport(student = student, attendance = attendance, status=stud['status'])   
                attendance_report.save()
                print("Attendance is successfully saved.")
            return JsonResponse({'status': 'Save Success', 'message': 'Attendance is successfully saved.'}, safe=False)
  
    

@permission_required('attendance.change_attendancereport', raise_exception=True)
def edit_student_attendance(request):
    
    form  = AttendanceForm()
    
    if request.method == 'POST':

        form  = AttendanceForm(request.POST)
        semester_id = request.POST.get('filter_semester')
        course_category_id = request.POST.get('course_category')
        course_id = request.POST.get('filter_course')
        section = request.POST.get('section')
        subject = request.POST.get('subject')
        attendance_date_object = request.POST.get('attendance_date')
        attendance_date = datetime.datetime.strptime(attendance_date_object, "%Y-%m-%d").date() 
        semester = get_object_or_404(Semester, pk = semester_id)
       
        course_category_instance = get_object_or_404(CourseCategory, pk = course_category_id)
        course_instance  = Course.objects.filter(pk = course_id).first() if course_id else None   
        section_instance  = get_object_or_404(Section, pk = section) if section else None
        subject_instance  =  Subject.objects.filter(pk = subject).first() if subject else None 
        semester = get_object_or_404(Semester, pk = semester_id)
        # attendance = Attendance.objects.filter( attendance_date = attendance_date,
        #                                     #    subject=subject_id 
        #                                     faculty = group
        #                                        )
        
        if course_category_instance == get_object_or_404(CourseCategory, course_name = 'School'):
            students = Student.objects.filter(
                                            #   course_category = course_category_instance, 
                                              semester = semester,
                                              section = section_instance, 
                                              student_user__is_active = 1
                                              ).order_by('student_user__username')
       
            attendance_instances = AttendanceReport.objects.filter(attendance__attendance_date = attendance_date,
                                                                   attendance__section = section_instance ,
                                                                   attendance__subject = subject_instance
                                                                   )
        if course_category_instance in CourseCategory.objects.filter(course_name__in = ['Plus-Two','Bachelor','Master']):
            students = Student.objects.filter(semester = semester, 
                                              course = course_instance, 
                                              student_user__is_active = 1
                                              ).order_by('student_user__username')
            attendance_instances = AttendanceReport.objects.filter(attendance__attendance_date = attendance_date,
                                                                   attendance__section = section ,
                                                                   attendance__subject = subject_instance
                                                                   )
            
        return render(request,'attendances/students/edit_attendance.html', {
                                                                            'form':form,
                                                                            'students':students,
                                                                            'semester':semester,
                                                                            'section':section_instance,
                                                                            'course':course_instance,
                                                                                'attendance_instances':attendance_instances,
                                                                            'course_category':course_category_instance,
                                                                            'subject':subject_instance,
                                                                            'today_date':datetime.date.today,
                                                                            # 'status_form':status_form
                                                                            })
     
    return render(request,'attendances/students/edit_attendance.html', {'form':form})




@csrf_exempt
def edit_save_student_attendance(request):
    attendance_date_object = request.POST.get('attendance_date')
    attendance_date = datetime.datetime.strptime(attendance_date_object, "%Y-%m-%d").date() 
    
    student_ids = request.POST.get('student_ids')
    semester_id = request.POST.get('semester_id')
    course_category_id = request.POST.get('course_category_id')
    semester = Semester.objects.get(pk=semester_id)
    course_category_instance = get_object_or_404(CourseCategory, pk = course_category_id)
    section = request.POST.get('section_id')
    subject = request.POST.get('subject_id')
    subject_instance  =  Subject.objects.filter(pk = subject).first() if subject else None 
    section_instance  =  Section.objects.filter(pk = section).first() if section else None 
    json_student=json.loads(student_ids)
    
    if course_category_instance in CourseCategory.objects.filter(course_name__in = ['Plus-Two','Bachelor','Master']):
        
        attendance=Attendance(semester=semester,
                            section=section_instance, 
                            subject=subject_instance, 
                            attendance_date=attendance_date)
        attendance.save()
        for stud in json_student:#FETCH EACH STUDENT AND ASSIGN DATA FOT THEM 
            student=Student.objects.get(student_user=stud['id'])
            each_attendance_report = get_object_or_404(AttendanceReport, pk = stud['attendance_report_id'])
            each_attendance_report.status = stud['status']
            each_attendance_report.save()
        return HttpResponse(True)
      
    
    
    if course_category_instance == get_object_or_404(CourseCategory, course_name = 'School'):
        attendance=Attendance(semester=semester,
                                section = section_instance,
                            attendance_date=attendance_date)
        attendance.save()
        for stud in json_student:
            print(stud,"Inside json data:::------------")
            student=Student.objects.get(student_user=stud['id'])
            each_attendance_report = get_object_or_404(AttendanceReport, pk = stud['attendance_report_id'])
            each_attendance_report.status = stud['status']
            each_attendance_report.save()
        return HttpResponse(True)



def student_attendance_report(request):
    context  ={
        'title':'Attendance report'
    }
    return render(request,'attendances/students/attendance_report.html', context)



def student_daily_attendance(request):
    
    datewise_attendance_form = AttendanceForm()
    if request.method == 'POST':
        # attendance_details_search = AttendanceForm(request.POST, user = request.user)
        course_category_id = request.POST.get('course_category')
        course_category_instance = get_object_or_404(CourseCategory, pk = course_category_id)
        course_id = request.POST.get('filter_course')
        course_instance  = get_object_or_404(Course, pk = course_id) if course_id else None
        attendance_details_search = AttendanceForm(request.POST)
        attendance_date = request.POST.get('attendance_date')
        semester_id = request.POST.get('filter_semester')
        semester = get_object_or_404(Semester , pk = semester_id)
        section = request.POST.get('section')
        section_instance  = get_object_or_404(Section, pk = section) if section else None
        subject_id = request.POST.get('subject')
        subject_instance = Subject.objects.filter(pk = subject_id).first() if subject_id else None 
        
        # if section !='' and subject !='':
        if course_category_instance in CourseCategory.objects.filter(course_name__in = ['Bachelor','Master']):
            attendance = Attendance.objects.filter(
                                attendance_date = attendance_date,
                                semester = semester_id,
                                section = section_instance,
                                subject = subject_instance
            )
            student_attendances = AttendanceReport.objects.filter(attendance__in = attendance)
            
        if course_category_instance in CourseCategory.objects.filter(course_name__in = ['School','Puls-Two']):
            
            course_category_id = request.POST.get('course_category')
            course_category = get_object_or_404(CourseCategory, pk = course_category_id)
            attendance = Attendance.objects.filter(
                                            attendance_date = attendance_date,
                                            semester = semester,
                                            section = section_instance,
                                            # faculty = group,
                                            # section = section_id,
                                            # subject = subject_id
                )
      
            
            student_attendances = AttendanceReport.objects.filter(attendance__in = attendance)

        
        context  ={
            'student_attendances':student_attendances,
            'title':'Datewise attendance',
            'course_category':course_category_instance,'course':course_instance,
            'semester':semester,'section':section_instance,'subject':subject_instance,
            'datewise_attendance_form':AttendanceForm(initial = {
                
                'course_category':course_category_instance,
                'filter_course':course_instance, 'filter_semester':semester, 'section':section_instance,
                'subject':subject_instance
            })
        }
        return render(request,'attendances/students/datewise_attendance.html', context)
    
    context  ={
            'title':'Datewise attendance',
            'datewise_attendance_form':datewise_attendance_form
        }
    
    return render(request,'attendances/students/datewise_attendance.html', context)



def student_monthly_attendance(request):
    
    monthly_filter_form = FilterMonthlyAttendance()
    
    if request.method == 'POST':
        month = request.POST.get('month')
        course_category_id = request.POST.get('course_category')
        course_category_instance = get_object_or_404(CourseCategory, pk = course_category_id)
        semester_id = request.POST.get('filter_semester')
        semester = get_object_or_404(Semester , pk = semester_id)
        course_id = request.POST.get('filter_course')
        course_instance  = get_object_or_404(Course, pk = course_id) if course_id else None
        section = request.POST.get('section')
        subject = request.POST.get('subject')
        section_instance  = get_object_or_404(Section, pk = section) if section else None
        subject_instance  =  Subject.objects.filter(pk = subject).first() if subject else None 
        
        if course_category_instance in CourseCategory.objects.filter(course_name__in = ['Bachelor','Master']):
        
            attendance = Attendance.objects.filter(
                attendance_date__month = month,
                attendance_date__year = datetime.date.today().year,
                semester = semester_id,
                section = section_instance, 
                subject = subject_instance
                )
            student_monthly_attendances = AttendanceReport.objects.filter(attendance__in = attendance).order_by('attendance__id')
            
        if course_category_instance in CourseCategory.objects.filter(course_name__in = ['School','Puls-Two']):
            
            attendance = Attendance.objects.filter(
                attendance_date__month = month,
                attendance_date__year = datetime.date.today().year,
                semester = semester,
                )
      
            
            student_monthly_attendances = AttendanceReport.objects.filter(attendance__in = attendance).order_by('attendance__id')
            
        context =  { 'student_monthly_attendances':student_monthly_attendances,
                    'attendance_details_form_search':AttendanceForm(),
                    'course_category':course_category_instance,'course':course_instance,
              'semester':semester,'section':section_instance,'subject':subject_instance,
                    'monthly_filter_form':FilterMonthlyAttendance(initial = {
                    'month':month,
                    'course_category':course_category_instance,
                    'filter_course':course_instance,
                    'filter_semester':semester,'section':section_instance,
                    'subject':subject_instance
                    }),
                    'semester':semester,
                    }
        
        return render(request,'attendances/students/monthly_attendance.html', context)
    

    context  ={
         'title':'Monthly attendance',
         'monthly_filter_form':monthly_filter_form
    }
    
    return render(request,'attendances/students/monthly_attendance.html', context)
    
    
       
    
def manage_student_attendance(request):
    
    # attendance_details_form_search = StudentAttendanceDetailsSearch(user = request.user)
    attendance_details_form_search = AttendanceForm()
    attendance_details_edit_form_search = StudentAttendanceEditDetailsSearch()
    monthly_filter_form = FilterMonthlyAttendance()
    
    if request.method == 'POST' and 'datewise_filter' in request.POST:
        # attendance_details_search = AttendanceForm(request.POST, user = request.user)
        attendance_details_search = AttendanceForm(request.POST)
        attendance_date = request.POST.get('attendance_date')
        semester_id = request.POST.get('filter_semester')#from hidden input
        semester = get_object_or_404(Semester , pk = semester_id)
        group = request.POST.get('group')#from hidden input
        section = request.POST.get('section')
        # section = get_object_or_404(Section , pk = section_id)
        subject = request.POST.get('subject')
        # subject = get_object_or_404(Subject , pk = subject_id)
        
        
        if section !='' and subject !='':
            course_category_id = request.POST.get('course_category')
            course_category = get_object_or_404(CourseCategory, pk = course_category_id)
            section = get_object_or_404(Section, pk = section)
            subject = get_object_or_404(Subject, pk = subject)
            attendance = Attendance.objects.filter(
                                attendance_date = attendance_date,
                                semester = semester_id,
                                faculty = group,
                                section = section,
                                subject = subject
            )
        
            student_attendances = AttendanceReport.objects.filter(attendance__in = attendance)
            
        if section == '' and subject == '':
            course_category_id = request.POST.get('course_category')
            course_category = get_object_or_404(CourseCategory, pk = course_category_id)
            attendance = Attendance.objects.filter(
                                            attendance_date = attendance_date,
                                            semester = semester,
                                            faculty = group,
                                            # section = section_id,
                                            # subject = subject_id
                )
            
            student_attendances = AttendanceReport.objects.filter(attendance__in = attendance)
            
        # monthly_attendances = AttendanceReport.objects.filter(attendance__attendance_date__month = today.month)
        
        
        
        
        context =  { 'student_attendances':student_attendances,
                    'attendance_details_form_search':AttendanceForm(initial = {
                    'attendance_date':attendance_date,'semester':semester_id,'group':group,
                        # 'section':section_id,'subject':subject_id
                    }),
                    'semester':semester,
                    'faculty':group,
                    'monthly_filter_form':monthly_filter_form,
                    # 'subject':subject,
                    # 'section':section,
                    'attendance_date':attendance_date}
        
        return render(request,'attendances/students/manage_attendance.html', context)
    
    
    
    if request.method == 'POST' and 'month_attendance_filter' in request.POST:
        month = request.POST.get('month')
        semester_id = request.POST.get('sem')
        semester = get_object_or_404(Semester , pk = semester_id)
        group = request.POST.get('alevel_group')
        
        attendance = Attendance.objects.filter(
            attendance_date__month = month,
            attendance_date__year = datetime.date.today().year,
            semester = semester_id,
            faculty = group,
            )
        
        student_monthly_attendances = AttendanceReport.objects.filter(attendance__in = attendance).order_by('attendance__id')
        
        context =  { 'student_monthly_attendances':student_monthly_attendances,
                     'attendance_details_form_search':AttendanceForm(),
                    'monthly_filter_form':FilterMonthlyAttendance(initial = {
                    'month':month,'semester':semester_id,'group':group,
                    }),
                    'semester':semester,
                    'faculty':group,
                    }
        
        return render(request,'attendances/students/manage_attendance.html', context)
    
    context = {'attendance_details_form_search':attendance_details_form_search,
               'monthly_filter_form':monthly_filter_form
               }
    return render(request,'attendances/students/manage_attendance.html', context)
    


def student_attendance_list(request):
    a_level_course_category = get_object_or_404(CourseCategory,course_name = 'A-Level')
    bachelor_course_category = get_object_or_404(CourseCategory,course_name = 'Bachelor')
    master_course_category = get_object_or_404(CourseCategory,course_name = 'Master')
    
    students = Student.objects.filter(student_user__is_active = 1,course_category = request.user.adminuser.course_category)
    
    if request.user.adminuser.course_category == a_level_course_category:
        search_form = StudentFormSearch(user = request.user)
    if request.user.adminuser.course_category in [bachelor_course_category,master_course_category]:
        search_form = StudentSearch(user = request.user)

    semester_query = request.GET.get('semester')
    section_query = request.GET.get('section')
    group_query = request.GET.get('group')

    
    if semester_query and section_query and group_query:
        search_students = Student.objects.filter(semester = semester_query, section = section_query,faculty = group_query,student_user__is_active = 1)
        context = {'students': search_students,'form':search_form}
        return render(request, 'attendances/students/student_list.html', context)
    
    elif semester_query:
        search_students = Student.objects.filter(semester = semester_query,student_user__is_active = 1)
        context = {'students': search_students,'form':search_form}
        return render(request, 'attendances/students/student_list.html', context)
    
    elif section_query:
        search_students = Student.objects.filter(section = section_query,student_user__is_active = 1)
        context = {'students': search_students,'form':search_form}
        return render(request, 'attendances/students/student_list.html', context)
    
    elif group_query:
        search_students = Student.objects.filter(faculty = group_query, student_user__is_active = 1)
        context = {'students': search_students,'form':search_form}
        return render(request, 'attendances/students/student_list.html', context)

    else:
        context = {
            'title':'Manage Student',
            'students': students,
                'form':search_form,'status':True
                }
        return render(request, 'attendances/students/student_list.html', context)

def get_teachers(request):
    teachers = Staff.objects.all()
    context = {'teachers':teachers}
    return render(request,'attendances/teachers/take_teacher_attendance.html', context)



@csrf_exempt
def save_teacher_attendance(request):
    attendance_date_object = request.POST.get('attendance_date')
    attendance_date = datetime.datetime.strptime(attendance_date_object, "%Y-%m-%d").date() 
    teacher_ids = request.POST.get('teacher_ids')
    json_teacher=json.loads(teacher_ids)
    try:
        attendance=Attendance(attendance_date=attendance_date)
        attendance.save()
        for teacher in json_teacher:
                staff=Staff.objects.get(staff_user=teacher['id'])#check or unchecked id
                attendance_report=AttendanceReport(staff = staff, attendance = attendance,status=teacher['status'])
                attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERROR")


def manage_teacher_attendance(request):
    attendance_details_form_search = AttendanceDetailsSearch()
    
    if request.method == 'POST':
        attendance_details_search = AttendanceDetailsSearch(request.POST)
        attendance_date_object = request.POST.get('attendance_date')
        attendance_date = datetime.datetime.strptime(attendance_date_object, "%Y-%m-%d").date() 
        # role = request.POST.get('role')
        attendance = Attendance.objects.filter(attendance_date = attendance_date, )
        staff = Staff.objects.filter(staff_user__user_type = Group.objects.get(name = 'Teacher'))#assigning role for teacher
        teacher_attendances = AttendanceReport.objects.filter(
            attendance__in = attendance,
            staff__in = staff#attendance for staff(teacher only)
            )
        context =  { 'teacher_attendances':teacher_attendances,
                    'attendance_details_form_search':attendance_details_form_search,
                    'attendance_date':attendance_date,
                    }
        return render(request,'attendances/teachers/manage_teacher_attendance.html', context)
    
    context = {'attendance_details_form_search':attendance_details_form_search,}
    return render(request,'attendances/teachers/manage_teacher_attendance.html', context)


def get_users(request):
    extra_users = ExtraUser.objects.all()
    context = {'extra_users':extra_users}
    return render(request,'attendances/users/take_user_attendance.html', context)



@csrf_exempt
def save_user_attendance(request):
    attendance_date_object = request.POST.get('attendance_date')
    attendance_date = datetime.datetime.strptime(attendance_date_object, "%Y-%m-%d").date() 
    user_ids = request.POST.get('user_ids')
    json_user=json.loads(user_ids)
    try:
        attendance=Attendance(attendance_date=attendance_date)
        attendance.save()
        for user in json_user:
                user=ExtraUser.objects.get(extra_user=user['id'])#check or unchecked id
                attendance_report=AttendanceReport(extra_user = user, attendance = attendance,status=user['status'])
                attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")


def manage_user_attendance(request):
    
    attendance_details_form_search = AttendanceDetailsSearch()
    if request.method == 'POST':
        attendance_details_search = AttendanceDetailsSearch(request.POST)
        attendance_date = request.POST.get('attendance_date')
        attendance = Attendance.objects.filter(attendance_date = attendance_date)
        extra_user = ExtraUser.objects.filter(
            Q(extra_user__user_type = 5) | Q(extra_user__user_type = 8)
            )#assigning for different users
       
        user_attendances = AttendanceReport.objects.filter(
            attendance__in = attendance,
            extra_user__in = extra_user#attendance for staff(teacher only)
            )
        
        context =  { 'user_attendances':user_attendances,
                    'attendance_details_form_search':attendance_details_form_search,
                    'attendance_date':attendance_date,
                        }
        
        return render(request,'attendances/users/manage_user_attendance.html', context)
    
    context =  { 
                    'attendance_details_form_search':attendance_details_form_search,
                  
                    }
    return render(request,'attendances/users/manage_user_attendance.html', context)



def fill_semester_select(request):
    course_category_id = request.GET['course_category']
    course_category = CourseCategory.objects.get(pk = course_category_id)
    semesters = Semester.objects.filter(course_category=course_category)
    context = {'semesters': semesters}
    
    return render(request, "attendances/auto_fill_select/semesters.html", context)



def fill_semester_from_course(request):
    course_id = request.GET['course']
    course = Course.objects.get(pk = course_id)
    semesters = Semester.objects.filter(course=course)
    context = {'semesters': semesters}
    return render(request, "attendances/auto_fill_select/semesters.html", context)



def fill_course_select(request):
    course_category = CourseCategory.objects.get(pk = request.GET['course_category'])
    
    courses = Course.objects.filter(course_category=course_category)
    
    if(len(courses) == 0):
        semesters = Semester.objects.filter(course_category=course_category)
        context = {'semesters': semesters}
        return render(request, "attendances/auto_fill_select/semesters.html", context)
    else:
        context = {'courses': courses}
        return render(request, "attendances/auto_fill_select/courses.html", context)

def fill_section_select(request):
    semester = Semester.objects.get(pk = request.GET['semester'])
    sections = Section.objects.filter(semester = semester)
    context = {'sections': sections}
    return render(request, "attendances/auto_fill_select/sections.html", context)
    
    
def fill_subject_select(request):
    semester = Semester.objects.get(pk = request.GET['semester'])
    # course_category = CourseCategory.objects.get(pk = request.GET['course_category'])  
    # if course_category.course_name == 'Bachelor':
    subjects = Subject.objects.filter(semester = semester)
    # if course_category.course_name == 'Master':
    #     subjects = Subject.objects.filter(course_category = course_category,master_semester = semester)
    context = {'subjects': subjects}
    return render(request, "attendances/auto_fill_select/subjects.html", context)
    

# def save_attendance(request):
#     semester_id = request.POST.get('semester_id')
#     semester = get_object_or_404(Semester, id = semester_id)
    
#     # print(semester,"semester id")
#     section = request.POST.get('section_id')
#     # section = get_object_or_404(Section, id = section)
    
#     section = semester.section_set.get(id = section )
#     print(section)
#     student = section.student_set.all()
#     print(student)
#     return HttpResponse("Reponse")
             
# def student_attendance(request):
#     search_form = AttendanceFormSearch()
#     semester = request.GET.get('semester')
#     print(semester)
#     section = request.GET.get('section')
#     print(section)
#     subject = request.GET.get('subject')
#     print(subject)
    
#     if semester and section:# and subject:
#         filter_students = Student.objects.filter(Q(semester = semester) &
#                                           Q(section= section) 
#                                         #   Q(subject= subject) 
                                          
            
#         )
#         semester = get_object_or_404(Semester, id = semester)
#         section = get_object_or_404(Section, id = section)
#         return render(request,'attendances/students/take_attendance.html', {
#                                                                             'form':search_form,
#                                                                             'students':filter_students,
#                                                                             'semester':semester,
#                                                                                  'section':section,
#                                                                             })
#     return render(request,'attendances/students/take_attendance.html', {'form':search_form})
    

# def confirm_attendance(request, semester_id):
#     semester = get_object_or_404(Semester, id=semester_id)
    
    # assc = get_object_or_404(AttendanceClass, id=ass_c_id)
    # ass = assc.assign
    # cr = ass.course
    # cl = ass.class_id
    # for i, s in enumerate(cl.student_set.all()):
    #     status = request.POST[s.USN]
        
    #     if status == 'present':
    #         status = 'True'
    #     else:
    #         status = 'False'
            
    #     if assc.status == 1:
    #         try:
    #             a = Attendance.objects.get(course=cr, student=s, date=assc.date, attendanceclass=assc)
    #             a.status = status
    #             a.save()
    #         except Attendance.DoesNotExist:
    #             a = Attendance(course=cr, student=s, status=status, date=assc.date, attendanceclass=assc)
    #             a.save()
    #     else:
    #         a = Attendance(course=cr, student=s, status=status, date=assc.date, attendanceclass=assc)
    #         a.save()
    #         assc.status = 1
    #         assc.save()

    # return HttpResponseRedirect(reverse('t_class_date', args=(ass.id,)))
    
    
