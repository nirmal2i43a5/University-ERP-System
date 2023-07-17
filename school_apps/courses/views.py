from json.encoder import JSONEncoder
from schedule import context_processors
from django import forms
from django.db.models import Q
from django.http.response import HttpResponse, JsonResponse
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from student_management_app.models import (
    CourseCategory,
    Section,
    Semester,
    Staff,
    Student,
    Subject,
    SubjectTeacher,
)
from .models import Term, application_form, selectedcourses, studentgrades, term_ranking
from .models import Exams
from school_apps.academic.forms import StudentFormSearch
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import ExamsForm, TermForm, CourseForm, DepartmentForm
from student_management_app.models import Staff, Course
from school_apps.attendance.models import Attendance, AttendanceReport
import datetime
from datetime import datetime as dtime
import csv
from django.contrib.auth.models import Group

from django.contrib.auth.decorators import permission_required



def index(request):
    return render(request, "courses/index.html")

@permission_required("courses.add_term",
                     raise_exception=True)
def addterm(request):
    term_form = TermForm()
    if request.method == "POST":
        formdata = TermForm(request.POST)
        print(formdata)
        if formdata.is_valid():
            # formdata.save(commit=False)
            # formdata.course_category = request.user.adminuser.course_category
            formdata.save()
            messages.success(request, "Term info added.")
            return HttpResponseRedirect(reverse("courses:addterm"))
        else:
            messages.error(
                request,
                "Term Information info invalid. Please check your information and try again.",
            )
            return render(request, "courses/addterm.html", {"form": term_form})
    else:
        return render(request, "courses/addterm.html", {"form": term_form})


def editterm(request):
    pass


@permission_required("courses.view_term",
                     raise_exception=True)
def viewterm(request):
    terms = Term.objects.all()

    context = {"terms": terms}
    return render(request, "courses/viewterm.html", context)


@permission_required("courses.view_exams",
                     raise_exception=True)
def checkterm_exams(request, pk):
    term = Term.objects.get(pk=pk)
    exams = Exams.objects.filter(term=term)

    context = {"exams": exams, "term": term}

    return render(request, "courses/checkterm_exams.html", context)


@permission_required("courses.add_exams",
                     raise_exception=True)
def addexam(request):
    subjects = Subject.objects.all()
    # classes = Class.objects.all
    exam_form = ExamsForm

    if request.method == "POST":
        examinfo = ExamsForm(request.POST)
        print(examinfo)
        if examinfo.is_valid():
            examinfo.save()
            messages.success(request, "Exam info added.")
            return HttpResponseRedirect(reverse("courses:addexam"))
        else:
            messages.error(
                request,
                "Exam info invalid. Please check your information and try again.",
            )
            return render(request, "courses/addexam.html", {"form": exam_form})
    else:
        return render(request, "courses/addexam.html",
                      {"subject": subjects, "form": exam_form})


def editexam(request):
    pass


def addexam_marks_ajax(request):
    term = Term.objects.get(pk=request.GET["term"])
    pass_marks = 40
    full_marks = 100
    if term.type == "Unit":
        pass_marks = 10
        full_marks = 25
    return JsonResponse({"p_marks": pass_marks, "f_marks": full_marks})


def get_result_of_each_subject(request):
    today = datetime.date.today()
    # exams = Exams.objects.all()
    terms = Term.objects.all()
    semesters = Semester.objects.all()
    subjects = Subject.objects.all()
    sections = Section.objects.all()
    courses = Course.objects.all()

    # for viewresult part
    if request.method == "POST":
        subject_id = request.POST["subject"]
        semester_id = request.POST["semester"]
        # section_id = request.POST['section']
        term_id = request.POST["term"]
        subject_instance = (
            get_object_or_404(Subject, pk=subject_id) if subject_id else None
        )
        semester_instance = (
            Semester.objects.get(pk=semester_id) if semester_id else None
        )
        # section_instance = Section.objects.get(pk = section_id) if section_id else None

        term_instance = get_object_or_404(
            Term, pk=term_id) if term_id else None
        results = studentgrades.objects.filter(
            term=term_instance, subject=subject_instance
        ).order_by("-marks")
        context = {
            "terms": terms,
            "results": results,
            "term_instance": term_instance,
            "subject_instance": subject_instance,
            "semester_instance": semester_instance,
            # 'section_instance':section_instance,
            "classes": semesters,
            "subjects": subjects,
            "sections": sections,
            "courses": courses,
        }
        return render(request, "courses/publishresults.html", context)

    else:
        return render(
            request,
            "courses/publishresults.html",
            {
                "terms": terms,
                "courses": courses,
                "classes": semesters,
                "subjects": subjects,
                "sections": sections,
            },
        )


