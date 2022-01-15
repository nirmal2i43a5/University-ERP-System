from builtins import print
from datetime import datetime
from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from school_apps.announcement.models import Notice

from django.db.models import Count
from student_management_app.models import (
    Staff, Student, Course, Subject, CustomUser, Semester, Student,CourseCategory

)
from django.views import View
from schedule.views import FullCalendarView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from schedule.models import Calendar, Event
from school_apps.attendance.models import AttendanceReport
from django.contrib.auth.models import Group


@login_required
def index(request):
    return HttpResponse("<h1>Not Found</h1><a href = '/accounts/login'>Click here to Login</a>")


class TeacherHome(View):
    def get(self, request, *args, **kwargs):
        particular_student_assign = Student.objects.filter(
            course__staff_user=request.user.id)
        print(particular_student_assign)

        # teacher = get_object_or_404(Staff, staff_user = request.user)#for current login teacher
        particular_teacher_subjects = Subject.objects.filter(
            staff_user=request.user.id)
        # subject belongs to particular teacher and subject is fk in student.so access
        students = Student.objects.filter(course)
        particular_subject_assign = subjects.count()


class HistoryLogs(View):
    def get(self, request, *args, **kwargs):
        students = Student.objects.get(id=10).delete().history.all()
        return render(request, 'logs/index.html')


def superuser_home(request):
    return render(request, 'main_home.html')

