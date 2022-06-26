import os

import json
import datetime
import csv,io
from dateutil.parser import parse
from school_apps.courses.models import selectedcourses
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db.models import Q,Count
from django.views.decorators.csrf import csrf_exempt
from student_management_app.django_forms.forms import AddCustomUserForm, DocumentFileForm, EditCustomUserForm
from school_apps.attendance.forms import StudentAttendanceDateFilterForm
from school_apps.academic.forms import StudentFormSearch,StudentSearch
from school_apps.student.forms import StudentForm
from student_management_app.models import (
    Course, CustomUser, Subject, Staff, SessionYear, Student,
    DocumentFile, Parent, Semester
)
from school_apps.parents.forms import (ParentForm)

from student_management_app.models import *
from school_apps.attendance.models import Attendance, AttendanceReport
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import  permission_required


@permission_required('student_management_app.add_student', raise_exception=True)
def add_student(request):
    
    if request.method == 'POST':

        custom_form = AddCustomUserForm(request.POST)
        student_form = StudentForm(request.POST, request.FILES)
        parent_form = ParentForm(request.POST, request.FILES)
        if custom_form.is_valid() and student_form.is_valid() and parent_form.is_valid():

            # parent = parent_form.save()
            email = custom_form.cleaned_data["email"]
            full_name = custom_form.cleaned_data['full_name']
            student_id = student_form.cleaned_data['stu_id']

            date_of_birth = str(request.POST.get('dob'))
            dob = datetime.datetime.strptime(
                date_of_birth, "%Y-%m-%d").date()  # parsing html date to python

            if request.FILES.get('image'):
                image_url = request.FILES['image']
            else:
                image_url = None

            parent_role = Group.objects.get(name='Parent')
            
            # father_fname = parent_form.cleaned_data["father_name"].split()[0]
            fname = full_name.split()[0]
            father_username = "p" + fname.lower() + f'{student_id}' 
            Father_object = CustomUser.objects.create_user(
                username=father_username, password='password', user_type=parent_role, full_name = parent_form.cleaned_data["father_name"]
            )

            Father_object.parent.father_name = parent_form.cleaned_data['father_name']
            Father_object.parent.mother_name = parent_form.cleaned_data['mother_name']
            Father_object.parent.father_phone = parent_form.cleaned_data['father_phone']
            Father_object.parent.mother_phone = parent_form.cleaned_data['mother_phone']
            Father_object.parent.local_guardian_name = parent_form.cleaned_data['local_guardian_name']
            Father_object.parent.local_guardian_phone =  parent_form.cleaned_data['local_guardian_phone']
            Father_object.parent.home_phone = parent_form.cleaned_data['home_phone']
            Father_object.groups.add(parent_role)
            Father_object.parent.save()
            
            
            fname = full_name.split()[0]
            student_username = fname.lower() + f'{student_id}'
            role = Group.objects.get(name='Student')
            user = CustomUser.objects.create_user(
                username=student_username, password='password', email=email, user_type=role, full_name = full_name)
                  
            # bachelor_group = Group.objects.get(name = 'Bachelor-Admin')
            # master_group = Group.objects.get(name = 'Master-Admin')
            # user_type = request.user.adminuser
            # if request.user.is_superuser and request.user.groups.filter(name = bachelor_group).exists():
            #     user.student.category = 'Bachelor'
            # if request.user.is_superuser and request.user.groups.filter(name = master_group).exists():
            #     user.student.category = 'Master'
            # if request.user.is_superuser and not request.user.groups.filter(name = bachelor_group).exists()\
            #                             and not request.user.groups.filter(name = master_group).exists() :
            #     user.student.category = 'A-Level'
        #     fields = (
        #     'join_year','stu_id','roll_no','gender','shift','semester','section','course','faculty','program','status','contact',
        #     'permanent_address','temporary_address','dob','blood_group','gpa','previous_school_name','image',
        # )
         
           
            user.student.course_category = get_object_or_404(CourseCategory, course_name = student_form.cleaned_data['course_category'])
            user.student.semester = student_form.cleaned_data['semester']
            user.student.section = student_form.cleaned_data['section']
            user.student.join_year =  student_form.cleaned_data["join_year"]
            user.student.stu_id = student_form.cleaned_data['stu_id']
            user.student.roll_no = student_form.cleaned_data['roll_no']
            user.student.gender = student_form.cleaned_data['gender']
            user.student.shift = student_form.cleaned_data["shift"]
            user.student.course = student_form.cleaned_data['course']
            user.student.faculty = student_form.cleaned_data['faculty']
            user.student.program = student_form.cleaned_data['program']
            user.student.status = student_form.cleaned_data['status']
            user.student.contact = student_form.cleaned_data['contact']
            user.student.permanent_address = student_form.cleaned_data['permanent_address']
            user.student.temporary_address = student_form.cleaned_data['temporary_address']
            user.student.dob = dob
            user.student.blood_group = student_form.cleaned_data['blood_group']
            # user.student.optional_subject = student_form.cleaned_data['optional_subject']
            user.student.gpa = student_form.cleaned_data['gpa']
            user.student.previous_school_name = student_form.cleaned_data["previous_school_name"]
            user.student.guardian = Father_object.parent
            if image_url != None:
                user.student.image = image_url
            user.save()
            user.groups.add(role)
            

            # selectedcourses.objects.create(
            #     student_id=user.student,
            #     subject_id = student_form.cleaned_data['optional_subject'],
            #     semester = student_form.cleaned_data['semester']
            # )

            # user.student.state = student_form.cleaned_data['state']
            # user.student.country = student_form.cleaned_data['country']
            # # user.student.group = group
            # # user.student.optional_subject = optional_subject
            # # user.student.register_no = register_no
            # # user.student.extra_activities = student_form.cleaned_data['extra_curricular_activities']
            # # user.student.remarks = student_form.cleaned_data['remarks']
            messages.success(request, "Successfully Added Student")
            return redirect('admin_app:manage_student')

            # except:
            #     messages.error(request, "Failed to Add Student")
            #     return redirect('admin_app:add_student')

    else:
        custom_form = AddCustomUserForm()
        student_form = StudentForm()
        parent_form = ParentForm()
    context = {
            'title':'Add Student',
            'custom_form': custom_form,
            'student_form': student_form,
            'parent_form': parent_form
        }
    return render(request, 'students/add_student.html', context)