def get_results_of_all_subjects(request):
    today = datetime.date.today()
    terms = Term.objects.all()
    semesters = Semester.objects.all()
    subjects = Subject.objects.all()
    sections = Section.objects.all()
    courses = Course.objects.all()

    # for viewresult part
    if request.method == "POST":
        subject_id = request.POST.get("subject")
        semester_id = request.POST.get("semester")
        section_id = request.POST.get("section")
        term_id = request.POST.get("term")
        subject_instance = (
            get_object_or_404(Subject, pk=subject_id) if subject_id else None
        )
        semester_instance = (
            Semester.objects.get(pk=semester_id) if semester_id else None
        )
        section_instance = Section.objects.get(
            pk=section_id) if section_id else None
        subjects = Subject.objects.filter(semester=semester_instance)

        term_instance = get_object_or_404(
            Term, pk=term_id) if term_id else None

        group = Group.objects.get(name="Student")
        student_role = request.user.groups.filter(name=group)
        if student_role.exists():
            results = studentgrades.objects.filter(
                term=term_instance, student=request.user.student
            ).select_related("student", "subject")
        else:
            results = studentgrades.objects.filter(
                term=term_instance).select_related(
                "student", "subject")

        # Create a dictionary to map subject IDs to their indexes
        subject_indexes = {
            subject.subject_id: idx for idx, subject in enumerate(subjects)
        }

        students_data = {}

        for result in results:
            student_name = result.student.student_user.full_name
            student_id = result.student.stu_id
            subject_id = result.subject_id
            marks = result.marks

            if student_name not in students_data:
                students_data[student_name] = {
                    "total_marks": 0,
                    "student_id": student_id,
                    "subject_marks": [None] * len(subjects),
                }

            subject_index = subject_indexes.get(subject_id)
            if subject_index is not None:
                students_data[student_name]["subject_marks"][subject_index] = marks
                students_data[student_name]["total_marks"] += marks if marks else 0
        print(students_data)
        # Calculate student ranks based on total marks
        students_sorted = sorted(
            students_data.items(),
            key=lambda x: x[1]["total_marks"],
            reverse=True)
        rank = 1
        for student, data in students_sorted:
            data["rank"] = rank
            rank += 1

        context = {
            "terms": terms,
            "students_data": students_data,
            "term_instance": term_instance,
            "subject_instance": subject_instance,
            "semester_instance": semester_instance,
            "section_instance": section_instance,
            "classes": semesters,
            "subjects": subjects,
            "sections": sections,
            "courses": courses,
        }

        return render(
            request,
            "courses/all_subjects_publishresults.html",
            context)
    else:
        return render(
            request,
            "courses/all_subjects_publishresults.html",
            {
                "terms": terms,
                "courses": courses,
                "classes": semesters,
                "subjects": subjects,
                "sections": sections,
            },
        )


def viewresults(request):
    selectedexam = get_object_or_404(Exams, exam_id=request.GET["exam"])
    results = studentgrades.objects.filter(
        exam_id=selectedexam).order_by("-marks")
    return render(request, "courses/results.html",
                  {"results": results, "exam": selectedexam})


@permission_required("courses.change_term",
                     raise_exception=True)
def publishresults(request):
    terms = Term.objects.all()
    return render(request, "courses/publishtermresults.html", {"terms": terms})



@permission_required("courses.change_term",
                     raise_exception=True)
