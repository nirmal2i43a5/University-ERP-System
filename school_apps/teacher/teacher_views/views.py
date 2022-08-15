

import json
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from student_management_app.django_forms.forms import (
                                          AddCustomUserForm,StaffForm,DocumentFileForm,EditCustomUserForm
                                         
                                          )
# from school_apps.academic.forms import StudentFormSearch
from school_apps.attendance.forms import AttendanceDateFilterForm
from student_management_app.models import (
                                        CustomUser, Staff, Student, DocumentFile,SubjectTeacher,Section ,Semester
                                           )
from school_apps.attendance.models import Attendance, AttendanceReport
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required  
from school_apps.academic.forms import ClassFormSearch,StudentSearch


@permission_required('student_management_app.add_teacher', raise_exception=True)
def add_teacher(request):

    if request.method == 'POST':
        custom_form = AddCustomUserForm(request.POST)
        staff_form = StaffForm(request.POST, request.FILES)
        courses = request.POST.getlist("courses")
        
        if custom_form.is_valid() and staff_form.is_valid():
            email = custom_form.cleaned_data["email"]
            full_name = custom_form.cleaned_data["full_name"]
            
            address = staff_form.cleaned_data["address"]
            
            contact = staff_form.cleaned_data['contact']
            gender = staff_form.cleaned_data['gender']
            religion = staff_form.cleaned_data['religion']
            department = staff_form.cleaned_data['department']
            
            joining_date = str(request.POST.get('join_date'))
            date_of_birth = str(request.POST.get('dob'))
            
            if date_of_birth:
                dob =  datetime.datetime.strptime(date_of_birth, "%Y-%m-%d").date()
            else:
                dob = None
            
            if joining_date:
                join_date = datetime.datetime.strptime(joining_date, "%Y-%m-%d").date()
            else:
                join_date = None
            
            

            if request.FILES.get('image'):
                image_url = request.FILES['image']
            else:
                image_url = None

            # try:
            fname = full_name.split()[0]
            teacher_username = full_name.lower().replace(" ","_")
            role = Group.objects.get(name = 'Teacher')
            user = CustomUser.objects.create_user(
                username=teacher_username, password='password', 
                email=email,full_name = full_name, user_type=role)
        
            user.staff.courses.set(courses)
            user.staff.address = address  
            user.staff.contact = contact
            user.staff.gender = gender  
            user.staff.religion = religion
            user.staff.dob = dob  
            user.staff.join_date = join_date
            user.staff.department = department

            if image_url != None:
                user.staff.image = image_url

            user.save()
            user.groups.add(role)
            messages.success(request, "Successfully Added Teacher")
            return redirect('admin_app:manage_staff')

            # except:
            #     messages.error(request, "Failed to Add Teacher")
            #     return redirect('admin_app:add_staff')
        # else:
        #     return HttpResponse("<h1>Invalid Form data</h1>")
    else:
        custom_form = AddCustomUserForm()
        staff_form = StaffForm()

    context = {
        'title':'Add Teacher',
        'custom_form': custom_form,
               'staff_form': staff_form}
    return render(request, 'teachers/add_staff.html', context)


@permission_required('student_management_app.view_teacher', raise_exception=True)
def manage_teacher(request):
    staffs = Staff.objects.all()  

    context = {'staffs': staffs,
               'title':'Manage Teacher'
               }
    
    return render(request, 'teachers/manage_staff.html', context)


@permission_required('student_management_app.change_teacher', raise_exception=True)
def edit_teacher(request, staff_id):
    staff_form_instance = get_object_or_404(Staff, staff_user=staff_id)
    custom_form_instance = get_object_or_404(CustomUser,pk = staff_id )
    
    if request.method == 'POST':
        staff_form = StaffForm(request.POST, request.FILES, instance=staff_form_instance)
        custom_form = EditCustomUserForm(request.POST, instance = custom_form_instance)
        
        try:
            if staff_form.is_valid() and custom_form.is_valid():
                staff_form.save()
                custom_form.save()
                messages.success(request, "Successfully Edited Teacher")
                return redirect('admin_app:manage_staff')
            
        except:
            messages.error(request, "Failed to Update Teacher")
            return redirect('admin_app:manage_staff')
    else:
        staff_form = StaffForm(instance=staff_form_instance)
        custom_form = EditCustomUserForm(instance = custom_form_instance)

    context = {'staff_form':staff_form, 
               'custom_form':custom_form,
               'title':'Edit Teacher'
               }
    return render(request, 'teachers/edit_staff.html', context)


