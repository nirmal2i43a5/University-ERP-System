from django.shortcuts import render,get_object_or_404
from datetime import datetime
from django.db.models import Count
from student_management_app.models import CourseCategory, Semester
from school_apps.attendance.models import (AttendanceReport)
from school_apps.academic.models import (Syllabus, Routine, Assignment, Grade)
from school_apps.academic import forms
                    
from student_management_app.models import (Section,Semester,Subject)
from django.contrib.auth.decorators import permission_required


"""Visit School Class"""

def school_class(request):
    

    '''For students chart dataset'''
    class_student_dataset = []
    course_category = get_object_or_404(CourseCategory, course_name = 'School')
    for semester in Semester.objects.filter(course_category  = course_category ):
        semester_instance = get_object_or_404(Semester, pk = semester.pk)
        students = semester_instance.student_set.all().count()
        class_student_dataset.append({'semester_name':semester,'students':students})

    '''For attendance chart dataset'''
    student_attendance_dataset = []
    course_category = get_object_or_404(CourseCategory, course_name = 'School')
    for semester in Semester.objects.filter(course_category  = course_category ):
        semester_instance = get_object_or_404(Semester, pk = semester.pk)
        present_status_count =  AttendanceReport.objects.filter(attendance__semester=semester, status='Present',
                                                                       attendance__attendance_date = datetime.today())\
                                                                      .annotate(count=Count('status')).count()
        absent_informed_status_count =  AttendanceReport.objects.filter(attendance__semester=semester, status='Absent(Informed)',
                                                                       attendance__attendance_date = datetime.today())\
                                                                      .annotate(count=Count('status')).count()
        absent_not_informed_status_count =  AttendanceReport.objects.filter(attendance__semester=semester, status='Absent(Not Informed)',
                                                                       attendance__attendance_date = datetime.today())\
                                                                      .annotate(count=Count('status')).count()
        student_attendance_dataset.append({'semester_name':semester,
                                           'present_status_count':present_status_count,
                                           'absent_informed_status_count':absent_informed_status_count,
                                           'absent_not_informed_status_count':absent_not_informed_status_count
                                           })
            
    context = {
        'title':'Class Room',
        'class_student_dataset':class_student_dataset,
        'student_attendance_dataset':student_attendance_dataset
                 }
    return render(request, 'classroom/school_classroom.html', context)



def manage_assignment(request,semester_id):
    semester_instance = get_object_or_404(Semester, pk = semester_id)
    # assignments = Assignment.objects.filter(semester = semester_instance)
    respective_teacher_assignments = Assignment.objects.filter(teacher_id=request.user.id, semester = semester_instance, draft=False)
    draft_assignments = Assignment.objects.filter(teacher_id=request.user.id,semester = semester_instance, draft=True)
    # for assignment in respective_teacher_assignments:
        
    # total_students = Student.objects.filter(section = '')
    # ------
    student = []
    assignment = []
    for submitted_assignment in Grade.objects.all():
        student.append(submitted_assignment.student_id)
        assignment.append(submitted_assignment.assignment_id)
    # for student in student:
    #     print(Student.objects.get(student_user = student).section)
    # total_students = Assignment.objects.filter(student__in=student)
    # submitted_assignment_no = CustomUser.objects.filter(Q(pk__in = student)&
    #                                                     Q()).count()
    # ---
    # graded = Grade.objects.filter(status = True).count()
    
    
    assignment_search_form = forms.ContentFilterForm(semester_id)
    # semester_id = request.GET.get('semester')
    section_id = request.GET.get('section')
    subject_id = request.GET.get('subject')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
   
    if  section_id and subject_id:
        search_assignments = Assignment.objects.filter(
                                                       section = get_object_or_404(Section, pk = section_id),
                                                       Subject = get_object_or_404(Subject, pk = subject_id),
                                                     )
        return search_assignments,draft_assignments,assignment_search_form 
    
    if subject_id:
        search_assignments = Assignment.objects.filter(
                                                       Subject = get_object_or_404(Subject, pk = subject_id),
                                                     )
        return search_assignments,draft_assignments,assignment_search_form 
    
    if start_date and end_date:
        start_data_parse = datetime.strptime(str(start_date), "%Y-%m-%d").date()
        end_data_parse = datetime.strptime(str(end_date), "%Y-%m-%d").date()
        search_assignments = Assignment.objects.filter(semester=get_object_or_404(Semester, pk = semester_id),
                                                       section = get_object_or_404(Section, pk = section_id),
                                                       Subject = get_object_or_404(Subject, pk = subject_id),
                                                        #  created_at__range=(start_data_parse, end_data_parse)
                                                       )
        return search_assignments,draft_assignments,assignment_search_form 
    search_assignments = None
    return search_assignments,draft_assignments,assignment_search_form 



@permission_required('academic.view_syllabus', raise_exception=True)
def manage_syllabus(request,semester_id):
    syllabus = Syllabus.objects.filter(semester=semester_id)
    return  syllabus


@permission_required('academic.view_routine', raise_exception=True)
def manage_routine(request,semester_id):

    routine_search_form = forms.RoutineSearchForm(semester_id)
    semester_instance = get_object_or_404(Semester, pk =  semester_id)
    search_routines = Routine.objects.filter(semester=semester_instance)
    
    
    section_id = request.GET.get('section')
    section_instance = get_object_or_404(Section , pk = section_id) if section_id else None

    if section_instance:
        search_routines = Routine.objects.filter(semester=semester_instance,section = section_instance)
        return search_routines,routine_search_form 
    
    # if semester:
    #     search_routines = Routine.objects.filter(semester=semester)
    #     return search_routines,routine_search_form 

  
    return search_routines,routine_search_form 


def classroom_contents(request,pk):
    
    school_classes = Semester.objects.filter(course_category = get_object_or_404(CourseCategory, course_name = 'School'))
    search_assignments,draft_assignments,assignment_search_form = manage_assignment(request,pk)
    syllabus = manage_syllabus(request,pk)
    search_routines,routine_search_form = manage_routine(request,pk)
    context = {
        
            'school_classes':school_classes,
            'title':'Class Room',
            
            '''-------------------Assignment context-------------------'''
            
            'assignments': search_assignments,
            'teacher_assignments': search_assignments,
            'draft_assignments': draft_assignments,
            # 'student_assignments':assignments.filter(),
            'assignment_form': assignment_search_form,
               'syllabus':syllabus,
               'search_routines':search_routines,
               'routine_form':routine_search_form
             # 'submitted_assignment_no':submitted_assignment_no,
            
      
                 } 
    return render(request, 'classroom/classroom_contents.html', context)



def plus_two_class(request):
    
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