def toggle_results(request, pk):
    terms = Term.objects.all()
    selected_term = Term.objects.get(pk=pk)

    if selected_term.is_published:
        selected_term.is_published = False
        selected_term.created_at = datetime.datetime.now()
        selected_term.save()
        messages.error(request, "Result publish is undo.")
        return redirect("courses:publishresults")
    else:
        selected_term.is_published = True
        selected_term.created_at = datetime.datetime.now()
        selected_term.save()
        messages.success(request, "Result is successfully published.")
        return redirect("courses:publishresults")

    # return render(request, 'courses/publishtermresults.html',
    # {'terms':terms})


def examtoppers(request):
    today = datetime.date.today()
    # filter(date__lte=today, term__course_category=request.user.adminuser.course_category)
    exams = (Exams.objects.all())
    if request.method == "GET":
        return render(request, "courses/examtoppers.html", {"exams": exams})
    else:
        selected_exam = get_object_or_404(
            Exams, exam_id=request.POST["exam_id"])
        studentrecords = (
            studentgrades.objects.filter(exam_id=selected_exam)
            .exclude(marks=-1)
            .order_by("-marks")[0:3]
        )
        selected_object = request.POST["exam_id"]
        return render(
            request,
            "courses/examtoppers.html",
            {
                "students": studentrecords,
                "exams": exams,
                "selected_exam": selected_exam,
            },
        )


def addstudentmarks(request):
    return render(request, "courses/addstudentmarks.html")


def studentsAjax(request):
    print("test")
    student_id = request.GET.get("student_id")
    student_list = []
    student_all = Student.objects.all()

    for student in student_all:
        if student_id in student.student_user.username:
            student_list.append(student)

    return render(request,
                  "courses/studentlist.html",
                  {"students": student_list})


def studentsmarksentry(request, id):
    student = get_object_or_404(Student, student_user__username=id)
    today = datetime.date.today()
    exams = studentgrades.objects.all().filter(
        Q(application_id__student=student)
        & Q(exam_id__date__lte=today)
        & Q(exam_id__term__course_category=request.user.adminuser.course_category)
    )
    return render(request, "courses/studentmarksentry.html",
                  {"student": student, "exams": exams})


@permission_required("courses.add_studentgrades",
                     raise_exception=True)
def submitscores(request):
    student = get_object_or_404(
        Student, student_user__username=request.POST["student_id"]
    )
    exams = studentgrades.objects.filter(application_id__student=student)

    for exam in exams:
        student_object = student
        exam_object = exam.exam_id
        marks = int(request.POST[exam.exam_id.exam_title])
        test = studentgrades.objects.filter(
            application_id__student=student_object, exam_id=exam_object
        )
        if test.exists():
            editobject = studentgrades.objects.get(
                application_id__student=student_object, exam_id=exam_object
            )
            if request.POST[exam.exam_id.exam_title]:
                editobject.marks = marks
            else:
                pass
            editobject.save()
            messages.success(request, "Marks entry successful.")
            print(messages)
        else:
            if request.POST[exam.exam_id.exam_title]:
                marks = marks
            else:
                marks = 0
            exam_marks = studentgrades(
                application_id__student=student_object,
                exam_id=exam_object,
                marks=marks)
            exam_marks.save()
            messages.success(request, "Marks entry successful.")
            print(messages)

    for item in studentgrades.objects.all():
        item.rank = studentgrades.objects.filter(
            marks__gt=item.marks).count() + 1
        item.save()

    return HttpResponseRedirect(reverse("home"))


def confirmexamapplication(request):
    return render(request, "courses/confirmexamapplication.html")


def confirmAjax(request):
    form_id = request.GET.get("form_id")
    form = application_form.objects.filter(
        Q(application_id__icontains=form_id),
        Q(status=False),
        Q(term__course_category=request.user.adminuser.course_category),
    )
    print(form, "-----------------")
    return render(request, "courses/examapplication.html", {"form": form})



@permission_required("courses.add_application_form",
                     raise_exception=True)