@permission_required('student_management_app.student_bulk_upload', raise_exception=True)
def student_file_upload(request):
    if request.method == "GET":
        return render(request, 'students/file_upload.html')
    else:
        csv_file = request.FILES['studentfile']
        
    if not csv_file.name.endswith('.csv'):
        print("Invalid file")
        
    data_set = csv_file.read().decode('latin-1')
    io_string = io.StringIO(data_set)
    next(io_string)
    
    file_data = csv.reader(io_string, delimiter=',', quotechar="|")
    
    for column in file_data:
        batch = column[1]
        join_year = batch[0:4]
        student_id = column[2]
        roll_no = column[3]
        fullName = column[4]
        gender = column[5]
        shift = column[6]
        section = column[7]
        course = column[8]
        faculty_first = column[9]
        email = column[9]      
        faculty_second = column[10]
        faculty = f'{faculty_first},{faculty_second}'#faculty column contain two column because comman separate one col to multi column
        program = column[10]
        status = column[11]
        home_phone = column[12]
        contact = column[13]
        permanent_address = column[20]
        temporary_address = column[21]
        
        dob_es_parse=""
        if (column[22]!="" ):
            dob_es_parse = parse(column[22]).date() #this change from 8/10/2020 to 2020-8-10 i.e in python format
        
        dob_bs_parse=""
        if (column[23]!="" ):
            dob_bs_parse = parse(column[23]).date()
        blood_group = column[24]
        # optional_subject = column[26]
        gpa = column[26]
        previous_school =  column[27]  
        # dob_es_parse = datetime.datetime.strptime(dob_es, "%Y-%m-%d")
    
        
        home_phone = home_phone,
        # home_phone[3:len-3] 
        father_name=column[14],
        father_phone=column[15],
        # home_phone[3:len-3] 
        mother_name=column[16],
        mother_phone=column[17],
        local_guardian_name=column[18],
        local_guardian_phone=column[19]

        father_name = ''.join(father_name)
        father_phone = ''.join(father_phone)
        mother_name = ''.join(mother_name)
        mother_phone = ''.join(mother_phone)
        local_guardian_name = ''.join(local_guardian_name)
        local_guardian_phone = ''.join(local_guardian_phone)
        fname = column[4].split()[0]
        
        student_username = fname.lower() + f'{student_id}'
        parent_role = Group.objects.get(name='Parent')
        father_username = "p" + student_username 
        Father_object = CustomUser.objects.create_user(
            username=father_username, password='password', user_type=parent_role, full_name = father_name
        )
        
        Father_object.parent.father_name = father_name
        Father_object.parent.mother_name = mother_name
        Father_object.parent.father_phone = father_phone
        Father_object.parent.mother_phone = mother_phone
        Father_object.parent.local_guardian_name = local_guardian_name
        Father_object.parent.local_guardian_phone =  local_guardian_phone
        Father_object.parent.home_phone = home_phone
        Father_object.groups.add(parent_role)
        Father_object.parent.save()
        
        sem_obj, created= Semester.objects.get_or_create(
            name=batch,
            course_category = request.user.adminuser.course_category
        )

        sem = sem_obj
        role = Group.objects.get(name = 'Student')
        # ---
        username_from_file = column[28]  
        customuser_object = CustomUser.objects.create_user(username = username_from_file,
                                                           password='password', 
                                                           email=email,
                                                           user_type=role,
                                                           full_name=fullName
                                                           )
        
 
        # ---
        customuser_object.student.course_category = get_object_or_404(CourseCategory, course_name = request.user.adminuser.course_category)
        customuser_object.student.stu_id = student_id
        customuser_object.student.roll_no = roll_no
        customuser_object.student.gender = gender
        customuser_object.student.shift = shift
        customuser_object.student.semester =  Semester.objects.get(name = batch, course_category = request.user.adminuser.course_category)
        
        if (column[7]!=""):
            section_obj, created = Section.objects.get_or_create(semester = sem_obj, section_name = section, course_category = sem_obj.course_category)
            customuser_object.student.section =  section_obj
       
        customuser_object.student.course = course
        customuser_object.student.faculty = column[10]
        customuser_object.student.program = program
        customuser_object.student.status = status
        customuser_object.student.contact = contact
        customuser_object.student.permanent_address = permanent_address
        customuser_object.student.temporary_address = temporary_address
        
        if dob_es_parse!="":
            customuser_object.student.dob = dob_es_parse
        elif dob_bs_parse!="":
            customuser_object.student.dob = dob_bs_parse
        else:
            customuser_object.student.dob = datetime.date.today()
        customuser_object.student.blood_group = blood_group
        # customuser_object.student.optional_subject = Subject.objects.get(subject_name = column[26])
        customuser_object.student.gpa = gpa
        customuser_object.student.previous_school_name = previous_school
        customuser_object.student.guardian = Father_object.parent
        customuser_object.student.join_year = batch[0:4]
        customuser_object.save()
        customuser_object.groups.add(role)

        # selectedcourses.objects.create(#mainly for through table
        #         student_id=customuser_object.student,
        #         subject_id = customuser_object.student.optional_subject,
        #         semester = customuser_object.student.semester
        #     )
        
    messages.success(request,"Students are successfully uploaded.")    
    return redirect('admin_app:manage_student')



