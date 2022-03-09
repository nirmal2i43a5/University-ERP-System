from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from django.http import HttpResponse
from django.db.models import Q
from student_management_app.django_forms.forms import (
    CourseForm
)
from .forms import (SubjectForm,MasterSubjectForm, BachelorSubjectForm,SemesterForm,BachelorSemesterForm,MasterSemesterForm,SectionForm,
                    SemesterSectionSearchForm,RoutineSearchForm,SyllabusSearchForm)
from school_apps.academic.forms import ClassFormSearch
from school_apps.academic.forms import (
    SyllabusForm, AssignmentForm, RoutineForm, SubjectSearchForm)
from student_management_app.models import (
    Course, CourseCategory, CustomUser, Subject,
    Semester, Section,   Department, Student
)
from school_apps.academic.models import (Syllabus, Routine, Assignment, Grade)

from django.contrib.auth.decorators import permission_required
from school_apps.notifications.utilities import create_notification
from school_apps.courses.forms import CourseCategoryeForm, CourseForm, DepartmentForm
from django.template.loader import get_template
from django.core.mail import EmailMessage

# this view is for adding and managing degree
@permission_required(['student_management_app.view_course', 'student_management_app.add_course'], raise_exception=True)
def add_manage_course(request):
    form = CourseForm()
    courses = Course.objects.all()
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Course is Added Successfully")
            return redirect('admin_app:add_manage_course')
    context = {'form': form,
               "courses": courses,
               'title': 'Course'
               }
    return render(request, "academic/courses/manage_course.html", context)



@permission_required(['student_management_app.view_course', 'student_management_app.add_course'], raise_exception=True)
def manage_coursecategory(request):
    form = CourseCategoryeForm()
    courses = CourseCategory.objects.all()
    if request.method == 'POST':
        form = CourseCategoryeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Course Category is Added Successfully")
            return redirect('academic:manage_coursecategory')
    context = {'form': form,
               "courses": courses,
               'title': 'Course Category'
               }
    return render(request, "academic/courses/manage_coursecategory.html", context)


    


@permission_required('student_management_app.change_course', raise_exception=True)
def edit_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    form = CourseForm(instance=course)
    context = {'form': form,
               'course': course,
               'title': 'Course'
               }
    return render(request, "academic/courses/edit_course.html", context)


@permission_required('student_management_app.change_course', raise_exception=True)
def save_edit_course(request):

    if request.method == 'POST':

        # i grab this id from hidden input (i can also grab this from url if i dont give hidden field)
        course_id = request.POST.get('course_id')
        course = get_object_or_404(Course, pk=course_id)

        try:
            form = CourseForm(request.POST, instance=course)
            if form.is_valid():
                form.save()
                messages.success(request, "Successfully Edited Course")
                return redirect("admin_app:add_manage_course")
        except:
            messages.error(request, "Failed To Edit Course.")
            return redirect("admin_app:add_manage_course")
    else:

        return HttpResponse("<h1>Method Not Allowed</h1>")


def add_department(request):
    form = DepartmentForm()
    departments = Department.objects.all()
    if request.method == 'POST':
        formdata = DepartmentForm(request.POST)
        if formdata.is_valid():
            formdata.save()
            messages.success(request, 'Department info added.')
            return redirect(('admin_app:add_department'))
        else:
            messages.error(
                request, "Department info invalid. Please check your information and try again.")
            return render(request, 'academic/courses/add_department.html', {'form': form})
    else:
        return render(request, 'academic/courses/add_department.html', {'form': form,'departments':departments})


def edit_department(request,pk):
    instance = get_object_or_404(Department, pk = pk)
    form = DepartmentForm(instance = instance)
    departments = Department.objects.all()
    if request.method == 'POST':
        formdata = DepartmentForm(request.POST, instance = instance)
        if formdata.is_valid():
            formdata.save()
            messages.success(request, 'Department info edited.')
            return redirect(('admin_app:add_department'))
        else:
            messages.error(
                request, "Department info invalid. Please check your information and try again.")
            return render(request, 'academic/courses/add_department.html', {'form': form})
    else:
        return render(request, 'academic/courses/add_department.html', {'form': form,'departments':departments,'instance':instance})