def confirmapplication(request):
    app_id = request.GET.get("application_radio")
    application = get_object_or_404(application_form, pk=app_id)
    application.status = True
    application.save()

    messages.success(request, "Registration confirmed.")
    return HttpResponseRedirect(reverse("home"))


def bulkprintadmitcard(request):
    latest_term = Term.objects.latest("start_date")
    applications = application_form.objects.filter(term=latest_term)

    context = {"applications": applications}
    return render(request, "courses/bulkprintadmitcard.html", context)


def returnexamdropdown(request):
    term = get_object_or_404(Term, pk=request.GET.get("term_id"))
    exams = Exams.objects.filter(term=term)

    context = {"exams": exams}
    return render(request, "courses/showexamdropdown.html", context)


def return_exams_admit(request):
    search_string = request.GET.get("exam_id")
    exams = Exams.objects.filter(exam_id__icontains=search_string)

    return render(request, "courses/showexamlist_admit.html", {"exams": exams})


def returnstudentlist_admit(request):
    applications = application_form.objects.filter(
        exam=get_object_or_404(Exams, pk=request.GET.get("exam_id"))
    ).filter(status=True)

    context = {
        "applications": applications,
        "exam": get_object_or_404(Exams, pk=request.GET.get("exam_id")),
    }
    return render(request, "courses/showadmitcardlist.html", context)


def printadmitcards(request):
    count = int(request.POST.get("count"))
    i = 1
    applications = []
    while i <= count:
        applications.append(
            get_object_or_404(application_form, pk=request.POST.get(str(i)))
        )
        i += 1

    gradeinfo = studentgrades.objects.none()

    for item in applications:
        gradeinfo = gradeinfo | (
            studentgrades.objects.filter(
                application_id=item))

    print(str(gradeinfo) + "\n___________________________________________")

    context = {"applications": applications, "gradeinfo": gradeinfo}
    return render(request, "courses/showbulkprintadmit.html", context)


# ----------------------------------------------------------------------------------------------------------------------

# bulk print results#


def bulkprintresults(request):
    terms = Term.objects.filter(
        course_category=request.user.adminuser.course_category)
    semester = Semester.objects.all()
    applications = application_form.objects.none()

    if request.method == "POST":
        applications = application_form.objects.filter(
            term=request.POST["term_id"],
            student_id__semester=request.POST["semester_id"],
        )

    context = {
        "applications": applications,
        "terms": terms,
        "semester": semester}
    return render(request, "courses/bulkprintresults.html", context)


def return_exams_results(request):
    search_string = request.GET.get("exam_id")
    exams = Exams.objects.filter(exam_id__icontains=search_string)

    return render(request,
                  "courses/showexamlist_results.html",
                  {"exams": exams})


def returnstudentlist_results(request):
    applications = application_form.objects.filter(
        exam=get_object_or_404(Exams, pk=request.GET.get("exam_id"))
    ).filter(status=True)

    context = {
        "applications": applications,
        "exam": get_object_or_404(Exams, pk=request.GET.get("exam_id")),
    }
    return render(request, "courses/showresultslist.html", context)


