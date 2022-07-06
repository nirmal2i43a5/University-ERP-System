from django.shortcuts import get_object_or_404
from datetime import datetime
from student_management_app.models import  Semester
from school_apps.academic.models import (Syllabus, Routine, Assignment, Grade,Enotes)
from school_apps.academic import forms
from django.urls import resolve
from student_management_app.models import (Section,Semester,Subject)
from django.contrib.auth.decorators import permission_required

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
    syllabus_search_form = forms.SubjectWiseFilter(semester_id)
    semester_instance = get_object_or_404(Semester, pk =  semester_id)
    search_syllabus = Syllabus.objects.filter(semester=semester_instance)
    
    
    subject_id = request.GET.get('subject')
    subject_instance = get_object_or_404(Subject , pk = subject_id) if subject_id else None

    if subject_instance:
        search_syllabus = Syllabus.objects.filter(semester=semester_instance,subject = subject_instance)
        return search_syllabus,syllabus_search_form 
  
    return search_syllabus,syllabus_search_form 


@permission_required('academic.view_routine', raise_exception=True)
def manage_routine(request,semester_id):

    routine_search_form = forms.SectionWiseFilter(semester_id)
    semester_instance = get_object_or_404(Semester, pk =  semester_id)
    search_routines = Routine.objects.filter(semester=semester_instance)
    
    
    section_id = request.GET.get('section')
    section_instance = get_object_or_404(Section , pk = section_id) if section_id else None

    if section_instance:
        search_routines = Routine.objects.filter(semester=semester_instance,section = section_instance)
        return search_routines,routine_search_form 
  
    return search_routines,routine_search_form 

@permission_required('academic.view_enotes', raise_exception=True)
def manage_enotes(request,semester_id):

    enote_search_form = forms.EnotesFilterForm(semester_id)
    
    
    subject_id = request.GET.get('subject')
    category = request.GET.get('category')
    subject_instance = get_object_or_404(Subject , pk = subject_id) if subject_id else None

    if subject_instance:
        search_enotes = Enotes.objects.filter(subject=subject_instance,note_category = category)
        return search_enotes,enote_search_form 
    search_enotes = None
    return search_enotes,enote_search_form 