def student_bulk_photo_upload(request):
    if request.method == 'POST':
        photos = request.FILES.getlist('photos')
        image_name = []
        for photo in photos:
            name = os.path.splitext(str(photo))
            image_name.append(name)
            
        student_id = []
        for username in image_name:
            student_id.append(username[0])
            
        for uname,photo in zip(student_id,photos):
            student_obj = Student.objects.get(student_user__username = uname)
            student_obj.image = photo
            student_obj.save(update_fields = ['image'])
            messages.success(request,'Photos are uploaded successfully')
            
    context = {
        'title':'Bulk Photo Upload'
    }
    
    return render(request,'students/student_bulk_photo_upload.html', context)

@permission_required('student_management_app.print_student_id_card', raise_exception=True)
def student_id_card(request, pk):
    student = get_object_or_404(Student, pk=pk)
    bachelor_category = get_object_or_404(CourseCategory,course_name = 'Bachelor')
    context = {
        'title': 'Id Card',
        'student': student,
        'bachelor_category':bachelor_category
    }
    return render(request,'students/print_id_card.html', context)


def bulk_print_id_card(request):
    bachelor_category = get_object_or_404(CourseCategory,course_name = 'Bachelor')
    count = int(request.POST.get("count"))
    i = 1
    students = []
    while (i<=count):
        students.append(get_object_or_404(Student, pk=request.POST.get(str(i))))
        i+=1
    context = {
        'students':students,
        'bachelor_category':bachelor_category
    }
    return render(request,'students/bulk_print_id_card.html', context)



