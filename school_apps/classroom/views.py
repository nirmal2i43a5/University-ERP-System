from django.shortcuts import render,get_object_or_404
from datetime import datetime
from django.db.models import Count
from student_management_app.models import CourseCategory, Semester,Course
from school_apps.attendance.models import (AttendanceReport)
from school_apps.academic.models import (Syllabus, Routine, Assignment, Grade,Enotes)
from school_apps.academic import forms
from django.urls import resolve
from student_management_app.models import (Section,Semester,Subject,Student,Staff)
from django.contrib.auth.decorators import permission_required
from .helpers import (
                        manage_assignment,
                      manage_enotes,
                      manage_routine,
                      manage_syllabus
                      )


school_course_category = get_object_or_404(CourseCategory, course_name = 'School')
plus_two_course_category = get_object_or_404(CourseCategory, course_name = 'Plus-Two')
bachelor_course_category = get_object_or_404(CourseCategory, course_name = 'Bachelor')
master_course_category = get_object_or_404(CourseCategory, course_name = 'Master')

plus_two_courses = Course.objects.filter(course_category = plus_two_course_category )
bachelor_courses = Course.objects.filter(course_category = bachelor_course_category )
master_courses = Course.objects.filter(course_category = master_course_category )

school_classes = Semester.objects.filter(course_category = school_course_category)
plus_two_classes = Semester.objects.filter(course_category = plus_two_course_category)
bachelor_classes = Semester.objects.filter(course_category = bachelor_course_category)
master_classes = Semester.objects.filter(course_category = master_course_category)


"""Visit School Class"""



def attendance_chart_data(request,semester):
    semester_instance = get_object_or_404(Semester, pk = semester.pk)
    course = semester_instance.course
    present_status_count =  AttendanceReport.objects.filter(attendance__semester=semester_instance, status='Present',
                                                                attendance__attendance_date = datetime.today())\
                                                                .annotate(count=Count('status')).count()
    absent_informed_status_count =  AttendanceReport.objects.filter(attendance__semester=semester_instance, status='Absent(Informed)',
                                                                attendance__attendance_date = datetime.today())\
                                                                .annotate(count=Count('status')).count()
    absent_not_informed_status_count =  AttendanceReport.objects.filter(attendance__semester=semester_instance, status='Absent(Not Informed)',
                                                                attendance__attendance_date = datetime.today())\
                                                                .annotate(count=Count('status')).count()
    return course,present_status_count,absent_informed_status_count,absent_not_informed_status_count


def total_students_chart_data(request,semester):
    semester_instance = get_object_or_404(Semester, pk = semester.pk)
    students = semester_instance.student_set.all().count()
    course = semester_instance.course
    return course,semester_instance,students


    
