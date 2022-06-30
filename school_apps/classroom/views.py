from django.shortcuts import render,get_object_or_404
from student_management_app.models import CourseCategory, Semester



def class_home(request):
    context = {
        
    }
    return render(request, 'classroom/class_home.html',context)