def delete_department(request,pk):
    instance = get_object_or_404(Department, pk = pk)
    instance.delete()
    messages.success(request, 'Department info deleted.')
    return redirect(('admin_app:add_department'))
    
   


@permission_required('student_management_app.delete_course', raise_exception=True)
def delete_course(request, course_id):
    try:
        # i am using custom user so i use staff_user_id instead of normal course id = staff_id
        course = get_object_or_404(Course, pk=course_id)
        course.delete()
        messages.success(
            request, f'Course {course.course_name} is Deleted Successfully')
        return redirect('admin_app:add_manage_course')
    except:
        messages.error(request, 'Failed To Delete course')
        return redirect('admin_app:add_manage_course')



@permission_required('student_management_app.add_subject', raise_exception=True)
def manage_subject(request):
    a_level_course_category = get_object_or_404(CourseCategory,course_name = 'A-Level')
    bachelor_course_category = get_object_or_404(CourseCategory,course_name = 'Bachelor')
    master_course_category = get_object_or_404(CourseCategory,course_name = 'Master')
    
    
    if request.user.adminuser.course_category == a_level_course_category :
        form = SubjectForm()
        if request.method == 'POST':
            form = SubjectForm(request.POST)
            try:
                if form.is_valid():
                    instance = form.save(commit = False)
                    instance.course_category = a_level_course_category
                    instance.save()
                    messages.success(request, "Subject is Added Successfully.")
                    return redirect('admin_app:manage_subject')

            except:
                messages.error(request, "Failed To Add Subject.")
                return redirect('admin_app:manage_subject')
            
    if request.user.adminuser.course_category == bachelor_course_category :
        form = BachelorSubjectForm()
        if request.method == 'POST':
            form = BachelorSubjectForm(request.POST)
            try:
                if form.is_valid():
                    instance = form.save(commit = False)
                    instance.course_category = bachelor_course_category
                    instance.save()
                    messages.success(request, "Subject is Added Successfully.")
                    return redirect('admin_app:manage_subject')

            except:
                messages.error(request, "Failed To Add Subject.")
                return redirect('admin_app:manage_subject')
            
    if request.user.adminuser.course_category == master_course_category :
        form = MasterSubjectForm()
        if request.method == 'POST':
            form = MasterSubjectForm(request.POST)
            try:
                if form.is_valid():
                    instance = form.save(commit = False)
                    instance.course_category = master_course_category
                    instance.save()
                    messages.success(request, "Subject is Added Successfully.")
                    return redirect('admin_app:manage_subject')

            except:
                messages.error(request, "Failed To Add Subject.")
                return redirect('admin_app:manage_subject')
            
    # subjects = Subject.objects.all()
    # search_form = ClassFormSearch(user = request.user)
    # query = request.GET.get('faculty')

    # if query:
    #     search_subjects = Subject.objects.filter(faculty=query)
    #     context = {'subjects': search_subjects, 'search_form': search_form}
    #     return render(request, 'academic/subjects/manage_subject.html', context)
    
    context = {'form': form,
            #    'subjects': subjects,
            #    'search_form': search_form,
               'title': 'Subject',
                'a_level_course_category':a_level_course_category,
               'bachelor_course_category':bachelor_course_category,
               'master_course_category':master_course_category,
                'a_level_subjects':Subject.objects.filter(course_category = a_level_course_category),
               'bachelor_subjects':Subject.objects.filter(course_category = bachelor_course_category),
                'master_subjects':Subject.objects.filter(course_category = master_course_category)
              
               }

    return render(request, 'academic/subjects/manage_subject.html', context)






@permission_required('student_management_app.change_subject', raise_exception=True)
def edit_subject(request, subject_id):  # keep subject_id hidden field in edit_subject.html
    subject_instance = get_object_or_404(Subject, pk=subject_id)
    form = SubjectForm(instance=subject_instance)

    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject_instance)

        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Subject is Edited Successfully.")
                return redirect('admin_app:manage_subject')

        except:
            messages.error(request, "Failed To Edit Subject.")
            return redirect('admin_app:edit_subject', subject_id)

    context = {'form': form,
               'title': 'Subject'
               }
    return render(request, 'academic/subjects/edit_subject.html', context)


