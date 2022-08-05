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

def assignment_handed_status(request):
    assignment_submitted_status = []

    for assignment in Assignment.objects.all():
        assignment_submitted_by_student = assignment.grade_set.all()#filter(assignment_status = 'Completed').count()
        # print(assignment_submitted_by_student)
        # for grade in assignment_grades:
        #     if grade.submitted:
        #         assignment_submitted_status.append(assignment.id)
                
        # print(grade.assignment_id)
        # grade_instance = get_object_or_404(Grade,pk = grade.pk)
        # assignment_submitted_by_student = Grade.objects.filter(
        #     Q(assignment_status = 'Completed')
        #     &Q(assignment_id = grade.assignment_id)
        #     ).count()
        # print(grade_count)
        
    
    #     assignment_submitted_by_student = Grade.objects.filter(
    #         assignment_status = 'Completed',#For submitted status by the student
    #         # assignment__semester = assignment.semester,
    #         # student__pk =  assignment.student,   
    #     #     assignment__section = assignment.section,
    #     #    assignment__Subject = assignment.Subject
    #        ).count()
    #     semester_instance = get_object_or_404(Semester, pk = assignment.semester.pk)
    #     section_instance = get_object_or_404(Section, pk = assignment.section.pk) if assignment.section else None
    #     total_students = Student.objects.filter(student_user__is_active = 1,
    #                                             semester = semester_instance, 
    #                                             section = section_instance).count()
        # assignment_reviewed_by_teacher = Grade.objects.filter(
        #     grade_status = True,
        #     assignment__semester = assignment.semester,
        #     assignment__section = assignment.section,
        #    assignment__Subject = assignment.Subject,
        #    assignment__pk = assignment.pk
        #    ).count()
    #     assignment_remained_to_check = Grade.objects.filter(
    #         grade_status = False,
    #         assignment__semester = assignment.semester,
    #         assignment__section = assignment.section,
    #        assignment__Subject = assignment.Subject
    #        ).count()
        assignment_submitted_status.append({
            # 'assignment':grade.assignment,
                                                # 'assignment_submitted_by_student':assignment_submitted_by_student,
                                            #  'assignment_reviewed_by_teacher':assignment_reviewed_by_teacher,
                                            #  'total_students':total_students,
                                            #  'assignment_remained_to_check':assignment_remained_to_check
                                             })
    print(assignment_submitted_status)
    return assignment_submitted_status



def manage_assignment(request,semester_id):
    semester_instance = get_object_or_404(Semester, pk = semester_id)
    draft_assignments = Assignment.objects.filter(teacher_id=request.user.id,semester = semester_instance, draft=True)
    assignment_submitted_status = assignment_handed_status(request)

    student = []
    assignment = []
    for submitted_assignment in Grade.objects.all():
        student.append(submitted_assignment.student_id)
        assignment.append(submitted_assignment.assignment_id)
 
  
    subject_id = request.GET.get('subject')
    subject_instance  = get_object_or_404(Subject, pk = subject_id) if subject_id else None
    section_id = request.GET.get('section')
    section_instance  = get_object_or_404(Section, pk = section_id) if section_id else None
    # teacher_id = request.GET.get('teacher')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    assignment_search_form = forms.ContentFilterForm(semester_id,initial = {
       
        'section':section_instance,'subject':subject_instance,'start_date':start_date,'end_date':end_date
    })
 

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
        return search_assignments,draft_assignments,assignment_search_form,assignment_submitted_status
    if subject_id:
        search_assignments = Assignment.objects.filter(
                                                    Subject = subject_instance,
                                                #    teacher = teacher_instance
                                                    )
        return search_assignments,draft_assignments,assignment_search_form,assignment_submitted_status
    

    search_assignments = None
    return search_assignments,draft_assignments,assignment_search_form,assignment_submitted_status



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
        
    search_enotes = None
    return search_enotes,enote_search_form 




   
 