@permission_required('student_management_app.delete_teacher', raise_exception=True)
def delete_teacher(request, staff_id):
  
    try:
        staff = get_object_or_404(Staff, staff_user = staff_id)
        staff.delete()
        messages.success(request, f'{staff.staff_user.username} is Deleted Successfully')
        return redirect('admin_app:manage_staff')
    except:
        messages.error(request, 'Failed To Delete Teacher')
        return redirect('admin_app:manage_staff')


def search_teacher(request):
    search_text = request.GET.get('query')
    if search_text:
        search_staffs = Staff.objects.filter(Q(staff_user__first_name__icontains=search_text) |
                                             Q(contact__iexact=search_text))
        return render(request, 'teachers/manage_staff.html', {'staffs': search_staffs})
    else:
        staffs = Staff.objects.all()
        return render(request, 'teachers/manage_staff.html', {'staffs': staffs})



# this is for ajax part (my ajax is success with title with title but file cannot upload so i am using above views for )
@csrf_exempt
@permission_required('student_management_app.add_teacher_document', raise_exception=True)
def add_teacher_document(request, teacher_id):#for ajax part
    
    teacher = get_object_or_404(Staff, pk = teacher_id)
    
    if request.method=="POST":
        
        form=DocumentFileForm(request.POST, request.FILES)
        if form.is_valid():
            document_id =request.POST["documentid"]#this is hidden field 
            title=request.POST.get("title")
            file=request.FILES["file"]  
            if(document_id==''):#if there is no product id then it has to insert data clicking on save button
                document = form.save(commit = False)
                #when i add_file then it must be the file of particular student with their respective id and i can retrieve this using _set see in view_student views function
                document.staff = teacher
                
            else:#if not id then edit data clicking on save button 
                document = form.save(commit = False)
                document.id = document_id#for updating particular field
                document.staff = teacher
            
        
            #when i add_file then it must be the file of particular student with their respective id and i can retrieve this using _set see in view_student views function
            document.save()
            document_value=DocumentFile.objects.filter(staff=teacher).values()#this filter data to show in ajax but commit filter for database
            document_data =list(document_value)#change to json
            return JsonResponse({'status':'True','document_data':document_data,'message':'Document is Successfully Saved'},safe=False)
        else:
            return JsonResponse({'status':0})
       



def attendance_filter_form(request):
    attendance_form = AttendanceDateFilterForm()
    return attendance_form
    
    
#attendance details of particular student 
# def attendance_view(request):
    
#     if request.method == 'POST' and 'attendance_submit' in request.POST:
        
#         attendance_form  = AttendanceDateFilterForm(request.POST)
        
#         start_date = request.POST.get('start_date')
#         end_date = request.POST.get('end_date')
#         start_data_parse=datetime.datetime.strptime(start_date,"%Y-%m-%d").date()
#         end_data_parse=datetime.datetime.strptime(end_date,"%Y-%m-%d").date()
        
#         teacher_id = request.POST.get('teacher')#froom hidden input
#         teacher = get_object_or_404(Staff , id = teacher_id)
        
#         attendance = Attendance.objects.filter(
#             attendance_date__range = (start_data_parse,end_data_parse),
          
#             )
        
     
#         teacher_attendance = AttendanceReport.objects.\
#         filter(staff = teacher_id, attendance__in = attendance)# or filter(student = student_id, attendance__attendance_date = month)
        
#         return teacher_attendance#return to view_student
    
    
# logic for student_profile and add_submit data with modal form
@permission_required('student_management_app.view_teacher_profile', raise_exception=True)
def view_teacher(request, teacher_id):
    
    try:
        teacher = Staff.objects.get(staff_user = teacher_id)#this is the  student_id  come from student not from customuser<check in view click>
        #this retrieve subjects belongs to customuser teacher
        customuser_teacher = CustomUser.objects.filter(user_type = Group.objects.get(name = 'Teacher')).get(id = teacher_id)
        subjects = customuser_teacher.subject_set.all()
    except:
        return render(request, '404.html')
    #retrieve DocumentFile upload for particualr student using foreign key    
    teacher_files =  teacher.documentfile_set.all()
    
    #this is for adding document form that is in view_student
    form = DocumentFileForm()

    if request.method == 'POST':
        print("inside:::::---------------:::::")
        
        attendance_form  = AttendanceDateFilterForm(request.POST)
        
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        start_data_parse=datetime.datetime.strptime(start_date,"%Y-%m-%d").date()
        end_data_parse=datetime.datetime.strptime(end_date,"%Y-%m-%d").date()
        
        teacher_id = request.POST.get('teacher')
        teacher = get_object_or_404(Staff , id = teacher_id)
        
        attendance = Attendance.objects.filter(
            attendance_date__range = (start_data_parse,end_data_parse),
          
            )
        
     
        teacher_attendance = AttendanceReport.objects.\
        filter(staff = teacher_id, attendance__in = attendance)
        context = {
                 'title':'View Teacher Details',
                'teacher':teacher,
               'subjects':subjects,
               'teacher_files':teacher_files,
               'form':form,
               
               #for attendance
               'attendance_form':attendance_filter_form(request),
               'attendance_reports':teacher_attendance
               }
        return render(request, 'teachers/views/main_view.html',context)
    context = {
                 'title':'View Teacher Details',
                'teacher':teacher,
               'subjects':subjects,
               'teacher_files':teacher_files,
               'form':form,
               
               #for attendance
               'attendance_form':attendance_filter_form(request),
               }
    return render(request, 'teachers/views/main_view.html',context)