# this is for ajax part (my ajax is success with title with title but file cannot upload so i am using above views for )
@csrf_exempt
@permission_required('student_management_app.add_student_document', raise_exception=True)
def add_student_document(request, student_id):  # for ajax part

    student = get_object_or_404(Student, pk=student_id)

    # add_document_submit come from formData action
    if request.method == "POST" and request.POST['action'] == "add_document_submit":

        form = DocumentFileForm(request.POST, request.FILES)
        if form.is_valid():
            document_id = request.POST["documentid"]  # this is hidden field
            title = request.POST.get("title")
            file = request.FILES["file"]

            if(document_id == ''):  # if there is no product id then it has to insert data clicking on save button
                document = form.save(commit=False)
                # when i add_file then it must be the file of particular student with their respective id and i can retrieve this using _set see in view_student views function
                document.student = student

            else:  # if not id then edit data clicking on save button
                document = form.save(commit=False)
                document.id = document_id  # for updating particular field
                document.student = student

            # when i add_file then it must be the file of particular student with their respective id and i can retrieve this using _set see in view_student views function
            document.save()
            # this filter data to show in ajax but commit filter for database
            document_value = DocumentFile.objects.filter(
                student=student).values()
            document_data = list(document_value)  # change to json

            return JsonResponse({'status': 'True', 'document_data': document_data, 'message': 'Document is Successfully Saved'}, safe=False)
        else:
            return JsonResponse({'status': 0})


def attendance_filter_form(request):
    attendance_form = StudentAttendanceDateFilterForm()
    return attendance_form



# attendance details of particular student
def attendance_view(request):

    if request.method == 'POST' and 'attendance_submit' in request.POST:
        attendance_form = StudentAttendanceDateFilterForm(request.POST)
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        start_data_parse = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        end_data_parse = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

        # subject_id = request.POST.get('subject')  # from hidden input
        # subject = get_object_or_404(Subject, pk=subject_id)

        student_id = request.POST.get('student')  # from hidden input
        student = get_object_or_404(Student, pk=student_id)
        
        attendance = Attendance.objects.filter(attendance_date__range=(start_data_parse, end_data_parse),
                                            #    subject = subject_id
                                               )

        # i add course in student  so access subject for student based on course in the collge only.
        student_attendance = AttendanceReport.objects.filter(student=student_id, attendance__in = attendance)  # or filter(student = student_id, attendance__attendance_date = month)
        total_present=AttendanceReport.objects.filter(student=student_id, attendance__in = attendance,status = 'Present').count()
        total_absent=AttendanceReport.objects.filter(student=student_id, attendance__in = attendance,status = 'Absent(Not Informed').count()
        return [student_attendance,total_present,total_absent]  



''' This is the student attendance view by admin '''
@permission_required('student_management_app.view_student_profile', raise_exception=True)
def view_student(request, student_id):

    try:
        student = get_object_or_404(Student, pk=student_id)
    except:
        return render(request, '404.html')
    
    #retrieve DocumentFile upload for particualr student using foreign key    
    student_files =  student.documentfile_set.all()
    
    courses = selectedcourses.objects.filter(student_id = student)
    
    # student_attendance = attendance_view(request)
    if request.method == 'POST' and 'attendance_submit' in request.POST:
        attendance_form = StudentAttendanceDateFilterForm(request.POST)
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        start_data_parse = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        end_data_parse = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

        # subject_id = request.POST.get('subject')  # from hidden input
        # subject = get_object_or_404(Subject, pk=subject_id)

        student_id = request.POST.get('student')  # from hidden input
        student = get_object_or_404(Student, pk=student_id)
        
        attendance = Attendance.objects.filter(attendance_date__range=(start_data_parse, end_data_parse),
                                            #    subject = subject_id
                                               )

        # i add course in student  so access subject for student based on course in the collge only.
        student_attendance = AttendanceReport.objects.filter(student=student_id, attendance__in = attendance)  # or filter(student = student_id, attendance__attendance_date = month)
        total_present=AttendanceReport.objects.filter(student=student_id, attendance__in = attendance,status = 'Present').count()
        total_absent=AttendanceReport.objects.filter(student=student_id, attendance__in = attendance, status__in = ['Absent(Not Informed)','Absent(Informed)']).count()
    
        context = {
                'title':'View Student Details',
                'student':student,
                'student_files':student_files,
                'form': DocumentFileForm(),
                 'attendance_reports': student_attendance,#for report list after post request
                'attendance_form':  StudentAttendanceDateFilterForm(initial = {
                                                                    # 'subject':subject,
                                                                          'start_date':start_data_parse,
                                                                          'end_date':end_data_parse}),
                'total_present':total_present,
                'total_absent':total_absent,
                'selectedcourses':courses
                
                
                }
        
        
        return render(request, 'students/views/main_view.html',context)
            
    context = {
                'title':'View Student Details',
                'student':student,
                'student_files':student_files,
                'form': DocumentFileForm(),
                'attendance_form': attendance_filter_form(request),
                 'selectedcourses':courses,
                
                }
    return render(request, 'students/views/main_view.html',context)