class home(FullCalendarView, View):

    def get(self, request, *args, **kwargs):
        a_level_course_category = get_object_or_404(CourseCategory,course_name = 'A-Level')
        bachelor_course_category = get_object_or_404(CourseCategory,course_name = 'Bachelor')
        master_course_category = get_object_or_404(CourseCategory,course_name = 'Master')
        '''----------------------For Teacher Dashboard content------------------------------'''
        # here I am filtering
        subject_assign_to_particular_teacher = Subject.objects.filter(
            staff_user=request.user.id)
        class_list = []
        # for subject in subject_assign_to_particular_teacher:
        # 	semester = Semester.objects.get(id = subject.semester.id)
        # 	class_list.append(semester.id)

        student_belong_to_particulat_subject = Student.objects.filter(
            semester__in=class_list).count()
        particular_teacher_subject_assign = Subject.objects.filter(
            staff_user=request.user.id).count()  # for respective subject belonging to active teacher

    # ----------------------------------------------for optional sub and student json-------------------------------------
        data = []
        student_subject_data = []
        students = Student.objects.all()
        data_set = set(data)
        for item in data_set:
            student_subject_data.append(
                {"subject": item, "student_count": data.count(item)})
    

     
    # ------------------------------------For Student attendance chart-------------------------------------------------
        total_present = AttendanceReport.objects.filter(student__student_user=request.user.id, status='Present')\
            .values('attendance__attendance_date__month').annotate(count=Count('status'))
        total_absent_informed = AttendanceReport.objects.filter(student__student_user=request.user.id, status='Absent(Informed)')\
            .values('attendance__attendance_date__month').annotate(count=Count('status'))
        total_absent_not_informed = AttendanceReport.objects.filter(student__student_user=request.user.id, status='Absent(Not Informed)')\
            .values('attendance__attendance_date__month').annotate(count=Count('status'))
        total_late = AttendanceReport.objects.filter(student__student_user=request.user.id, status='Late')\
            .values('attendance__attendance_date__month').annotate(count=Count('status'))
        total_excused = AttendanceReport.objects.filter(student__student_user=request.user.id, status='Excused')\
            .values('attendance__attendance_date__month').annotate(count=Count('status'))

    # -------------------------------------------For active students-------------------------------------------------------------------
        nonscience_faculty,total_subjects,science_faculty,inactive_students,active_students = 0,0,0,0,0
        semester_student_dataset = []
       
        alevel_group = Group.objects.get(name = 'Admin')
        bachelor_group = Group.objects.get(name = 'Bachelor-Admin')
        master_group = Group.objects.get(name = 'Master-Admin')
        
        # if request.user.groups.filter(name=alevel_group).exists() or request.user.groups.filter(name=bachelor_group).exists() or \
        # request.user.groups.filter(name=master_group).exists():
        try:
            inactive_students = Student.objects.filter(course_category = request.user.adminuser.course_category, student_user__is_active = 0).count()
            active_students = Student.objects.filter(course_category = request.user.adminuser.course_category, student_user__is_active = 1).count()
            total_subjects = Subject.objects.filter(course_category = request.user.adminuser.course_category).count()
        except:
            try:
                categories = request.user.staff.courses.all()
                inactive_students = Student.objects.filter(course_category__in=categories, student_user__is_active = 0).count()
                inactive_students = Student.objects.filter(course_category__in=categories, student_user__is_active = 1).count()
                total_subjects = Subject.objects.filter(course_category__in = categories).count()
            except:
                s_user =Student.objects.get(student_user=request.user)
                categories = s_user.course_category
                inactive_students = Student.objects.filter(course_category = categories, student_user__is_active = 0).count()
                active_students = Student.objects.filter(course_category = categories, student_user__is_active = 1).count()
                total_subjects = Subject.objects.filter(course_category = categories).count()


        # active_students = Student.objects.filter(course_category = request.user.adminuser.course_category, student_user__is_active = 1).count()
        science_faculty = Student.objects.filter(faculty='Science').count()
        nonscience_faculty = Student.objects.filter(faculty='Non-Science').count()
        
                # ------------------------------------For bachelor bar-------------------------------------------------
                
        semester_student_dataset = []
        try:
            categories = request.user.staff.courses.all()
            for semester in Semester.objects.filter(course_category__in = categories):
                semester_instance = get_object_or_404(Semester, pk = semester.pk)
                students = semester_instance.student_set.all().count()
                semester_student_dataset.append({'semester_name':semester,'students':students})
        except:
            try:
                categories = request.user.adminuser.course_category
                for semester in Semester.objects.filter(course_category = categories):
                    semester_instance = get_object_or_404(Semester, pk = semester.pk)
                    students = semester_instance.student_set.all().count()
                    semester_student_dataset.append({'semester_name':semester,'students':students})
            except:
                s_user =Student.objects.get(student_user=request.user)
                categories = s_user.course_category
                for semester in Semester.objects.filter(course_category = categories):
                    semester_instance = get_object_or_404(Semester, pk = semester.pk)
                    students = semester_instance.student_set.all().count()
                    semester_student_dataset.append({'semester_name':semester,'students':students})
        
        
        
    



    # -------------------------------------For calendar-------------------------------------------------------------------
        # calendar_slug = get_object_or_404(Calendar, slug = 'gci')
        # events = Event.objects.values('title', 'start', 'end')
        teachers_count=0
        # try:
        #     teachers_count =  Staff.objects.filter(courses__course_name__contains=request.user.adminuser.course_category.course_name).count(),
            
        # except:
        #     categories = request.user.staff.courses.all()
        #     for item in categories:
        #         teachers_count +=  Staff.objects.filter(courses__course_name__contains=item.course_name).count()

        if request.user.groups.filter(name='Teacher').exists():
            categories = request.user.staff.courses.all()
            teachers_list=[]

            for item in categories:
                staffs = Staff.objects.filter(courses__course_name__contains=item.course_name)
                for s_item in staffs:
                    teachers_list.append(s_item)
                
            teachers_list_final = set(teachers_list)
            teachers_count = len(teachers_list_final)
        else:
            teachers_count =  Staff.objects.filter(courses__course_name__contains=request.user.adminuser.course_category.course_name).count()

        context = {

            # 'teachers_count':  Staff.objects.filter(courses__course_name__contains=request.user.adminuser.course_category.course_name).count(),
            'teachers_count' : teachers_count,  
            'courses_count': Course.objects.all().count(),
            'students_count': active_students,  # for active students,
            'inactive_students_count': inactive_students,  # for active students
            'nonscience_faculty_count': nonscience_faculty,
            'science_faculty_count': science_faculty,
            'subjects_count':total_subjects,
            'semester_student_dataset':semester_student_dataset,
            #  'particular_subject_assign':particular_subject_assign,
            'particular_student_assign': student_belong_to_particulat_subject,
            'subject_assign': particular_teacher_subject_assign,
            'students_count_chart': Student.objects.all().count(),

            # ----------------------For calendar slug akin to schedule view for fullcalendar.html----------------------------
            'events': Event.objects.filter(start__gte=datetime.today()),
            'calendar_slug': 'gci',
            # ------------------------------------------------------For Notice------------------------------------------------
            'notice': Notice.objects.filter(status=True),
            'notices': Notice.objects.all()[:4],
            'dataset': student_subject_data,
            # ------------------------------------------------------for student attendance chart----------------------------
            'total_present': total_present, 'total_absent_informed': total_absent_informed, 'total_absent_not_informed': total_absent_not_informed,
            'total_excused': total_excused, 'total_late': total_late,
            # ----------------------------------------------for -------------------------------------------------------------
             'a_level_course_category':a_level_course_category,
               'bachelor_course_category':bachelor_course_category,
               'master_course_category':master_course_category,
            # for calendar
            # 'calendar_slug':calendar_slug,'events':events

        }
        return render(request, 'admin_templates/dashboard.html', context)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


def a_level_home(request):
    a_level = request.user.adminuser
    a_level.course_category = get_object_or_404(CourseCategory, course_name = 'A-Level')
    a_level.save()
    return redirect('home')

def bachelor_home(request):
    a_level = request.user.adminuser
    a_level.course_category = get_object_or_404(CourseCategory, course_name = 'Bachelor')
    a_level.save()
    return redirect('home')

def master_home(request):
    a_level = request.user.adminuser
    a_level.course_category = get_object_or_404(CourseCategory, course_name = 'Master')
    a_level.save()
    return redirect('home')

def get_user_by_role_ajax(request):
    role = request.GET['role']
    users = CustomUser.objects.filter(user_type=role).all()
    context = {
        'users': users
    }
    return render(request, 'customusers/get_user_by_role.html', context)