@permission_required('student_management_app.delete_subject', raise_exception=True)
def delete_subject(request, subject_id):
    # try:
    subject = get_object_or_404(Subject, pk=subject_id)
    subject.delete()
    messages.success(
        request, f' {subject.subject_name} is Deleted Successfully')
    return redirect('admin_app:manage_subject')
    # except:
      # messages.error(request, 'Failed To Delete Subject')
      # return redirect('admin_app:manage_subject')


def search_subject(request):
    search_text = request.GET.get('query')

    if search_text:
        search_subjects = Subject.objects.filter(
            Q(subject_name__icontains=search_text))
        return render(request, 'subjects/manage_subject.html', {'subjects': search_subjects})
    else:
        subjects = Subject.objects.all()
        return render(request, 'subjects/manage_subject.html', {'subjects': subjects})


# this is for semester

@permission_required('student_management_app.add_semester', raise_exception=True)
@permission_required('student_management_app.view_semester', raise_exception=True)
def manage_class(request):
    
    a_level_course_category = get_object_or_404(CourseCategory,course_name = 'A-Level')
    bachelor_course_category = get_object_or_404(CourseCategory,course_name = 'Bachelor')
    master_course_category = get_object_or_404(CourseCategory,course_name = 'Master')
    
    if request.user.adminuser.course_category == a_level_course_category :
        form = SemesterForm()
        if request.method == 'POST':
            form = SemesterForm(request.POST)
            try:
                if form.is_valid():
                    instance = form.save(commit = False)
                    instance.course_category = a_level_course_category
                    instance.save()
                    messages.success(request, "Class is Added Successfully.")
                    return redirect('admin_app:manage_class')
            except:
                messages.error(request, "Failed To Add Class.")
                return redirect('admin_app:manage_class')
        
        
    if request.user.adminuser.course_category == bachelor_course_category:
        form = BachelorSemesterForm()
        if request.method == 'POST':
            form = BachelorSemesterForm(request.POST)
            print(form)
            try:
                if form.is_valid():
                    print(1)
                    instance = form.save(commit = False)
                    print(2)
                    instance.course_category = bachelor_course_category
                    print(3)
                    instance.save()
                    print(4)
                    messages.success(request, "Class is Added Successfully.")
                    return redirect('admin_app:manage_class')
            except:
                messages.error(request, "Failed To Add Class.")
                return redirect('admin_app:manage_class')
        
        
    if request.user.adminuser.course_category == master_course_category:
        form = MasterSemesterForm()
        if request.method == 'POST':
            form = MasterSemesterForm(request.POST)
            try:
                if form.is_valid():
                    instance = form.save(commit = False)
                    instance.course_category = master_course_category
                    instance.save()
                    messages.success(request, "Class is Added Successfully.")
                    return redirect('admin_app:manage_class')
            except:
                messages.error(request, "Failed To Add Class.")
                return redirect('admin_app:manage_class')
   

    context = {'form': form,
               'title': 'Class',
               'a_level_course_category':a_level_course_category,
               'bachelor_course_category':bachelor_course_category,
               'master_course_category':master_course_category,
                'a_level_classes':Semester.objects.filter(course_category = a_level_course_category),
               'bachelors_semesters':Semester.objects.filter(course_category = bachelor_course_category),
                 'masters_semesters':Semester.objects.filter(course_category = master_course_category)
               }
    return render(request, "academic/classes/manage_class.html", context)



