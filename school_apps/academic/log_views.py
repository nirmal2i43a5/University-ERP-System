from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from .models import Assignment, Routine, Syllabus
from student_management_app.models import Subject, Semester, Section
from django.utils.encoding import force_text

# from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION


def academic_logs(request):
    assignments_logs = Assignment.history.all()
    subjects_logs = Subject.history.all()
    sections_logs = Section.history.all()
    semesters_logs = Semester.history.all()
    routines_logs = Routine.history.all()
    syllabus_logs = Syllabus.history.all()
    context = {
        "title": "Academic Log",
        "assignments_logs": assignments_logs,
        "subjects_logs": subjects_logs,
        "sections_logs": sections_logs,
        "semesters_logs": semesters_logs,
        "routines_logs": routines_logs,
        "syllabus_logs": syllabus_logs,
    }
    return render(request, "academic/loghistory/allhistory.html", context)


def assignment_log(request):
    assignments_logs = Assignment.history.all()
    context = {
        "title": "Assignmen Log",
        "assignments_logs": assignments_logs,
    }
    return render(
        request,
        "academic/loghistory/individuals/assignment.html",
        context)


def semester_log(request):
    semesters_logs = Semester.history.all()
    context = {
        "title": "Semester Log",
        "semesters_logs": semesters_logs,
    }
    return render(
        request,
        "academic/loghistory/individuals/semester.html",
        context)


def subject_log(request):
    subjects_logs = Subject.history.all()
    context = {
        "title": "Subject Log",
        "subjects_logs": subjects_logs,
    }
    return render(
        request,
        "academic/loghistory/individuals/subject.html",
        context)


def section_log(request):
    sections_logs = Section.history.all()
    context = {
        "title": "Section Log",
        "sections_logs": sections_logs,
    }
    return render(
        request,
        "academic/loghistory/individuals/section.html",
        context)


def syllabus_log(request):
    syllabus_logs = Syllabus.history.all()
    context = {
        "title": "Syllabus Log",
        "syllabus_logs": syllabus_logs,
    }
    return render(
        request,
        "academic/loghistory/individuals/syllabus.html",
        context)


def routine_log(request):
    routines_logs = Routine.history.all()
    context = {
        "title": "Routine Log",
        "routines_logs": routines_logs,
    }
    return render(
        request,
        "academic/loghistory/individuals/routine.html",
        context)