def printresults(request):
    count = int(request.POST.get("count"))

    # -----------------------------------------------------------------------------------------------------------------
    # retrieve applications and grades
    i = 1
    applications = []
    all_exams = []
    print(request, list(request.POST.items()), "\n")
    while i <= count:
        # print('applications' , request.POST.get(str(i)) , '\n')
        # applications.append(get_object_or_404(application_form, pk=request.POST.get(str(i))))
        applications.append(
            application_form.objects.get(
                pk=request.POST.get(
                    str(i))))
        i += 1

    gradeinfo = studentgrades.objects.none()
    for item in applications:
        gradeinfo = gradeinfo | (
            studentgrades.objects.filter(
                application_id=item))
        all_exams.append(item.exam.all())

    list1 = []
    for item in all_exams:
        for sub_item in item:
            list1.append(sub_item)

    set_exams = set(list1)
    unique_exams = list(set_exams)
    print("\n here", unique_exams)
    highest_obtained = {}
    test = []

    for item in unique_exams:
        highest_obtained[item] = (
            studentgrades.objects.filter(exam_id=item).latest("marks").marks
        )

    print(highest_obtained)

    total_rank = []
    for item in applications:
        total_rank.append(
            term_ranking.objects.get(student=item.student, term=item.term)
        )

    # -----------------------------------------------------------------------------------------------------------------
    # retrieve attendance

    from_date = dtime.strptime(request.POST.get("from"), "%Y-%m-%d")
    to_date = dtime.strptime(request.POST.get("to"), "%Y-%m-%d")
    daterange = pd.date_range(from_date, to_date)
    no_of_days = to_date - from_date
    no_of_sat = 0
    # print(from_date, to_date ,no_of_days.days, type(from_date), "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    for item in daterange:
        # print(item.date(), type(item.date()), item.date().strftime('%a'), '\n')
        if item.date().strftime("%a") == "Sat":
            no_of_sat += 1

    total_working_days = no_of_days.days - no_of_sat

    student_list = []

    for item in applications:
        student_list.append(item.student)

    attendance_list = {}

    attendance = Attendance.objects.filter(
        attendance_date__range=(from_date, to_date),
    )

    for item in applications:
        student_attendance = AttendanceReport.objects.filter(
            student=item.student, attendance__in=attendance
        )  # or filter(student = student_id, attendance__attendance_date = month)
        total_present = AttendanceReport.objects.filter(
            student=item.student, attendance__in=attendance, status="Present"
        ).count()
        attendance_list[item.student] = total_present

    # -----------------------------------------------------------------------------------------------------------------
    # retrieve best grades

    best_grades = {}
    for item in applications:
        item_bestgrades = studentgrades.objects.none()
        item_bestgrades = item_bestgrades | (
            studentgrades.objects.filter(application_id=item)
            .exclude(grade="Abs")
            .exclude(grade="U")
            .order_by("-marks")[:3]
        )

        bestgrades_str = ""
        for b_item in item_bestgrades:
            bestgrades_str += b_item.grade + "  "

        best_grades[item.student] = bestgrades_str

    # -----------------------------------------------------------------------------------------------------------------
    # fintal results
    final_result = {}
    for students in gradeinfo.values_list(
            "application_id__student").distinct():
        grades = gradeinfo.filter(application_id__student=students)

        if False in grades.values_list("passed", flat=True):
            final_result[Student.objects.get(pk=students[0])] = "Failed"
        else:
            final_result[Student.objects.get(pk=students[0])] = "Passed"
    print(final_result)

    today = datetime.date.today()

    context = {
        "applications": applications,
        "gradeinfo": gradeinfo,
        "total_rank": total_rank,
        "attendance_list": attendance_list,
        "total_days": total_working_days,
        "best_grades": best_grades,
        "final_result": final_result,
        "highest_obtained": highest_obtained,
        "today": today,
    }
    return render(request, "courses/gci_printresults.html", context)


def examreport(request):
    terms = Term.objects.all()
    if request.method == "GET":
        context = {"terms": terms}
        return render(request, "courses/examreport.html", context)
    else:
        exam = Exams.objects.get(pk=request.POST["exam"])
        results = studentgrades.objects.filter(exam_id=exam).order_by("-marks")
        print(results)
        context = {"terms": terms, "results": results, "selectdexam": exam}
        return render(request, "courses/examreport.html", context)


def returnexamlist_Ajax(request):
    term = Term.objects.get(pk=request.GET["term"])
    exams = Exams.objects.filter(term=term)

    context = {"exams": exams}
    return render(request, "courses/examlist.html", context)


def printexamreport(request, pk):
    exam = Exams.objects.get(pk=pk)
    results = studentgrades.objects.filter(exam_id=exam).order_by("-marks")

    context = {"results": results, "exam": exam}

    return render(request, "courses/printexamreport.html", context)


# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# add exam marks

@permission_required("courses.add_studentgrades",
                     raise_exception=True)