@permission_required('student_management_app.edit_semester', raise_exception=True)
def edit_class(request, class_id):
    class_instance = get_object_or_404(Semester, pk=class_id)
    a_level_course_category = get_object_or_404(CourseCategory,course_name = 'A-Level')
    bachelor_course_category = get_object_or_404(CourseCategory,course_name = 'Bachelor')
    master_course_category = get_object_or_404(CourseCategory,course_name = 'Master')
    
    if request.user.adminuser.course_category == a_level_course_category :
        form = SemesterForm(instance = class_instance)
        if request.method == 'POST':
            form = SemesterForm(request.POST, instance = class_instance)
            try:
                if form.is_valid():
                    instance = form.save(commit = False)
                    instance.course_category = a_level_course_category
                    instance.save()
                    messages.success(request, "Class is Updated Successfully.")
                    return redirect('admin_app:manage_class')
            except:
                messages.error(request, "Failed To Add Class.")
                return redirect('admin_app:manage_class')
        
        
    if request.user.adminuser.course_category == bachelor_course_category:
        form = BachelorSemesterForm(instance = class_instance)
        if request.method == 'POST':
            form = BachelorSemesterForm(request.POST,instance = class_instance)
            try:
                if form.is_valid():
                    instance = form.save(commit = False)
                    instance.course_category = bachelor_course_category
                    instance.save()
                    messages.success(request, "Class is Updated Successfully.")
                    return redirect('admin_app:manage_class')
            except:
                messages.error(request, "Failed To Add Class.")
                return redirect('admin_app:manage_class')
        
        
    if request.user.adminuser.course_category == master_course_category:
        form = MasterSemesterForm(instance = class_instance)
        if request.method == 'POST':
            form = MasterSemesterForm(request.POST,instance = class_instance)
            try:
                if form.is_valid():
                    instance = form.save(commit = False)
                    instance.course_category = master_course_category
                    instance.save()
                    messages.success(request, "Class is Updated Successfully.")
                    return redirect('admin_app:manage_class')
            except:
                messages.error(request, "Failed To Add Class.")
                return redirect('admin_app:manage_class')
   

    context = {'form': form,
               'title': 'Class',
               'a_level_course_category':a_level_course_category,
               'bachelor_course_category':bachelor_course_category,
               'master_course_category':master_course_category,
                'a_level_classes':Semester.objects.filter(course_category = a_level_course_category),
               'bachelors_semesters':Semester.objects.filter(course_category = bachelor_course_category),
                 'masters_semesters':Semester.objects.filter(course_category = master_course_category)
               }
    return render(request, "academic/classes/manage_class.html", context)




@permission_required('student_management_app.delete_semester', raise_exception=True)
def delete_class(request, class_id):
    try:
        semester_instance = get_object_or_404(Semester, pk=class_id)
        semester_instance.delete()
        messages.success(
            request, f' Class is Deleted Successfully')
        return redirect('admin_app:manage_class')
    except:
        messages.error(request, 'Failed To Delete Semester')
        return redirect('admin_app:manage_class')


@permission_required('student_management_app.add_section', raise_exception=True)
@permission_required('student_management_app.view_section', raise_exception=True)
def manage_section(request):
    # ----------search part---
    # sections = Section.objects.all()
    # search_form = ClassFormSearch(user = request.user)
    # query = request.GET.get('semester')
    # if query:
    #     search_sections = Section.objects.filter(semester=query)
    #     context = {'sections': search_sections, 'form': search_form,
    #                 'sections': Section.objects.all(),'form':form
    #                }
    #     return render(request, 'academic/sections/manage_section.html', context)
    # -----------
    a_level_course_category = get_object_or_404(CourseCategory,course_name = 'A-Level')
    bachelor_course_category = get_object_or_404(CourseCategory,course_name = 'Bachelor')
    master_course_category = get_object_or_404(CourseCategory,course_name = 'Master')
    form = SectionForm(user = request.user)
    
    if request.user.adminuser.course_category == a_level_course_category :
        if request.method == 'POST':

            form = SectionForm(request.POST, user = request.user)
            try:
                if form.is_valid():
                    instance = form.save(commit = False)
                    instance.course_category = a_level_course_category
                    instance.save()
                    messages.success(request, "Section is added successfully.")
                    return redirect('admin_app:manage_section')
            except:
                messages.error(request, "Failed to add section.")
                return redirect('admin_app:manage_section')
      
            
    if request.user.adminuser.course_category == bachelor_course_category :
        if request.method == 'POST':
            form = SectionForm(request.POST,user = request.user)
            try:
                if form.is_valid():
                    instance = form.save(commit = False)
                    instance.course_category = bachelor_course_category
                    instance.save()
                    messages.success(request, "Section is added successfully.")
                    return redirect('admin_app:manage_section')
            except:
                messages.error(request, "Failed to add section.")
                return redirect('admin_app:manage_section')
            
            
    if request.user.adminuser.course_category == master_course_category :
        if request.method == 'POST':
            form = SectionForm(request.POST,user = request.user)
            try:
                if form.is_valid():
                    instance = form.save(commit = False)
                    instance.course_category = master_course_category
                    instance.save()
                    messages.success(request, "Section is added successfully.")
                    return redirect('admin_app:manage_section')
            except:
                messages.error(request, "Failed to add section.")
                return redirect('admin_app:manage_section')
            
    context = {'form': form,
            #    'sections': sections,
            #    'search_form': search_form,
               'sections': Section.objects.all(),
                'a_level_course_category':a_level_course_category,
               'bachelor_course_category':bachelor_course_category,
               'master_course_category':master_course_category,
                'a_level_sections':Section.objects.filter(course_category = a_level_course_category),
               'bachelor_sections':Section.objects.filter(course_category = bachelor_course_category),
                 'master_sections':Section.objects.filter(course_category = master_course_category),
               'title': 'Section'}
    
    return render(request, "academic/sections/manage_section.html", context)



