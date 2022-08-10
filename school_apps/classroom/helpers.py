from django.shortcuts import get_object_or_404
from datetime import datetime,timedelta
from student_management_app.models import  Semester
from school_apps.academic.models import (Syllabus, Routine, Assignment, Grade,Enotes)
from school_apps.academic import forms
from django.urls import resolve
from student_management_app.models import (Section,Semester,Subject,Staff,CustomUser)
from django.contrib.auth.decorators import permission_required
from student_management_app.models import Student
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger



def manage_assignment(request,semester_id):
    semester_instance = get_object_or_404(Semester, pk = semester_id)
    draft_assignments = Assignment.objects.filter(teacher_id=request.user.id,semester = semester_instance, draft=True)

    student = []
    assignment = []
    for submitted_assignment in Grade.objects.all():
        student.append(submitted_assignment.student_id)
        assignment.append(submitted_assignment.assignment_id)
 
  
    subject_id = request.GET.get('subject')
    subject_instance  = get_object_or_404(Subject, pk = subject_id) if subject_id else None
    section_id = request.GET.get('section')
    section_instance  = get_object_or_404(Section, pk = section_id) if section_id else None
    teacher_id = request.GET.get('teacher')
    print(teacher_id,":::::::::::==================")
    teacher_instance  = CustomUser.objects.get(pk = teacher_id) if teacher_id else None
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    assignment_search_form = forms.ContentFilterForm(semester_id,initial = {
       
        'section':section_instance,'subject':subject_instance,'start_date':start_date,'end_date':end_date
    })
 
    if section_id and not subject_id and not teacher_id:
        search_assignments = Assignment.objects.filter(
                                                    section = section_instance,
                                                    )
    
        return search_assignments,draft_assignments,assignment_search_form
    if subject_id and start_date  and end_date:
        
        start_date_parse = datetime.strptime(str(start_date), "%Y-%m-%d").date()
        end_date_parse = datetime.strptime(str(end_date), "%Y-%m-%d").date()
    
        search_assignments = Assignment.objects.filter(
                                                    Subject = subject_instance,
                                                        created_at__range=(
                                                            start_date_parse, 
                                                            end_date_parse + timedelta(days=1)
                                                            )
                                                    )
        return search_assignments,draft_assignments,assignment_search_form
    if subject_id and not teacher_id:
        search_assignments = Assignment.objects.filter(
                                                    Subject = subject_instance,
                                                #    teacher = teacher_instance
                                                    )
    
        return search_assignments,draft_assignments,assignment_search_form
    
   
    if subject_id and teacher_id:
        print("Inside ")
        search_assignments = Assignment.objects.filter(
                                                    Subject = subject_instance,
                                                    teacher = teacher_instance
                                                    )
    
        return search_assignments,draft_assignments,assignment_search_form
        
    search_assignments = Assignment.objects.filter(
                                                    semester = semester_instance,
                                                    )
    page = request.GET.get('page', 1)
    paginator = Paginator(search_assignments, 10)
    try:    
        search_assignments = paginator.page(page)
    except PageNotAnInteger:
        search_assignments = paginator.page(10)
    except EmptyPage:
        search_assignments = paginator.page(paginator.num_pages)
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

    enote_search_form = forms.EnotesFilterForm(semester_id,request.user)
    
           
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    subject_id = request.GET.get('subject')
    category = request.GET.get('category')
    subject_instance = get_object_or_404(Subject , pk = subject_id) if subject_id else None

    if   subject_id or category or start_date or end_date :
       

        if start_date and end_date:
            start_data_parse = datetime.strptime(str(start_date), "%Y-%m-%d").date()
            end_data_parse = datetime.strptime(str(end_date), "%Y-%m-%d").date()
     
            search_enotes = Enotes.objects.filter(
                                                        subject = subject_instance,
                                                         note_category = category,
                                                         created_at__range=(start_data_parse,
                                                                            end_data_parse+ timedelta(days=1)
                                                                            )
                                                       )
        else:
            search_enotes = Enotes.objects.filter(
                                                       subject = subject_instance,
                                                       note_category = category,

                                                    #    teacher = teacher_instance
                                                       )
        enote_search_form = forms.EnotesFilterForm(semester_id,request.user,initial = {
         'subject': subject_id,'category': category,'start_date': start_date,'end_date': end_date
                                         })
    
        return search_enotes,enote_search_form 
    
    search_enotes = Enotes.objects.all()
    
    page = request.GET.get('page', 1)
    paginator = Paginator(search_enotes, 10)
    try:    
        search_enotes = paginator.page(page)
    except PageNotAnInteger:
        search_enotes = paginator.page(10)
    except EmptyPage:
        search_enotes = paginator.page(paginator.num_pages)
        
    return search_enotes,enote_search_form 




   
 