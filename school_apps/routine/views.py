from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from django.db.models import Q

from school_apps.academic.forms import (SectionWiseFilter)
from school_apps.academic.forms import (RoutineForm,RoutineSearchForm)

from school_apps.academic.models import (Routine)

from django.contrib.auth.decorators import permission_required
from school_apps.notifications.utilities import create_notification


@permission_required('academic.add_routine', raise_exception=True)
def add_routine(request):
    if request.method == 'POST':
        form = RoutineForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                instance = form.save(commit = False)
                instance.save()
                semester = form.cleaned_data['semester']
                section = form.cleaned_data['section']
                
                create_notification(request, post=f'Routine is added for {section}', notification_type=1, 
                                    created_by=request.user,type='routine')
                messages.success(request, "Routine is Added Successfully.")
                return redirect('academic:manage_routine')
        except:
            messages.error(request, "Failed to Add Routine.")
            return redirect('routine:add_routine')

    else:
        form = RoutineForm()

    context = {
        'form': form,
        'title': 'Routine'
    }
    return render(request, "academic/routines/add_routine.html", context)


@permission_required('academic.view_routine', raise_exception=True)
def manage_routine(request):

    routines = Routine.objects.all()
    if request.user.is_superuser:
        search_form = RoutineSearchForm(user = request.user)

    else:
        search_form = RoutineSearchForm(user = request.user)
    semester = request.GET.get('filter_semester')
    section = request.GET.get('section')

    if semester and section:
        search_routines = Routine.objects.filter(semester=semester,section = section)
        context = {'routines': search_routines,
                   'form': RoutineSearchForm(user = request.user,initial = {'semester': semester}),#show selected instance in search form
                   'title': 'Routine'
                   }

        return render(request, 'academic/routines/manage_routine.html', context)
    
    if semester:
        search_routines = Routine.objects.filter(semester=semester)
        context = {'routines': search_routines,
                   'form': RoutineSearchForm(user = request.user,initial = {'semester': semester}),#show selected instance in search form
                   'title': 'Routine'
                   }

        return render(request, 'academic/routines/manage_routine.html', context)

    context = {'form': search_form,
               'routines': routines,
               'title': 'Routine'}
    return render(request, 'academic/routines/manage_routine.html', context)


def view_student_routine(request):
    routine = Routine.objects.filter(semester = request.user.student.semester,section = request.user.student.section).first()
    context = {'routine': routine,
            #    'routines': routines,
               'title': 'Routine'}
    return render(request, 'academic/routines/view_student_routine.html', context)
    
    
@permission_required('academic.edit_routine', raise_exception=True)
def edit_routine(request, routine_id):
    routine = get_object_or_404(Routine, pk=routine_id)
    form = RoutineForm(instance=routine)
    if request.method == 'POST':
        form = RoutineForm(request.POST, request.FILES, instance=routine)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Routine is Edited Successfully  .")
                return redirect('academic:manage_routine')
        except:
            messages.error(request, "Failed To  Edit routine.")
            return redirect('academic:edit_Routine', routine_id)
    context = {
        'form': form,
        'title': 'Routine'

    }
    return render(request, 'academic/routines/edit_routine.html', context)


@permission_required('academic.delete_routine', raise_exception=True)
def delete_routine(request, routine_id):
    Routine.objects.get(id=routine_id).delete()
    return render(request, 'academic/routines/manage_routine.html')