@permission_required('student_management_app.edit_section', raise_exception=True)
def edit_section(request, section_id):

    section = get_object_or_404(Section, pk=section_id)
    a_level_course_category = get_object_or_404(CourseCategory,course_name = 'A-Level')
    bachelor_course_category = get_object_or_404(CourseCategory,course_name = 'Bachelor')
    master_course_category = get_object_or_404(CourseCategory,course_name = 'Master')
    form = SectionForm(user = request.user,instance = section)
    
    if request.user.adminuser.course_category == a_level_course_category :
        if request.method == 'POST':

            form = SectionForm(request.POST, user = request.user,instance = section)
            try:
                if form.is_valid():
                    instance = form.save(commit = False)
                    instance.course_category = a_level_course_category
                    instance.save()
                    messages.success(request, "Section is updated successfully.")
                    return redirect('admin_app:manage_section')
            except:
                messages.error(request, "Failed to add section.")
                return redirect('admin_app:manage_section')
      
            
    if request.user.adminuser.course_category == bachelor_course_category :
        if request.method == 'POST':
            form = SectionForm(request.POST,user = request.user,instance = section)
            try:
                if form.is_valid():
                    instance = form.save(commit = False)
                    instance.course_category = bachelor_course_category
                    instance.save()
                    messages.success(request, "Section is updated successfully.")
                    return redirect('admin_app:manage_section')
            except:
                messages.error(request, "Failed to add section.")
                return redirect('admin_app:manage_section')
            
            
    if request.user.adminuser.course_category == master_course_category :
        if request.method == 'POST':
            form = SectionForm(request.POST,user = request.user,instance = section)
            try:
                if form.is_valid():
                    instance = form.save(commit = False)
                    instance.course_category = master_course_category
                    instance.save()
                    messages.success(request, "Section is updated successfully.")
                    return redirect('admin_app:manage_section')
            except:
                messages.error(request, "Failed to add section.")
                return redirect('admin_app:manage_section')

    context = {
        'form': form,
        'title': 'Section',
         'sections': Section.objects.all(),
          'a_level_course_category':a_level_course_category,
               'bachelor_course_category':bachelor_course_category,
               'master_course_category':master_course_category,
                'a_level_sections':Section.objects.filter(course_category = a_level_course_category),
               'bachelor_sections':Section.objects.filter(course_category = bachelor_course_category),
                 'master_sections':Section.objects.filter(course_category = master_course_category),
    }
    return render(request, "academic/sections/manage_section.html", context)



