import datetime
from datetime import datetime as date1
import json
from django.db.models import fields
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from student_management_app.models import Semester, Student, Parent
from school_apps.courses.models import (
    Exams,
    application_form,
    studentgrades,
    Subject,
    selectedcourses,
    Term,
)
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.utils.html import format_html
from django.views.decorators.csrf import csrf_exempt


class SubjectNotFound(Exception):
    pass


class TermNotFound(Exception):
    pass


class ApplicationNotFound(Exception):
    pass


student = Student.objects.none()


def index(request):
    student = get_object_or_404(Student, student_user=request.user.id)
    return render(request, "student/index.html", {"student": student})


def checkscore(request):
    student = get_object_or_404(Student, student_user=request.user.id)
    applications = application_form.objects.filter(student=student)
    terms = []

    for item in applications:
        terms.append(item.term)

    terms_set = set(terms)
    terms = list(terms_set)
    print(terms, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    context = {"student": student, "terms": terms}

    return render(request, "student/checkscore.html", context)


def selectcourse(request):
    student = get_object_or_404(Student, student_user=request.user.id)
    courses_remove = selectedcourses.objects.all().filter(student_id=student)
    subject_list = Subject.objects.all()
    for course in courses_remove:
        subject_list = subject_list.exclude(
            subject_id=course.subject_id.subject_id)

    return render(
        request,
        "student/selectcourse.html",
        {"student": student, "courses": subject_list},
    )


def registerexam(request):
    student = get_object_or_404(Student, student_user=request.user.id)
    if request.method == "GET":
        courses = selectedcourses.objects.all().filter(student_id=student)
        exam = Exams.objects.all()
        returnobject = Exams.objects.none()
        for course in courses:
            exam_toadd = exam.filter(subject_id=course.subject_id)
            returnobject = returnobject | exam_toadd

        removeexams = studentgrades.objects.all().filter(student_id=student)
        for exams in removeexams:
            returnobject = returnobject.exclude(exam_id=exams.exam_id.exam_id)
        return render(
            request,
            "student/registerexam.html",
            {"exam": returnobject, "student": student},
        )
    else:
        examid = request.POST["exam"]
        exam = get_object_or_404(Exams, exam_id=examid)
        objectdata = studentgrades(
            student_id=student,
            exam_id=exam,
            marks=-1,
            semester=student.semester)
        objectdata.save()
        messages.success(
            request,
            "Exam " +
            exam.exam_title +
            " register successful.")
        return HttpResponseRedirect(reverse("home"))


def examapplication(request):
    student = get_object_or_404(Student, student_user=request.user.id)
    today = datetime.date.today()
    # latest_term = Term.objects.none
    latest_term = Term.objects.latest("start_date")
    try:
        latest_term = Term.objects.latest("start_date")
    except BaseException:
        print("no term")
        return render(
            request,
            "student/examapplication.html",
            {
                "student": student,
            },
        )

    current_application = application_form.objects.none()

    if (
        datetime.timedelta(0)
        <= latest_term.start_date - today
        <= datetime.timedelta(15)
    ):
        try:
            current_application = application_form.objects.get(
                student=student, term=latest_term
            )
        except BaseException:
            print("Application not found.")
            selected_subjects = selectedcourses.objects.filter(
                Q(student_id=student) & Q(semester=student.semester)
            )
            print(selected_subjects)
            exams = []

            for subject in selected_subjects:
                try:
                    exams.append(
                        Exams.objects.get(
                            Q(term=latest_term) & Q(subject_id=subject.subject_id)
                        )
                    )
                except BaseException:
                    print(subject.__str__() + " exam not found")
            print(exams)
            return render(
                request,
                "student/examapplication.html",
                {"student": student, "term": latest_term, "exams": exams},
            )

        if current_application:
            print("in try")
            selected_subjects = selectedcourses.objects.filter(
                Q(student_id=student) & Q(semester=student.semester)
            )
            current_exams = current_application.exam.all()
            print("selected subjects", selected_subjects)
            print("current_exams=" + str(current_exams))
            exams = []

            for subject in selected_subjects:
                try:
                    exams.append(
                        Exams.objects.get(
                            Q(term=latest_term) & Q(subject_id=subject.subject_id)
                        )
                    )
                except BaseException:
                    messages.error(request, "Something went wrong.")
                    # return HttpResponseRedirect(reverse('home'))

            for exam in current_exams:
                if exam in exams:
                    exams.remove(exam)

            return render(
                request,
                "student/examapplication.html",
                {
                    "student": student,
                    "term": latest_term,
                    "exams": exams,
                    "already_selected": current_exams,
                },
            )
    else:
        print("nothing")
        return render(request,
                      "student/examapplication.html",
                      {"student": student})


def examslist(request):
    student = get_object_or_404(Student, student_user=request.user.id)
    term_id = request.GET.get("term_id")
    term = get_object_or_404(Term, pk=term_id)
    selected_subjects = selectedcourses.objects.filter(student_id=student)
    exams = Exams.objects.filter(term=term)
    exams_list = []

    for subject in selected_subjects:
        exam_item = exams.filter(subject_id=subject.subject_id)
        if exam_item.exists():
            exams_list.append(exam_item.last())

    return render(
        request, "student/examslist.html", {"exams": exams_list, "term": term}
    )


def examdetails(request):
    student = get_object_or_404(Student, student_user=request.user.id)
    """I commented this to show term directly w/o application_form process"""
    # applications = application_form.objects.filter(student=student)
    # terms = []

    # for item in applications:
    #     terms.append(item.term)

    # terms_set = set(terms)
    # terms = list(terms_set)
    terms = Term.objects.all()

    print(terms, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    context = {"student": student, "terms": terms}
    return render(request, "student/examdetails.html", context)


def viewcourses(request):
    student = get_object_or_404(Student, student_user=request.user.id)
    SEM_CHOICES = [(r) for r in range(1, student.semester.semester_value + 1)]
    courses = selectedcourses.objects.all().filter(student_id=student)
    return render(
        request,
        "student/viewcourses.html",
        {"courses": courses, "student": student, "semesters": SEM_CHOICES},
    )


def postCourses(request):
    student = get_object_or_404(Student, student_user=request.user.id)
    semester = request.GET.get("semester")
    courses_data = (
        selectedcourses.objects.all()
        .filter(student_id=student)
        .filter(semester=semester)
    )
    context = {"courses": courses_data}
    return render(request, "student/courseslist.html", context)


def postGrades(request):
    student = get_object_or_404(Student, student_user=request.user.id)
    term = Term.objects.get(pk=request.GET.get("term"))
    is_published = True
    if term.is_published:
        grades_data = studentgrades.objects.filter(
            Q(application_id__student_id=student)
            & Q(application_id__term=term)
            & ~Q(marks=-1)
        )
        remaining = studentgrades.objects.filter(
            Q(application_id__student_id=student)
            & Q(application_id__term=term)
            & Q(marks=-1)
        )
        context = {
            "records": grades_data,
            "remaining": remaining,
            "is_published": is_published,
        }
        return render(request, "student/grades.html", context)
    else:
        is_published = False
        context = {"is_published": is_published}
        return render(request, "student/grades.html", context)


def postExams(request):
    student = get_object_or_404(Student, student_user=request.user.id)
    term = Term.objects.get(pk=request.GET.get("term"))
    # exams_data = studentgrades.objects.all().filter(Q(application_id__student_id = student)& Q(application_id__term=term))
    exams_data = term.exams_set.all()
    print(exams_data)
    return render(request, "student/exams.html", {"exams": exams_data})


def testexamAjax(request):
    student = get_object_or_404(Student, student_user=request.user.id)
    exam_data = request.GET.get("exams")
    exams = json.loads(exam_data)
    print(exams)
    exams_list = []
    i = 0
    while i < len(exams):
        exams_list.append(get_object_or_404(Exams, pk=exams[str(i)]))
        i += 1

    for exam in exams_list:
        if (
            (studentgrades.objects.filter(application_id__student_id=student))
            .filter(exam_id__subject_id=exam.subject_id)
            .exists()
        ):
            exam.type = "Chance"
        else:
            exam.type = "Regular"
    return render(request, "student/selectedexams.html", {"exams": exams_list})


def confirmexamAjax(request):
    student = get_object_or_404(Student, student_user=request.user.id)
    exam_data = request.GET.get("exam_data")
    exams = json.loads(exam_data)
    exams_list = []
    i = 0
    while i < len(exams):
        exams_list.append(get_object_or_404(Exams, pk=exams[str(i)]))
        i += 1

    for exam in exams_list:
        exam_check = (
            (studentgrades.objects.filter(application_id__student_id=student))
            .filter(exam_id__subject_id=exam.subject_id)
            .exists()
        )
        obj = application_form(
            student=student,
            exam=exam,
            exam_type="CHA" if exam_check else "REG")
        obj.save()

    return JsonResponse({"a": "b"})


def addAjax(request):
    print("---call ajax=========")
    student = get_object_or_404(Student, student_user=request.user.id)
    search_string = request.GET.get("search_string")
    print(search_string)
    course_list = []
    course_all = Subject.objects.all()
    for course in course_all:
        if search_string in course.subject_id:
            course_list.append(course)

    selected_courses = selectedcourses.objects.filter(student_id=student)
    a_list = []
    for course in selected_courses:
        a_list.append(course.subject_id)

    final_list = list(set(course_list) - set(a_list))

    return render(request,
                  "student/courseaddlist.html",
                  {"courses": final_list})


def confirmAjax(request):
    student = get_object_or_404(Student, student_user=request.user.id)
    course_code = request.GET.get("course_id")
    student_object = student
    course_object = get_object_or_404(Subject, subject_id=course_code)

    to_add = selectedcourses(
        subject_id=course_object,
        student_id=student_object,
        year=date1.now().year,
        semester=student_object.semester,
    )
    to_add.save()
    return HttpResponseRedirect(reverse("student:addcourse"))


def login(request):
    return render(request, "student/login.html")


def viewform(request):
    student = get_object_or_404(Student, student_user=request.user.id)
    term = get_object_or_404(Term, pk=request.POST["term"])
    count = int(request.POST["count"])
    exams = []
    i = 0

    while i < count:
        exams.append(get_object_or_404(Exams, pk=request.POST[str(i)]))
        i += 1

    print("exams", exams)

    context = {"term": term, "student": student, "exams": exams}
    return render(request, "student/view_form.html", context)


def student_application(request):
    student = get_object_or_404(Student, student_user=request.user.id)
    term = get_object_or_404(Term, pk=request.POST["term"])
    count = int(request.POST["count"])
    print(count, "::::::::::::::::::::::::::;;")
    app_id = request.POST["application_id"]
    exams = []
    i = 0

    app_obj = application_form(
        application_id=app_id,
        student=student,
        term=term,
        semester=student.semester)

    if application_form.objects.filter(application_id=app_id).exists():
        while i < count:
            exams.append(get_object_or_404(Exams, pk=request.POST[str(i)]))
            i += 1

        print(exams)
        for item in exams:
            if item not in app_obj.exam.all():
                print(str(item))
                """I make this passed = true as I dont want admin to verify for appliation form """
            app_obj.exam.add(
                item, through_defaults={"exam_type": True, "passed": True}
            )  #

        app_obj.save()

        messages.success(
            request,
            'Application successful. <a href="printapplicationform">Test link</a><br>Or access the page from sidebar.',
            extra_tags="safe",
        )
        return HttpResponseRedirect(reverse("home"))
    else:
        app_obj.save()

        while i < count:
            exams.append(get_object_or_404(Exams, pk=request.POST[str(i)]))
            i += 1

        for item in exams:
            app_obj.exam.add(
                item, through_defaults={
                    "exam_type": True, "passed": True})

        app_obj.save()

        messages.success(
            request,
            'Application successful. Print form <a href="printapplicationform">here</a>',
            extra_tags="safe",
        )
        return HttpResponseRedirect(reverse("home"))


def printresults(request, form_id):
    # student = get_object_or_404(Student, student_id = request.session['user_id'])
    form = get_object_or_404(application_form, pk=form_id)
    grades = studentgrades.objects.filter(application_id=form)
    print(form)
    context = {"form": form, "grades": grades}
    return render(request, "student/print_results.html", context)


def printadmitcard(request):
    latest_term = Term.objects.latest("start_date")
    print(latest_term)
    student = get_object_or_404(Student, student_user=request.user.id)

    try:
        application = application_form.objects.get(
            Q(term=latest_term) & Q(student=student) & Q(status=True)
        )
        grades = studentgrades.objects.filter(application_id=application)
        context = {"student": student, "form": application, "grades": grades}
        print("True")
        return render(request, "student/print_admitcard.html", context)
    except BaseException:
        print("False")
        return render(request, "student/print_admitcard.html")


def printapplicationform(request):
    latest_term = Term.objects.latest("start_date")
    print(latest_term)
    student = get_object_or_404(Student, student_user=request.user.id)

    try:
        # application=application_form.objects.get(Q(term=latest_term)&Q(student=student)&Q(status=True))
        application = application_form.objects.get(
            Q(term=latest_term) & Q(student=student) & Q(status=False)
        )
        grades = studentgrades.objects.filter(application_id=application)
        context = {"student": student, "form": application, "grades": grades}
        print("True")
        return render(request, "student/print_applicationform.html", context)
    except BaseException:
        print("False")
        return render(request, "student/print_applicationform.html")


# def show_routine(request):
#     student = get_object_or_404(Student, student_user = request.user.id)
#     semester = request.GET.get('semester')
#     selected_courses = selectedcourses.objects.filter(Q(student_id=student)&Q(semester=semester))
#     selected_routine = routine.objects.none()
#     for item in selected_courses:
#         selected_routine =selected_routine|routine.objects.filter(Q(subject=item.subject_id)&Q(semester=semester))
#     selected_routine=selected_routine.order_by('day','period')
#     print(selected_routine)

#     context = {
#         'routine':selected_routine
#     }
#     return render(request, 'student/routine.html', context)


def logout(request):
    del request.session["user_id"]
    return render(request, "student/login.html")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# parent views#
def parent_checkscore(request):
    parent = get_object_or_404(Parent, parent_user=request.user.id)
    student = Student.objects.filter(guardian=parent)

    if request.method == "GET":
        context = {
            "student": student,
        }
        return render(request, "parent/checkscore.html", context)
    else:
        application = application_form.objects.get(
            Q(
                student=Student.objects.get(
                    student_user__username=request.POST["student"]
                )
            )
            & Q(term=Term.objects.get(pk=request.POST["term"]))
        )
        # grades = studentgrades.objects.filter(application_id=application)

        grades_data = studentgrades.objects.filter(
            Q(application_id=application) & ~Q(marks=-1)
        )
        remaining = studentgrades.objects.filter(
            Q(application_id=application) & Q(marks=-1)
        )

        context = {
            "student": student,
            "records": grades_data,
            "remaining": remaining}

        return render(request, "parent/checkscore.html", context)


def returnExamslist(request):
    student = Student.objects.get(
        student_user__username=request.GET["student"])
    applications = application_form.objects.filter(student=student)

    termlist = []

    for item in applications:
        termlist.append(item.term)

    context = {"terms": termlist}
    return render(request, "parent/termslist.html", context)


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    student_email = Student.objects.filter(student_user__email=email).exists()
    if student_email:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


# def student_ajax_autocomplete(request):
#     students = Student.objects.filter(student_user__username__contains = request.GET['student'])
#     context = {'students': students}
# return render(request, "students/student_ajax_autocomplete.html",
# context)


def student_ajax_autocomplete(request):
    stu_id = request.GET.get("student")
    student_datas = []
    if stu_id:
        students = Student.objects.filter(stu_id__icontains=stu_id)

        for student in students:
            # image_url = student.image.url if student.image else None
            # student_data = {
            #                 'image':image_url,
            #                 'stu_id':student.stu_id,
            #                 'name': student.student_user.full_name,
            #                   'class': student.semester.name,
            #                      'program': student.course.course_name,
            #                 }
            student_datas.append(student.stu_id)

    # import json
    # response_data = json.dumps(student_datas)

    return JsonResponse({"status": 200, "data": student_datas})
