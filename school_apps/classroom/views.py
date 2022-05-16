from django.shortcuts import render



def class_home(request):
    return render(request, 'classroom/class_home.html')