@permission_required('student_management_app.delete_section', raise_exception=True)
def delete_section(request, section_id):
    # try:
    section = get_object_or_404(Section, pk=section_id)
    section.delete()
    messages.success(
        request, f' {section.section_name} is Deleted Successfully')
    return redirect('admin_app:manage_section')
    # except:
    #     messages.error(request, 'Failed To Delete Section')
    #     return redirect('admin_app:manage_section')


@permission_required('academic.add_syllabus', raise_exception=True)
def add_syllabus(request):
    if request.method == 'POST':
        form = SyllabusForm(request.POST, request.FILES)

        try:
            if form.is_valid():
                instance = form.save(commit = False)
                instance.save()
                semester = form.cleaned_data['semester']
                
                create_notification(request, post=f'Syllabus is added for Semester : {semester}', notification_type=1, 
                                    created_by=request.user,type='syllabus')
                messages.success(request, "Syllabus is Added Successfully.")
                return redirect('admin_app:add_syllabus')
        except:
            messages.error(request, "Failed to Add Syllabus.")
            return redirect('admin_app:add_syllabus')

    else:
        form = SyllabusForm()

    context = {'form': form,
               'title': 'Syllabus'}
    return render(request, "academic/syllabus/add_syllabus.html", context)


@permission_required('academic.view_syllabus', raise_exception=True)
def manage_syllabus(request):
    syllabus = Syllabus.objects.all()
    search_form = SyllabusSearchForm()
    semester = request.GET.get('semester')
    
    if semester:
        search_syllabus = Routine.objects.filter(semester=semester)
        context = {'syllabus': search_syllabus,
                   'form': SyllabusSearchForm(initial = {'semester': semester}),#show selected instance in search form
                   'title': 'Routine'
                   }

        return render(request, 'academic/syllabus/manage_syllabus.html', context)

    context = {
        'syllabus': syllabus,
        'form': search_form,
               'title': 'Syllabus'
    }
    return render(request, 'academic/syllabus/manage_syllabus.html', context)

def view_student_syllabus(request):
    syllabus = Syllabus.objects.filter(semester = request.user.student.semester).last()
    context = {'syllabus': syllabus,
               'title': 'Syllabus'}
    return render(request, 'academic/syllabus/view_student_syllabus.html', context)


@permission_required('academic.change_syllabus', raise_exception=True)
def edit_syllabus(request, syllabus_id):
    syllabus = get_object_or_404(Syllabus, pk=syllabus_id)
    form = SyllabusForm(instance=syllabus)
    if request.method == 'POST':
        form = SyllabusForm(request.POST, request.FILES,instance=syllabus)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Syllabus is Edited Successfully  .")
                return redirect('admin_app:manage_syllabus')
        except:
            messages.error(request, "Failed To  Edit Syllabus.")
            return redirect('admin_app:edit_syllabus', syllabus_id)
    context = {
        'form': form,
        'title': 'Syllabus'
    }
    return render(request, 'academic/syllabus/edit_syllabus.html', context)


@permission_required('academic.delete_syllabus', raise_exception=True)
def delete_syllabus(request, syllabus_id):
    try:
        syllabus = get_object_or_404(Syllabus, pk=syllabus_id)
        syllabus.delete()
        messages.success(request, f' {syllabus.title} is Deleted Successfully')
        return redirect('admin_app:manage_syllabus')
    except:
        messages.error(request, 'Failed To Delete Syllabus')
        return redirect('admin_app:manage_syllabus')


def student_send_bulk_email(request):
    student_bulk_email = []
    students_email = Student.objects.values_list(
           'student_user__email', flat=True)
    for email in students_email:
        student_bulk_email.append(email)

    if request.method == 'POST':
        # try:
        files = request.FILES.getlist('file')
        subject = request.POST.get('subject', None)
        message = request.POST.get('message', None)
        context = {
            'message': message,
        }
        template = get_template(
            'bulk_email/email_message.html').render(context)

        email = EmailMessage(
            subject,
            template,
            'nirmalpandey27450112@gmail.com',  # sender
            student_bulk_email,  # receiver
        )

        for file in files:
            email.attach(file.name, file.read(), file.content_type)

        email.content_subtype = 'html'
        email.send()
        email.fail_silently = False

        messages.success(request, 'Message is  successfully sent.')
        return redirect('student_send_bulk_email')
        # except:
        # 	messages.error(request, 'Failed to Sent message.')
        # 	return redirect('send_bulk_email')

    return render(request, 'bulk_email/form.html', {'title': 'Student  Message'})