def addexammarks(request):
    terms = (
        Term.objects.all()
    )  # filter(course_category=request.user.adminuser.course_category)
    semesters = Semester.objects.all()
    subjects = Subject.objects.all()
    sections = Section.objects.all()
    courses = Course.objects.all()
    if request.user.groups.filter(name="Teacher").exists():
        course_category = request.user.staff.courses.all()
    elif (
        request.user.is_superuser
        or request.user.groups.filter(name="Super-Admin").exists()
    ):
        course_category = CourseCategory.objects.all()

    print(terms)
    context = {
        "terms": terms,
        "sections": sections,
        "classes": semesters,
        "subjects": subjects,
        "course_category": course_category,
        "courses": courses,
    }

    return render(request, "courses/addexamgrades.html", context)


@permission_required("courses.add_studentgrades",
                     raise_exception=True)
def examsAjax(request):
    section_id = request.GET.get("section_id")
    class_id = request.GET.get("class_id")
    term_id = request.GET.get("term_id")
    term_instance = Term.objects.get(pk=term_id) if term_id else None
    subject_id = request.GET.get("subject_id")
    semester_instance = Semester.objects.get(pk=class_id) if class_id else None
    # section_instance = Section.objects.get(pk =  section_id) if section_id else None
    subject_instance = Subject.objects.get(
        pk=subject_id) if subject_id else None

    students = Student.objects.filter(semester=semester_instance)
    # if not section_id:
    #     students = Student.objects.filter(semester = semester_instance)
    # if  section_id:
    #     students = Student.objects.filter(section = section_instance)

    grades = studentgrades.objects.filter(
        term=term_instance,
        semester=semester_instance,
        subject=subject_instance)

    # selected_exam = get_object_or_404(Exams, exam_id=exam_id)

    # student_data = studentgrades.objects.all()#filter(Q(exam_id=selected_exam))
    # print(student_data)

    return render(
        request,
        "courses/submit_score.html",
        {
            "students": students,
            #   'section_id':section_id,
            "class_id": class_id,
            "term_id": term_id,
            "subject_id": subject_id,
            "studentgrades": grades,
            "term": term_instance,
        }
        #    {'students':student_data, 'term_id':term_id}
    )


def addremarks(request):
    terms = (
        Term.objects.all()
    )  # filter(course_category=request.user.adminuser.course_category)
    semester = (
        Semester.objects.all()
    )  # filter(course_category=request.user.adminuser.course_category)
    sections = Section.objects.all()
    courses = Course.objects.all()
    if request.user.groups.filter(name="Teacher").exists():
        course_category = request.user.staff.courses.all()
    elif (
        request.user.is_superuser
        or request.user.groups.filter(name="Super-Admin").exists()
    ):
        course_category = CourseCategory.objects.all()
    context = {
        "terms": terms,
        "classes": semester,
        "sections": sections,
        "course_category": course_category,
        "courses": courses,
    }

    if request.method == "POST":
        term_id = request.POST["term"]
        term_instance = Term.objects.get(pk=term_id) if term_id else None
        class_id = request.POST["semester"]
        # semester = Semester.objects.get(pk=class_id)
        section_id = request.POST["section"]
        semester_instance = Semester.objects.get(
            pk=class_id) if class_id else None
        section_instance = Section.objects.get(
            pk=section_id) if section_id else None
        if not section_id:
            students = Student.objects.filter(semester=semester_instance)
        if section_id:
            students = Student.objects.filter(section=section_instance)
        context["students"] = students
        context["term"] = term_instance
        return render(request, "courses/addremarks.html", context)

    return render(request, "courses/addremarks.html", context)


def addstudentremarks(request, term_id, student_id):
    # app_form = application_form.objects.get(pk=pk)
    student_instance = Student.objects.get(pk=student_id)
    term_instance = Term.objects.get(pk=term_id)

    grades = studentgrades.objects.filter(
        term=term_instance, student=student_instance)

    context = {
        "student": student_instance,
        "grades": grades,
        "term": term_instance}
    return render(request, "courses/addstudentremarks.html", context)