def classroom(request):
    
    url_name = resolve(request.path).url_name
    school_class_list = Semester.objects.filter(course_category  = school_course_category )
    plus_two_class_list = Semester.objects.filter(course_category  = plus_two_course_category )
    bachelor_class_list = Semester.objects.filter(course_category  = bachelor_course_category )
    master_class_list = Semester.objects.filter(course_category  = master_course_category )
    student_attendance_dataset = []
    class_student_dataset = []

    '''--------------------------------------------For School Dashboard--------------------------------------------'''
    if url_name == 'school-classroom':
        '''For attendance chart data'''
        for semester in school_class_list:
            course,present_status_count,absent_informed_status_count,absent_not_informed_status_count = attendance_chart_data(request,semester)
            # Every eveery time function is called with respective semester
            student_attendance_dataset.append({'semester_name':semester,
                                               'course_name':course,
                                    'present_status_count':present_status_count,
                                    'absent_informed_status_count':absent_informed_status_count,
                                    'absent_not_informed_status_count':absent_not_informed_status_count
                                    })
    
            
        '''For total students chart data'''
        for semester in school_class_list :
            course,semester_instance,students = total_students_chart_data(request,semester)
            class_student_dataset.append({'course_name':course,'semester_name':semester_instance,'students':students})
        
        
        '''For data count'''
        active_students = Student.objects.filter(course_category = school_course_category,student_user__is_active = True)
        inactive_students = Student.objects.filter(course_category = school_course_category,student_user__is_active = False)
        teachers = Staff.objects.filter(courses = school_course_category)
        
        
    '''--------------------------------------------For Plus Two Dashboard--------------------------------------------'''
    if url_name == 'plus-two-classroom':
        '''For attendance chart data'''
        for semester in plus_two_class_list:
            course,present_status_count,absent_informed_status_count,absent_not_informed_status_count = attendance_chart_data(request,semester)
            # Every eveery time function is called with respective semester
            student_attendance_dataset.append({'semester_name':semester,
                                               'course_name':course,
                                    'present_status_count':present_status_count,
                                    'absent_informed_status_count':absent_informed_status_count,
                                    'absent_not_informed_status_count':absent_not_informed_status_count
                                    })
        
            
        '''For total students chart data'''
        for semester in plus_two_class_list :
            course,semester_instance,students = total_students_chart_data(request,semester)
            class_student_dataset.append({'course_name':course,'semester_name':semester_instance,'students':students})
        
        '''For data count'''
        active_students = Student.objects.filter(course_category = plus_two_course_category,student_user__is_active = True)
        inactive_students = Student.objects.filter(course_category = plus_two_course_category,student_user__is_active = False)
        teachers = Staff.objects.filter(courses = plus_two_course_category)
        
       
    '''--------------------------------------------For Bachelor Dashboard--------------------------------------------'''
    if url_name == 'bachelor-classroom':
        '''For attendance chart data'''
        for semester in bachelor_class_list:
            course,present_status_count,absent_informed_status_count,absent_not_informed_status_count = attendance_chart_data(request,semester)
            # Every eveery time function is called with respective semester
            
            student_attendance_dataset.append({'semester_name':semester,
                                               'course_name':course,
                                    'present_status_count':present_status_count,
                                    'absent_informed_status_count':absent_informed_status_count,
                                    'absent_not_informed_status_count':absent_not_informed_status_count
                                    })
    
            
        '''For total students chart data'''
        for semester in bachelor_class_list :
            course,semester_instance,students = total_students_chart_data(request,semester)
            class_student_dataset.append({'course_name':course,'semester_name':semester_instance,'students':students})
        
        
        '''For data count'''
        active_students = Student.objects.filter(course_category = bachelor_course_category,student_user__is_active = True)
        inactive_students = Student.objects.filter(course_category = bachelor_course_category,student_user__is_active = False)
        teachers = Staff.objects.filter(courses = bachelor_course_category)
          
    '''--------------------------------------------For Master Dashboard--------------------------------------------'''
    if url_name == 'master-classroom':
        '''For attendance chart data'''
        for semester in master_class_list:
            course,present_status_count,absent_informed_status_count,absent_not_informed_status_count = attendance_chart_data(request,semester)
            # Every eveery time function is called with respective semester
            student_attendance_dataset.append({'semester_name':semester,
                                               'course_name':course,
                                    'present_status_count':present_status_count,
                                    'absent_informed_status_count':absent_informed_status_count,
                                    'absent_not_informed_status_count':absent_not_informed_status_count
                                    })
    
            
        '''For total students chart data'''
        for semester in master_class_list :
            course,semester_instance,students = total_students_chart_data(request,semester)
            class_student_dataset.append({'course_name':course,'semester_name':semester_instance,'students':students})
        
            '''For data count'''
        active_students = Student.objects.filter(course_category = master_course_category,student_user__is_active = True)
        inactive_students = Student.objects.filter(course_category = master_course_category,student_user__is_active = False)
        teachers = Staff.objects.filter(courses = master_course_category)
            
    context = {
        'url_name':url_name,
        'title':'Class Room',
          # ---------------------------Respective classes-----------------------
        'school_classes':school_classes,
        'plus_two_classes':plus_two_classes,
        'bachelor_classes':bachelor_classes,
        'master_classes':master_classes,
          'plus_two_courses':plus_two_courses,
         'bachelor_courses':bachelor_courses,
           'plus_two_courses':plus_two_courses,
         'master_courses':master_courses,
        
        # ---------------------------Chart Data-----------------------
        'class_student_dataset':class_student_dataset,
        'student_attendance_dataset':student_attendance_dataset,
        
        # -------For details count
        'active_students_count':active_students.count(),
         'inactive_students_count':inactive_students.count(),
         'teachers_count':teachers.count(),
       
                 }
    return render(request, 'classroom/classroom.html', context)




def classroom_contents(request,pk):
    url_name = resolve(request.path).url_name
    print(url_name)
    search_assignments,draft_assignments,assignment_search_form = manage_assignment(request,pk)
    search_syllabus,syllabus_search_form  = manage_syllabus(request,pk)
    search_routines,routine_search_form = manage_routine(request,pk)
    search_enotes,enote_search_form = manage_enotes(request,pk)
    context = {
        
            'school_classes':school_classes,
             'plus_two_classes':plus_two_classes,
            'bachelor_classes':bachelor_classes,
            'master_classes':master_classes,
        
            'title':'Class Room',
            'url_name':url_name,
              'plus_two_courses':plus_two_courses,
                 'bachelor_courses':bachelor_courses,
           'plus_two_courses':plus_two_courses,
         'master_courses':master_courses,
            
            '''-------------------Assignment context-------------------'''
            
            'assignments': search_assignments,
            'teacher_assignments': search_assignments,
            'draft_assignments': draft_assignments,
            # 'student_assignments':assignments.filter(),
            'assignment_form': assignment_search_form,
               'syllabus':search_syllabus,
                 'syllabus_form':syllabus_search_form,
               'search_routines':search_routines,
               'routine_form':routine_search_form,
               'enote_search_form':enote_search_form,
               'search_enotes':search_enotes
             # 'submitted_assignment_no':submitted_assignment_no,
            
      
                 } 
    return render(request, 'classroom/classroom_contents.html', context)



def plus_two_class(request):
    school_url_name = resolve(request.path).url_name
    
    context = {
        'title':'Class Room',
        
                 }
    return render(request, 'classroom/plus_two_classroom.html', context)


def bachelor_class(request):
    
    context = {
        'title':'Class Room',
     
        
                 }
    return render(request, 'classroom/bachelor_classroom.html', context)


def master_class(request):
    
    context = {
        'title':'Class Room',
                 }
    return render(request, 'classroom/master_classroom.html', context)