@permission_required('academic.add_assignment', raise_exception=True)
def add_assignment(request):
    # -----
  
    # ------
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        semester = request.POST.get('semester')
        section = request.POST.get('section')
        # subject = request.POST.get('subject')

        # try:
        if form.is_valid():
            # -----------Email msg--------------------
            
        #     student_bulk_email = []
        #     students_email = Student.objects.filter(semester = semester, section = section).\
        #     values_list('student_user__email', flat=True)
        #     print(students_email)
        #     for email in students_email:
        #         student_bulk_email.append(email)
        #     context = {
        #     'message': "Please, Check Your Assignment in GCI Mis.",
        # }
        #     template = get_template(
        #     'bulk_email/email_message.html').render(context)

        #     email = EmailMessage(
        #     "Assignment",
        #     template,
        #     'nirmalpandey27450112@gmail.com',  # sender
        #     student_bulk_email,  # receiver
        # )   
        #     email.content_subtype = 'html'
        #     email.send()
            # email.fail_silently = False 
            # ---------------------Email service end--------------------
            title = form.cleaned_data['title']
            instance = form.save(commit=False)
            instance.teacher_id = request.user.id
            instance.save()
            user = request.user
            create_notification(request, post=title, notification_type=1, created_by=user,type='assignment')
            messages.success(request, "Assignment is Added Successfully.")
            return redirect('admin_app:add_assignment')
        # except:
        #     messages.error(request, "Failed to Add Assignment.")
        #     return redirect('admin_app:add_assignment')

    else:
        form = AssignmentForm()  # passing user so as to restrict choice field for respective user

    context = {
        'form': form,
        'title': 'Assignment'
    }
    return render(request, "academic/assignments/add_assignment.html", context)


@permission_required('academic.view_assignment', raise_exception=True)
def manage_assignment(request):

    assignments = Assignment.objects.all()
    respective_teacher_assignments = Assignment.objects.filter(teacher_id=request.user.id, draft=False)
    draft_assignments = Assignment.objects.filter(teacher_id=request.user.id, draft=True)
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
    total_students = Assignment.objects.filter(student__in=student)
        
    # submitted_assignment_no = CustomUser.objects.filter(Q(pk__in = student)&
    #                                                     Q()).count()
    # ---
    # graded = Grade.objects.filter(status = True).count()
    search_form = SemesterSectionSearchForm()
    semester_id = request.GET.get('semester')
    section_id = request.GET.get('section')
    subject_id = request.GET.get('subject')

    if semester_id and section_id and subject_id:
        search_assignments = Assignment.objects.filter(semester=get_object_or_404(Semester, pk = semester_id),
                                                       section = get_object_or_404(Section, pk = section_id),
                                                       Subject = get_object_or_404(Subject, pk = subject_id))
        print(search_assignments)
        context = {
            'assignments': search_assignments,
            'teacher_assignments': search_assignments,
            'draft_assignments': draft_assignments,
                    # 'total_reviewed':graded,
            'form': search_form,
                    'title': 'Assignment',
        }
        return render(request, 'academic/assignments/manage_assignment.html', context)

    context = {
        'assignments': assignments,
        'teacher_assignments': respective_teacher_assignments,
        'draft_assignments': draft_assignments,
        # 'student_assignments':assignments.filter(),
        'form': search_form,
        # 'submitted_assignment_no':submitted_assignment_no,
        'title': 'Assignment'
    }

    return render(request, 'academic/assignments/manage_assignment.html', context)



# When u click publish in draft section of assignment then draft is changed to False.
def draft_publish_unpublish(request,pk):
    assignment = Assignment.objects.get(pk = pk)
    if assignment.draft == True:
        assignment.draft = False
        assignment.save()
    else:
        assignment.draft=True
        assignment.save()
    return redirect('admin_app:manage_assignment')
    