def student_view_by_parent(request):
    parent = get_object_or_404(Parent, parent_user = request.user.id)
    childrens = parent.student_set.all()
    context = {
        'title':'Childred Details',
        'childrens':childrens
        
    }
    return render(request,'children/child_view.html', context)


''' This is the student attendance view by parent and teacher '''
def student_attendance_view(request, student_id):
    try:
        student = get_object_or_404(Student, pk=student_id)
    except:
        return render(request, '404.html')
    
    # student_attendance, total_present,total_absent = attendance_view(request)
    if request.method == 'POST' and 'attendance_submit' in request.POST:
        attendance_form = StudentAttendanceDateFilterForm(request.POST)
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        start_data_parse = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        end_data_parse = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

        # subject_id = request.POST.get('subject')  # from hidden input
        # subject = get_object_or_404(Subject, pk=subject_id)

        student_id = request.POST.get('student')  # from hidden input
        student = get_object_or_404(Student, pk=student_id)
        
        attendance = Attendance.objects.filter(attendance_date__range=(start_data_parse, end_data_parse)
                                            #    , subject = subject_id
                                               )

        # i add course in student  so access subject for student based on course in the collge only.
        student_attendance = AttendanceReport.objects.filter(student=student_id, attendance__in = attendance)  # or filter(student = student_id, attendance__attendance_date = month)
        total_present=AttendanceReport.objects.filter(student=student_id, attendance__in = attendance,status = 'Present').count()
        total_absent=AttendanceReport.objects.filter(student=student_id, attendance__in = attendance,status__in = ['Absent(Not Informed)','Absent(Informed)']).count()
        context = {
        'title':'Attendance Details',
        'student':student,
        'attendance_reports': student_attendance,
        'attendance_form':  StudentAttendanceDateFilterForm(initial = {
            # 'subject':subject,
                                                                          'start_date':start_data_parse,
                                                                          'end_date':end_data_parse}),#for report list after post request
        'total_present':total_present,
        'total_absent':total_absent
        
    }
        return render(request,'students/attendance/attendance_view.html', context)
    
    context = {
        'title':'Student Details',
        'student':student,
        'attendance_form':  StudentAttendanceDateFilterForm(),
        
    }
    return render(request,'students/attendance/attendance_view.html', context)


# this is for edit student document(for edit it also goes to else part in add)
@csrf_exempt
@permission_required('student_management_app.edit_student_document', raise_exception=True)
def edit_student_document(request):

    id = request.POST.get('documentid')

    if request.method == "POST":
        id = request.POST.get('documentid')

    document = get_object_or_404(DocumentFile, pk=id)
    # you can't serialize the object, because it's an Image. You have to serialize the string representation of it's path.
    file_data = json.dumps(str(document.file))
    document_data = {"id": document.id,
                     "title": document.title, "file": file_data}
    
    return JsonResponse(document_data, safe=False)



@permission_required('student_management_app.delete_student_document', raise_exception=True)
def delete_student_document(request, student_id, document_id):
    try:
        # i am using custom user so i use staff_user_id instead of normal document id = staff_id
        document = get_object_or_404(DocumentFile, pk=document_id)
        document.delete()
        messages.success(request, f'Document is Deleted Successfully')
        return redirect('admin_app:view_student', student_id)
    except:
        messages.error(request, 'Failed To Delete Document')
        return redirect('admin_app:view_student', student_id)