#this is for edit student document(for edit it also goes to else part in add)
@csrf_exempt
@permission_required('student_management_app.edit_teacher_document', raise_exception=True)
def edit_teacher_document(request):
    
    id=request.POST.get('documentid')
    if request.method=="POST":
        id=request.POST.get('documentid')
        
    document= get_object_or_404(DocumentFile, pk=id)
    
    file_data = json.dumps(str(document.file)) #you can't serialize the object, because it's an Image. You have to serialize the string representation of it's path.
    
    document_data={"id":document.id, "title":document.title,"file":file_data }
    """i cant see file but cant see title instance while click edit button .because i am not passing--
    "file":file as it gives file field cannt be json serailize.so ,I will solve this problem in future
    """
    return JsonResponse(document_data,safe=False)


@permission_required('student_management_app.delete_teacher_document', raise_exception=True)
def delete_teacher_document(request,teacher_id, document_id):
    
    try:
        document = get_object_or_404(DocumentFile, id = document_id)#i am using custom user so i use staff_user_id instead of normal document id = staff_id
        document.delete()
        messages.success(request, f'Document is Deleted Successfully')
        return redirect('admin_app:view_teacher', teacher_id)
    except:
        messages.error(request, 'Failed To Delete Document')
        return redirect('admin_app:view_teacher', teacher_id)



def teacher_log(request):
    teachers_logs = Staff.history.all()
    context = {
        'title':'Teacher Log',
         'teachers_logs':teachers_logs,
    }
    return render(request,'teachers/loghistory/history.html',context)



def delete_log(request):
    print("delete-----")
    Staff.history.all().delete()
    messages.success(request,"Teachers logs are deleted successfully.")
    return redirect('teacher:teacher_log')
    
    
    
def student_view_by_teacher(request):
    
    subjectteacher = SubjectTeacher.objects.filter(teacher = request.user.id)
    # -------
    # search_form = StudentSearch(user = request.user)
    semester_query = request.GET.get('filter_semester')
    course_query = request.GET.get('filter_course')
    course_category_query = request.GET.get('course_category')
    section_query = request.GET.get('section')
    semester_instance = Semester.objects.get(pk = semester_query) if semester_query else None
    section_instance = Section.objects.get(pk = section_query) if section_query else None
    search_form = StudentSearch(user = request.user,initial = {
        'course_category':course_category_query,'filter_course':course_query,
        'filter_semester':semester_query,'section':section_query})
    if semester_query and section_query:
        search_students = Student.objects.filter(semester = semester_instance,section = section_instance,student_user__is_active = 1)
        context = {'students': search_students,'form':search_form}
        return render(request,'teachers/students/student_list.html', context)
    
    if semester_query:
        search_students = Student.objects.filter(semester = semester_instance,student_user__is_active = 1)
        context = {'students': search_students,'form':search_form}
        return render(request,'teachers/students/student_list.html', context)

    else:
        search_students = Student.objects.filter(semester = semester_instance,student_user__is_active = 1)
        context = {
            'students': Student.objects.filter(student_user__is_active = 1),
                   'form':search_form}
        return render(request,'teachers/students/student_list.html', context)
    #     students = []
    #     for item in subjectteacher:
    #         students = Student.objects.filter(semester = item.semester,section = item.section)
    
    #     context = {
    #     'title':'Student Details',
    #         'form':search_form,
    #     'students':students
        
    # }
        # return render(request,'teachers/students/student_list.html', context)
    # ------------
    
  