def add_assignment_grade(request,pk):
    assignment = Assignment.objects.get(pk = pk)
    context = {
        'title':'Mark',
        'assignment':assignment
    }
    return render(request, 'academic/assignments/add_grade.html', context)

@permission_required('academic.change_assignment', raise_exception=True)
def edit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    form = AssignmentForm(instance=assignment)
    if request.method == 'POST':
        form = AssignmentForm(request.POST,
                              request.FILES,
                              instance=assignment)
        try:
            if form.is_valid():
                title = form.cleaned_data['title']
                form.save()
                user = request.user
                create_notification(
                    request, post=title, notification_type=2, created_by=user, type='assignment')
                messages.success(
                    request, "Assignment is Edited Successfully  .")
                return redirect('admin_app:manage_assignment')
        except:
            messages.error(request, "Failed To  Edit Assignment.")
            return redirect('admin_app:edit_assignment', assignment_id)
    context = {
        'form': form,
        'title': 'Assignment'
    }
    return render(request, 'academic/assignments/edit_assignment.html', context)


@permission_required('academic.delete_assignment', raise_exception=True)
def delete_assignment(request, assignment_id):
    try:
        assignment = get_object_or_404(Assignment, pk=assignment_id)
        assignment.delete()
        messages.success(
            request, f' {assignment.title} is Deleted Successfully')
        return redirect('admin_app:manage_assignment')
    except:
        messages.error(request, 'Failed To Delete Assignment')
        return redirect('admin_app:manage_assignment')


def student_assignment(request):
    print(request.user.student.section,";;;;;;;;;;;;;;;;;;;;;;;;;;")
    
    form = SubjectSearchForm(request=request)
    # try:
    query = request.GET.get('subject')

    if query:
        student_assignments =  Assignment.objects.filter(Subject=query)
        context = {
            'assignments': student_assignments,
            'form': form,
            'today_date': timezone.today(),
                    'title': 'Assignment',
        }
        return render(request, 'academic/assignments/student_assignment.html', context)

    student_completed_assignments = Grade.objects.filter(student=request.user.id, assignment_status='Completed')
    student_assigned_assignments =  Assignment.objects.filter(semester= request.user.student.semester, draft = False,
                                                              section=request.user.student.section).exclude(student = request.user.id)

    context = {
        'assigned_assignments': student_assigned_assignments,
        'completed_assignments': student_completed_assignments,
        'form': form,
        'today_date': timezone.now(),
        'title': 'Assignment'
    }

    return render(request, 'academic/assignments/student_assignment.html', context)


def assignment_answer_upload(request, assignment_id, student_id):

    if request.method == 'POST':

        upload_answer_file = request.FILES['answer_upload']
        grade = Grade(assignment_id=assignment_id, student_id = request.user.id, answer_upload = upload_answer_file)
        grade.save()

        '''When particular student submit assignment then make its assignment_status to Completed '''
        student_grade = Grade.objects.filter(pk=grade.id).first()
        student_grade.assignment_status = 'Completed'
        student_grade.save()
        # # assignment.student.set([request.user.id])
        messages.success(request, 'Your Answer is submitted successully.')
        return redirect('admin_app:student_assignment')

    return render(request, 'academic/assignments/upload_answer.html')


def student_assignment_grade(request, assignment_id):
    student_assignments = Grade.objects.filter(assignment=assignment_id).exclude(grade_status = True)

    context = {
        'title': 'Check Assignment',
        'assignments': student_assignments,
    }
    return render(request, 'academic/assignments/view_submit_assignment.html', context)


def assignment_retured(request):
    grade = request.POST.get('grade')
    feedback = request.POST.get('feedback')
    grade_id = request.POST.get('grade_id')
    assignment_id = request.POST.get('assignment_id')
    assignment_grade = Grade.objects.get(pk=grade_id)
    assignment_grade.grade = grade
    assignment_grade.feedback = feedback
    assignment_grade.grade_status = True
    assignment_grade.save(update_fields=['grade', 'grade_status','feedback'])
    messages.success(request, 'Assignment is returned successfully')
    return redirect('academic:student_assignment_grade', assignment_id)