@permission_required('student_management_app.change_student', raise_exception=True)
def edit_student(request, student_id):

    student_form_instance = get_object_or_404(Student, pk=student_id)
    custom_form_instance = get_object_or_404(CustomUser, pk=student_form_instance.student_user.pk)
    parent_form_instance = student_form_instance.guardian

    if request.method == 'POST':
        student_form = StudentForm(request.POST, request.FILES, instance=student_form_instance)
        custom_form = EditCustomUserForm(request.POST, instance=custom_form_instance)
        parent_form = ParentForm(request.POST, instance=parent_form_instance)
        
        try:
            if student_form.is_valid() and custom_form.is_valid() and parent_form.is_valid():
                student_form.save()
                custom_form.save()
                parent_form.save()
                messages.success(request, "Successfully Edited Student")
                return redirect('admin_app:manage_student')
        except:
            messages.error(request, "Failed to Update Student")
            return redirect('admin_app:manage_student')
        
    else:
        student_form = StudentForm(instance=student_form_instance)
        custom_form = EditCustomUserForm(instance=custom_form_instance)
        parent_form = ParentForm(instance=parent_form_instance)


    context = {
               'title':'Edit Student', 
                'student_form':student_form,
               'custom_form':custom_form,
               'parent_form':parent_form
               }
    return render(request, 'students/edit_student.html', context)


@permission_required('student_management_app.delete_student', raise_exception=True)
def delete_student(request, pk):
    # try:
    student_object = get_object_or_404(Student, pk=pk)
    custom_form_instance = get_object_or_404(CustomUser, pk=student_object.student_user.pk)
    custom_form_instance.delete()
    messages.success(
        request, f'{student_object.student_user.username} is Deleted Successfully')
    return redirect('admin_app:manage_student')
    # except:
    #     messages.error(request, 'Failed To Delete Student')
    #     return redirect('admin_app:manage_student')
    

def make_student_inactive(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    user.is_active = 0
    user.save()
    messages.success(request, 'Student is inactive successfully')
    return redirect('admin_app:manage_student')
    
    
    
def restore_inactive_students(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    user.is_active = 1
    user.save()
    messages.success(request, 'Student is activated successfully')
    return redirect('student:inactive_students')
    
    


@permission_required('student_management_app.view_student', raise_exception=True)
def inactive_students(request):    
    
    students = Student.objects.filter(student_user__is_active = 0,course_category = request.user.adminuser.course_category)
    search_form = StudentFormSearch(user = request.user)
    semester_query = request.GET.get('semester')
    section_query = request.GET.get('section')
    group_query = request.GET.get('group')
    
    if semester_query and section_query and group_query:
        search_students = Student.objects.filter(semester = semester_query, section = section_query,faculty = group_query)
        context = {'students': search_students,'form':search_form}
        return render(request, 'students/inactive_students.html', context)
    
    elif semester_query:
        search_students = Student.objects.filter(semester = semester_query)
        context = {'students': search_students,'form':search_form}
        return render(request, 'students/inactive_students.html', context)
    
    elif section_query:
        search_students = Student.objects.filter(section = section_query)
        context = {'students': search_students,'form':search_form}
        return render(request, 'students/inactive_students.html', context)
    
    elif group_query:
        search_students = Student.objects.filter(faculty = group_query)
        context = {'students': search_students,'form':search_form}
        return render(request, 'students/inactive_students.html', context)
    else:
        context = {
            'title':'Inactive Students',
            'students': students,
            'form':search_form
                }
        return render(request, 'students/inactive_students.html', context)



@permission_required('student_management_app.view_student', raise_exception=True)
def manage_student(request):
    a_level_course_category = get_object_or_404(CourseCategory,course_name = 'A-Level')
    bachelor_course_category = get_object_or_404(CourseCategory,course_name = 'Bachelor')
    master_course_category = get_object_or_404(CourseCategory,course_name = 'Master')
    search_form = StudentSearch(user = request.user)
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
        return render(request, 'students/manage_student.html', context)
    
    elif semester_query:
        search_students = Student.objects.filter(semester = semester_query,student_user__is_active = 1)
        context = {'students': search_students,'form':search_form}
        return render(request, 'students/manage_student.html', context)
    
    elif section_query:
        search_students = Student.objects.filter(section = section_query,student_user__is_active = 1)
        context = {'students': search_students,'form':search_form}
        return render(request, 'students/manage_student.html', context)
    
    elif group_query:
        search_students = Student.objects.filter(faculty = group_query, student_user__is_active = 1)
        context = {'students': search_students,'form':search_form}
        return render(request, 'students/manage_student.html', context)

    else:
        context = {
            'title':'Manage Student',
            'students': students,
                'form':search_form,'status':True
                }
        return render(request, 'students/manage_student.html', context)
    



def student_log(request):
    students_logs = Student.history.all()
    context = {
        'title':'Student Log',
         'students_logs':students_logs,
    }
    return render(request,'students/loghistory/history.html',context)



def delete_log(request):
    Student.history.all().delete()
    messages.success(request,"Students logs are deleted successfully.")
    return redirect('student:student_log')



