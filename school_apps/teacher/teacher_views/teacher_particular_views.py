

"""This contains all the views for student"""
from django.shortcuts import render, redirect,get_object_or_404

from student_management_app.models import Subject, Student, Staff, CustomUser

def teacher_home(request):
    # Fetch All Student Under Particular Teacher
       
    # teacher = get_object_or_404(Staff, staff_user = request.user)#for current login teacher
    subjects = Subject.objects.filter(staff_user = request.user.id)#sub for current login user
    students = Student.objects.filter(course)#subject belongs to particular teacher and subject is fk in student.so access 
    subject_count = subjects.count()
    context = {'subject_count':subject_count}
    return render(request, 'teacher_templates/dashboard.html',context)