def editremarks(request, pk):
    student = Student.objects.get(pk=pk)
    remarks = request.GET["remarks"]
    student.remarks = remarks
    student.save()

    return HttpResponseRedirect(reverse("courses:addremarks"))


def editexammarks(request):
    pass


def fill_exam_select(request):
    term = Term.objects.get(term_id=request.GET["term"])
    print(term)
    exams = Exams.objects.filter(term=term)

    context = {"exams": exams}

    return render(request, "courses/examlist.html", context)


@permission_required("courses.add_application_form",
                     raise_exception=True)
def massexamapplication(request):
    terms = Term.objects.filter(
        course_category=request.user.adminuser.course_category)
    section = Section.objects.all()
    faculty = Student._meta.get_field("faculty").choices
    faculty_choices = []

    response = HttpResponse(
        content_type="text/csv",
        headers={
            "Content-Disposition": 'attachment; filename="somefilename.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(["First row", "Foo", "Bar", "Baz"])

    for item in faculty:
        faculty_choices.append(item[0])

    if request.method == "POST":
        selected_term = Term.objects.get(pk=request.POST["term_id"])
        selected_section = Section.objects.get(pk=request.POST["section_id"])
        forms = []

        students = Student.objects.filter(
            section=selected_section,
            faculty=request.POST["group"],
            course_category=request.user.adminuser.course_category,
        )

        for item in students:
            application_id_str = (
                selected_term.term_id + "." + item.student_user.username
            )
            obj, created = application_form.objects.get_or_create(
                student=item,
                term=selected_term,
                application_id=application_id_str,
                semester=item.semester,
            )
            selected_subjects = selectedcourses.objects.filter(student_id=item)
            selected_exams = []
            for sub_item in selected_subjects:
                try:
                    selected_exams.append(
                        Exams.objects.get(
                            term=selected_term,
                            subject_id=sub_item.subject_id,
                            semester=item.semester,
                        )
                    )
                except BaseException:
                    # print(str(sub_item.subject_id) + " exam not found~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    writer.writerow(
                        [selected_term, item, sub_item.subject_id, item.semester]
                    )

            for exam in selected_exams:
                obj.exam.add(
                    exam, through_defaults={"exam_type": True, "passed": False}
                )

            obj.save()

        forms = application_form.objects.filter(
            term=selected_term,
            student__faculty=request.POST["group"],
            student__section=selected_section,
            student__course_category=request.user.adminuser.course_category,
        )
        print("testforms: ", forms, forms.count(), "\n\n")

        context = {
            "terms": terms,
            "section": section,
            "faculty": faculty_choices,
            "forms": forms,
        }
        # return response
        return render(
            request,
            "courses/massexamapplication.html",
            context=context)

    context = {"terms": terms, "section": section, "faculty": faculty_choices}
    return render(request, "courses/massexamapplication.html", context=context)


@permission_required("courses.change_application_form",
                     raise_exception=True)
def toggle_application(request, pk):
    application = application_form.objects.get(pk=pk)
    print(application.status)
    if application.status:
        application.status = False
        application.save()
    else:
        application.status = True
        application.save()

    terms = Term.objects.all()
    section = Section.objects.all()
    faculty = Student._meta.get_field("faculty").choices
    faculty_choices = []

    for item in faculty:
        faculty_choices.append(item[0])

    selected_term = application.term
    group = application.student.faculty
    selected_section = application.student.section

    print(
        selected_term,
        group,
        selected_section,
        "+++++++++++++++++++++++++++++++++++++++++++++",
    )

    forms = application_form.objects.filter(
        term=selected_term,
        student__faculty=group,
        student__section=selected_section)
    print(
        forms,
        "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_",
    )

    context = {
        "terms": terms,
        "section": section,
        "faculty": faculty_choices,
        "forms": forms,
    }
    return render(request, "courses/massexamapplication.html", context=context)


def gci_printresults(request):
    return render(request, "courses/gci_printresults.html")


def fill_section_select(request):
    semester = Semester.objects.get(pk=request.GET["class"])
    sections = Section.objects.filter(semester=semester)
    context = {"section": sections}
    return render(request, "courses/section_list.html", context)
