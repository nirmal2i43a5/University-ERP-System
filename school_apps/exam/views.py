from django.core.files.base import ContentFile
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from school_apps import exam
from school_apps.exam.forms import (
    QuestionPaperUploadForm, QuestionMark, QuestionGradeForm, StudentDetailsSearch, SubQuestionMark)
from school_apps.exam.models import QuestionPaper, Question, QuestionGrade, AnswerSheet, SubQuestion, SubQuestionGrade
from django.contrib import messages
from student_management_app.models import *
from django.views import View
from school_apps.courses.models import Exams, application_form, studentgrades, Term
from django.forms import inlineformset_factory
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from student_management_app.models import Semester, Section, Subject
from django.forms import modelformset_factory
from django.db import transaction, IntegrityError
from django.template.loader import render_to_string


class QuestionPaperUpload(View):

    def get(self, request, *args, **kwargs):
        form = QuestionPaperUploadForm(user=request.user)
        context = {
            'title': 'Question',
            'form': form
        }
        return render(request, 'exam/teachers/add_question.html', context)

    def post(self, request, *args, **kwargs):
        form = QuestionPaperUploadForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Question Paper is Uploaded SUccessfully.')
            return redirect('exam:question-index')
        context = {
            'title': 'Question',
            'form': form
        }
        return render(request, 'exam/teachers/add_question.html', context)


def qustion_paper_update(request, pk):
    paper_instance = get_object_or_404(QuestionPaper, pk=pk)
    form = QuestionPaperUploadForm(instance=paper_instance,user = request.user)

    if request.method == 'POST':
        form = QuestionPaperUploadForm(
            request.POST, request.FILES, instance=paper_instance,user = request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Question Paper is Updated SUccessfully.')
            return redirect('exam:question-index')
    context = {
        'title': 'Question',
        'paper_instance': paper_instance,
        'form': form
    }
    return render(request, 'exam/teachers/add_question.html', context)


class QuestionListView(View):
    def get(self, request, *args, **kwargs):

        # student_completed_exams = AnswerSheet.objects.filter(student__student_user = request.user.id, questionpaper_status = 'Completed')
        # submitted_questionpaper = []
        # for item in student_completed_exams:
        #     exam_obj = get_object_or_404(Exams, pk = item.exam_id)
        #     submitted_questionpaper.append(exam_obj.questionpaper.pk)#access question(child) from parent instance exam

        # # Exclude questionpaper from student page which is already submitted
        # student_assigned_papers = QuestionPaper.objects.filter(exam__semester = request.user.student.semester, draft = False).\
        #                                                                                 exclude(pk__in = submitted_questionpaper)

        # papers_not_submitted = student_assigned_papers.count()
        question_papers = QuestionPaper.objects.all()
        context = {
            'title': 'Question',
            'question_papers': question_papers,
            # 'submitted_papers':'',
            # 'papers not submitted':papers_not_submitted
        }
        return render(request, 'exam/teachers/question_paper_list.html', context)


# class EachQuestionMarkAdd(View):

#     def get(self, request, questionpaper_id, *args, **kwargs):

#         questionpaper = get_object_or_404(QuestionPaper, pk=questionpaper_id)
#         questions = questionpaper.question_set.all()
#         # form = QuestionMark()
#         form = SubQuestionMarkFormset()

#         context = {
#             'title': 'Mark',
#             'items': form,
#             'questions': questions,
#             'questionpaper': questionpaper
#         }
#         return render(request, 'exam/teachers/add_each_question_mark.html', context)

#     def post(self, request, questionpaper_id,  *args, **kwargs):
#         form = QuestionMark(request.POST, request.FILES)
#         questionpaper_id = request.POST.get('questionpaper_id')
#         questionpaper_instance = get_object_or_404(QuestionPaper, pk=questionpaper_id)

#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.question_paper = questionpaper_instance
#             instance.save()
#             messages.success(
#                 request, 'Question Mark is Uploaded SUccessfully.')
#             return redirect('exam:each-mark-add', questionpaper_id)

#         context = {
#             'title': 'Mark',
#             'form': form
#         }

#         return render(request, 'exam/teachers/add_question.html', context)


def each_question_mark_create(request, questionpaper_id):
    
    SubQuestionFormset = modelformset_factory(SubQuestion, form=SubQuestionMark)
    form = QuestionMark(request.POST or None, request.FILES or None)
    formset = SubQuestionFormset(request.POST or None, request.FILES or None,
                                 queryset=SubQuestion.objects.none(),
                                 prefix='sub_questions')  # prefix is related name for question(fk)
   
    if request.method == "POST":
        questionpaper_instance = get_object_or_404(QuestionPaper, pk=questionpaper_id)
        
        if form.is_valid() and formset.is_valid():
            
            with transaction.atomic():
                """For parent part"""
                question = form.save(commit=False)
                question.question_paper = questionpaper_instance
                question.save() 

                """For Child part"""
            if  question.has_sub_question:
                total_marks = 0
                for subquestion in formset:
                    instance = subquestion.save(commit=False)
                    total_marks +=instance.total_marks
                    instance.question = question
                    instance.save()
                question.total_marks = total_marks
                question.save()
         

            messages.success(request, 'Question Mark is Uploaded SUccessfully.')
            return redirect('exam:each-mark-add', questionpaper_id)
    
    
    # ---For Extra instance only--
    questionpaper = get_object_or_404(QuestionPaper, pk=questionpaper_id)
    questions = questionpaper.question_set.all()

    context = {
        'formset':formset,
        'form':form,
        'title':'Mark',
        'questionpaper':questionpaper,
        'questions':questions
    }
    return render(request, 'exam/teachers/add_each_question_mark.html', context)


class EachQuestionMarkView(View):
    def get(self, request, pk, *args, **kwargs):
        question_instance = get_object_or_404(QuestionPaper, pk=pk)
        question_marks = question_instance.question_set.all()
        # for question in question_marks:
        #     sub_question_instance = get_object_or_404(Question,pk = question)
            
        #     print(question)
        
        context = {
            'title': 'Mark',
            'question_marks': question_marks
        }
        return render(request, 'exam/teachers/eachquestion_mark_show.html', context)


def sub_question_marks_show(request,mainquestion_id):
    print(mainquestion_id)
    main_question_instance = get_object_or_404(Question,pk = mainquestion_id)
    print(main_question_instance)
    sub_questions_marks = main_question_instance.sub_questions.all()
    context = {
            'title': 'Sub Question Mark',
            'sub_questions_marks': sub_questions_marks
        }
    return render(request, 'exam/teachers/subquestion_markshow.html', context)


def qustionpaper_mark_update(request, questionpaperid, pk):
    paper_instance = get_object_or_404(Question, pk=pk)
    
    SubQuestionFormset = modelformset_factory(SubQuestion, form=SubQuestionMark)
    form = QuestionMark(instance=paper_instance)
    formset = SubQuestionFormset(request.POST or None, request.FILES or None,
                                 queryset=SubQuestion.objects.none(),
                                 prefix='sub_questions',
                                 
                                 )  # prefix is related name for question(fk)
    
    # questionpaper = get_object_or_404(QuestionPaper, pk=questionpaperid)
    if request.method == "POST":
        form = QuestionMark(request.POST or None, request.FILES or None,instance=paper_instance)
        
        questionpaper_instance = get_object_or_404(QuestionPaper, pk=questionpaperid)
        
        if form.is_valid() and formset.is_valid():
            
            with transaction.atomic():
                """For parent part"""
                question = form.save(commit=False)
                question.question_paper = questionpaper_instance
                question.save() 

                """For Child part"""
            if  question.has_sub_question:
                total_marks = 0
                for subquestion in formset:
                    instance = subquestion.save(commit=False)
                    total_marks +=instance.total_marks
                    instance.question = question
                    instance.save()
                question.total_marks = total_marks
                question.save()
         

            messages.success(request, 'Question Mark is Uploaded SUccessfully.')
            return redirect('exam:each-mark-add', questionpaperid)
    
    
    # ---For Extra instance only--
    questionpaper = get_object_or_404(QuestionPaper, pk=questionpaperid)
    questions = questionpaper.question_set.all()

    context = {
        'formset':formset,
        'form':form,
        'title':'Mark',
        'questionpaper':questionpaper,
        'questions':questions,
         'paper_instance': paper_instance,
    }
    return render(request, 'exam/teachers/add_each_question_mark.html', context)
 


class StudentQuestionPaperView(View):

    def get(self, request, *args, **kwargs):

        student_completed_exams = AnswerSheet.objects.filter(
            student__student_user=request.user.id, questionpaper_status='Completed')
        submitted_questionpaper = []
        for item in student_completed_exams:
            exam_obj = get_object_or_404(Exams, pk=item.exam_id)
            # access question(child) from parent instance exam
            submitted_questionpaper.append(exam_obj.questionpaper.pk)

        # Exclude questionpaper from student page which is already submitted
        student_assigned_papers = QuestionPaper.objects.filter(exam__semester=request.user.student.semester, draft=False).\
            exclude(pk__in=submitted_questionpaper)

        context = {
            'title': 'Question',
            'exam_papers': student_assigned_papers,
            'student_completed_exams': student_completed_exams
        }
        return render(request, 'exam/students/student_question_paperview.html', context)


class StudentUploadAnswer(View):

    def get(self, request, *args, **kwargs):
        context = {
            'title': 'Upload',
            # 'previous_exam_papers':
        }
        return render(request, 'exam/students/student_upload_answer.html', context)

    def post(self, request, exampk,  *args, **kwargs):
        upload_answer_file = request.FILES['answer_upload']
        student_instance = get_object_or_404(
            Student, student_user=request.user.id)
        print(student_instance)
        answersheet = AnswerSheet(
            exam_id=exampk, student=student_instance, answer_upload=upload_answer_file)
        answersheet.save()

        '''When particular student upload answer then make its questionpaper_status to Completed '''
        exam_question_sheet = AnswerSheet.objects.filter(
            pk=answersheet.pk).first()
        exam_question_sheet.questionpaper_status = 'Completed'
        exam_question_sheet.save()
        # # assignment.student.set([request.user.id])
        messages.success(request, 'Your Answer is submitted successully.')
        return redirect('exam:student-questionpaper-view')


class TeacherViewAnswer(View):
    def get(self, request, examid, *args, **kwargs):
        student_answer_list = AnswerSheet.objects.filter(exam_id=examid)
        
        student_list = []
        for student in student_answer_list:
            student_list.append(student.student)
        
        
        valid_student_list = []
        for item in student_list:
            try:
                application = application_form.objects.get(student = item, term = student_answer_list[0].exam.term)
                valid_student_list.append(item)
            except:
                continue
      
        valid_answer_sheet = AnswerSheet.objects.filter(student__in = valid_student_list,exam_id=examid )#show answersheet only for exam apply students
        print(valid_answer_sheet)
        print(valid_student_list)
        context = {
            'title': 'Student Answer',
            'student_answer_list': valid_answer_sheet,
            
            # 'previous_exam_papers':
        }
        return render(request, 'exam/grades/teacher_view_answer.html', context)

    def post(self, request, exampk,  *args, **kwargs):
        messages.success(request, 'Your Answer is submitted successully.')
        return redirect('exam:student-questionpaper-view')



'''This views is for checking paper uploaded by  student from their respective dashboard'''
class TeacherAddGrade(View):

    def get(self, request, studentid, answerid, *args, **kwargs):
        answer_sheet = get_object_or_404(AnswerSheet, pk=answerid)
        exam_instance = get_object_or_404(Exams, pk=answer_sheet.exam_id)

        grade_form = QuestionGradeForm()
        grade_form.fields['question'].queryset = Question.objects.filter(question_paper__exam=answer_sheet.exam)

        question_marks = QuestionGrade.objects.filter(
            student_id=studentid, question__question_paper__exam=exam_instance)

        question_paper = get_object_or_404(QuestionPaper, exam=exam_instance)
        
        question = Question.objects.filter(question_paper=question_paper)
        sub_question = SubQuestion.objects.none()
        for item in question:
            sub_question = sub_question|SubQuestion.objects.filter(question= item)
            
        # question_grade_marks = QuestionGrade.objects.filter(student=Student.objects.get(pk=studentid))
        # sub_question_grade_marks = SubQuestionGrade.objects.filter(student=Student.objects.get(pk=studentid))
        
        question_grade_marks = QuestionGrade.objects.filter(student=Student.objects.get(pk=studentid), question__question_paper__exam=exam_instance)
        sub_question_grade_marks = SubQuestionGrade.objects.filter(student=Student.objects.get(pk=studentid), sub_question__question__question_paper__exam=exam_instance)
        
        questions = Question.objects.filter(question_paper__exam=exam_instance)
        total_marks = 0
        for item in questions:
            try:
                q_marks = QuestionGrade.objects.get(question=item, student=Student.objects.get(pk=studentid))
                marks = q_marks.marks
                total_marks+= marks
            except:
                print(item,"marks not found")
    

        context = {
            'title': 'Grade',
            'grade_form': grade_form,
            'answer_sheet': answer_sheet,
            'question_marks': question_marks,
            'exam_instance': exam_instance,
            # 'question_and_subquestion':zip(question,sub_question),
            'sub_question':sub_question,
            'question_grade':question_grade_marks,
            'sub_question_grade':sub_question_grade_marks,
            'question': question,
            'total':total_marks,
            # 'previous_exam_papers':
        }
        return render(request, 'exam/grades/teacher_add_grade.html', context)

    def post(self, request, studentid, answerid,  *args, **kwargs):
        studentid = request.POST.get('student_id')
        print(studentid)
        student_instance = get_object_or_404(Student, pk=studentid)
        examid = request.POST.get('exam_id')
        exam_instance = get_object_or_404(Exams, pk=examid)

        question_paper = get_object_or_404(QuestionPaper, exam=exam_instance)
        question = Question.objects.filter(question_paper=question_paper)

        marks_list = []
        
        for item in question:
            id = str(item.pk)
            mark_instance = float(request.POST[id])
            marks_list.append(mark_instance)
            QuestionGrade.objects.create(student=student_instance, question=get_object_or_404(
                Question, pk=item.pk), marks=mark_instance)

        print(marks_list)

        applicationform_instance = application_form.objects.get(
            term=exam_instance.term, student=student_instance)
        student_grade = studentgrades.objects.get(
            exam_id=exam_instance, application_id=applicationform_instance)
        student_grade.marks = sum(marks_list)
        student_grade.save()

        messages.success(request, 'Question Mark is Uploaded SUccessfully.')
        return redirect('exam:teacher-view-answer', examid)


def check_exam_paper(request):
    if request.method == 'POST':# and 'fetch_answer_paper' in request.POST:
        print("Inside POST-------------------------------")
        
        exam = Exams.objects.get(pk = request.POST['exam'])
        answersheets = AnswerSheet.objects.filter(exam = exam)
        context = {
          'terms': Term.objects.all(),
          'answersheets':answersheets,
        'title':'Check Papers',
        
    }
        return render(request, 'exam/teachers/check_papers.html', context)

    teacher = get_object_or_404(CustomUser, id = request.user.id)
    staff_user = Staff.objects.get(staff_user=teacher)
    category = staff_user.courses.all()
    print(staff_user,'\n',category,'\n')
    terms = Term.objects.filter(course_category__in = category)
    context = {
          'terms': terms,
        'title':'Check Papers',
         'answersheets' : AnswerSheet.objects.all()
        
    }
    return render(request, 'exam/teachers/check_papers.html', context)



@csrf_exempt
def add_student_grade(request):

    studentid = request.POST.get('student_id')
    examid = request.POST.get('exam_id')
    questionmark_value = request.POST.get('questionmark_value')
    question_id = request.POST.get('questionmark_id')
    # grade_id = request.POST.get('grade_id')
    
    student_instance = get_object_or_404(Student, pk=studentid)
    question_instance = get_object_or_404(Question, pk=question_id)
    exam_instance = get_object_or_404(Exams, pk=examid)

     # --For saving individual marks to student respective grade
    question_paper = get_object_or_404(QuestionPaper, exam=exam_instance)
    question = Question.objects.filter(question_paper=question_paper)

    # marks_list = []
    # for item in question:
    #     id = item.pk
    #     mark_instance = float(request.POST[id])
    #     marks_list.append(mark_instance)
    # print(marks_list,"----------mark list------------")

    obj, created = QuestionGrade.objects.get_or_create(student=student_instance, question=question_instance)
    obj.marks = questionmark_value
    obj.save()


    applicationform_instance = application_form.objects.get(term = exam_instance.term, student = student_instance)
    student_grade  = studentgrades.objects.get(exam_id = exam_instance, application_id = applicationform_instance)
    questions = Question.objects.filter(question_paper__exam=exam_instance)
    total_marks = 0
    for item in questions:
        try:
            q_marks = QuestionGrade.objects.get(question=item, student=student_instance)
            marks = q_marks.marks
            total_marks+= marks
        except:
            print(item,"marks not found")
    
    student_grade.marks = float(total_marks)
    student_grade.save()
    

    question_grade_marks = QuestionGrade.objects.filter(student=Student.objects.get(pk=studentid), question__question_paper__exam=exam_instance)
    sub_question_grade_marks = SubQuestionGrade.objects.filter(student=Student.objects.get(pk=studentid), sub_question__question__question_paper__exam=exam_instance)

    context = {'question':question_grade_marks,
                'sub_question':sub_question_grade_marks,
                'total':total_marks}
    
    print(context)

    html = render_to_string('exam/grades/show_grades_table.html', context=context)
    res = {'html': html}
    return JsonResponse(res, safe=False)


    # return render (request, 'exam/grades/show_grades_table.html', context=context)
    
    # student_grade.marks = float(questionmark_value)
    # student_grade.save()

    # else:
    #     question_grade = QuestionGrade.objects.create(student=student_instance,
    #                                                   question=question_instance, marks=questionmark_value)

    # --

    # --
    # grade_instance = question_instance.questiongrade_set.all()
    # # Update instance if grade is already present
    # if grade_instance:
    #     grade_pk = []
    #     for grade in grade_instance:
    #         grade_pk.append(grade.pk)
    #         question_grade = QuestionGrade.objects.filter(
    #             pk__in=grade_pk, question=question_instance).first()
    #         question_grade.marks = questionmark_value
    #         question_grade.save()
    #         # --

        # #Updating student mark to application form also such that student can readily view grade from their dashboard
    

    # def post(self,request,studentid, answerid,  *args, **kwargs):
    #     studentid = request.POST.get('studentid')
    #     student_instance = get_object_or_404(Student, pk = studentid )
    #     examid = request.POST.get('examid')
    #     exam_instance = get_object_or_404(Exams, pk = examid)

    #     question_paper = get_object_or_404(QuestionPaper,exam = exam_instance)
    #     question = Question.objects.filter(question_paper = question_paper)

    #     marks_list = []
    #     for item in question:
    #         id = str(item.pk)
    #         mark_instance = float(request.POST[id])
    #         marks_list.append(mark_instance)
    #         QuestionGrade.objects.create(student = student_instance, question = get_object_or_404(Question, pk = item.pk), marks = mark_instance)

    #     print(marks_list)

    #     applicationform_instance = application_form.objects.get(term = exam_instance.term, student = student_instance)
    #     student_grade  = studentgrades.objects.get(exam_id = exam_instance, application_id = applicationform_instance)
    #     student_grade.marks = sum(marks_list)
    #     student_grade.save()

    #     messages.success(request,'Question Mark is Uploaded SUccessfully.')
    #     return redirect('exam:teacher-view-answer',examid)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@csrf_exempt
def add_student_grade_sub(request):
    studentid = request.POST.get('student_id')
    examid = request.POST.get('exam_id')
    question_id = request.POST.get('parent_question')
    subquestion_id = request.POST.get('subquestion_id')
    marks = request.POST.get('marks')

    student_instance = get_object_or_404(Student, pk=studentid)
    exam_instance = get_object_or_404(Exams, pk=examid)
    question_instance = get_object_or_404(Question, pk=question_id)
    subquestion_instance = get_object_or_404(SubQuestion, pk=subquestion_id)

    obj, created = SubQuestionGrade.objects.get_or_create(student=student_instance, sub_question=subquestion_instance)
    obj.marks = marks
    obj.save()
    print(obj, "~~~~~~~~~~~~~~~~~~~~~~~~~~~", "OBJ FIRST")

    subquestions = SubQuestion.objects.filter(question=question_instance)
    obj2, created2 = QuestionGrade.objects.get_or_create(student=student_instance, question=question_instance)
    print(obj2,"~~~~~~~~~~~~~~~~~~~~~~~~~~~", "OBJ SECOND")
    print(subquestions, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", "subquestions")
    question_marks = 0

    for item in subquestions:
        try:
            print("Subquestion: ", SubQuestionGrade.objects.get(sub_question=item, student=student_instance), "~~~~~~~~~~~~~~~~~~~~~~")
            q_marks = SubQuestionGrade.objects.get(sub_question=item, student=student_instance)
            marks = q_marks.marks
            question_marks+= marks
        except:
            print(item,"marks not found instide try")
    
    obj2.marks = question_marks
    obj2.save()
    print(obj2, "oj2 saved", "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    
    applicationform_instance = application_form.objects.get(term = exam_instance.term, student = student_instance)
    student_grade  = studentgrades.objects.get(exam_id = exam_instance, application_id = applicationform_instance)
    questions = Question.objects.filter(question_paper__exam=exam_instance)
    total_marks = 0
    for item in questions:
        try:
            q_marks = QuestionGrade.objects.get(question=item, student=student_instance)
            marks = q_marks.marks
            total_marks+= marks
        except:
            print(item,"marks not found inside second try")
    
    student_grade.marks = total_marks
    student_grade.save()

    question_grade_marks = QuestionGrade.objects.filter(student=Student.objects.get(pk=studentid), question__question_paper__exam=exam_instance)
    sub_question_grade_marks = SubQuestionGrade.objects.filter(student=Student.objects.get(pk=studentid), sub_question__question__question_paper__exam=exam_instance)

    context = {'question':question_grade_marks,
                'sub_question':sub_question_grade_marks,
                'total':total_marks}
    
    print(context)

    html = render_to_string('exam/grades/show_grades_table.html', context=context)
    res = {'html': html}
    return JsonResponse(res, safe=False)



def all_answer_upload(request):
    print("all answer upload")

    form = StudentDetailsSearch(user=request.user)
    if request.method == 'POST':# and  'fetch_student' in request.POST :
        
        print("Inside post:::")
        exam = Exams.objects.get(pk = request.POST['exam'])
        students = studentgrades.objects.filter(exam_id=exam)
        print(students)

        valid_students = []

        for item in students:
            application = item.application_id
            if (application.status):
                valid_students.append(item.application_id.student)
        
        return render(request,  'exam/admin/all_answer_upload.html', {'students':valid_students, 
                                                                      'terms': Term.objects.all(),
                                                                        'exam':exam})
   


    if request.method == 'POST' and 'upload_answer_button' in request.POST:
        examid = request.POST.get('exam')
        print("examid: ", examid, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        students = request.POST.getlist('students')
        print("students: ", students, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        student_answer_files = request.FILES.getlist('answer_upload')
        for student_id, answer_file in zip(students, student_answer_files):
            print(student_id, answer_file)
            student_instance = get_object_or_404(
                Student, student_user=student_id)
            obj, created = AnswerSheet.objects.get_or_create(exam_id=examid, student=student_instance)
            obj.answer_upload=answer_file
            obj.save()
        messages.success(request, "Answers are uploaded successfully")


    teacher = get_object_or_404(CustomUser, id = request.user.id)
    try:
        staff_user = Staff.objects.get(staff_user=teacher)
        category = staff_user.courses.all()
        terms = Term.objects.filter(course_category__in = category)
    except:
        # category=request.user.adminuser.course_category
        terms = Term.objects.all()#filter(course_category = category)
    

    context = {
        'form': form,
        'terms': terms
    }
    return render(request, 'exam/admin/all_answer_upload.html', context)



def fill_exam_select_ajax(request):
    term = Term.objects.get(pk=request.GET['term'])
    exams = Exams.objects.filter(term=term)

    context = {'exams':exams}

    html = render_to_string('exam/admin/exam_select.html', context=context)
    res = {'html': html}
    return JsonResponse(res, safe=False)


'''This is view of answersheet with grade for respective students  '''
def view_answer_sheet(request):
    exams = Exams.objects.all()
    terms = Term.objects.all()
    if request.method == 'POST':
        exam = request.POST.get('exam')
        term = request.POST.get('term')
        answer_sheet=AnswerSheet.objects.none()
        try:
            answer_sheet = AnswerSheet.objects.get(exam = exam, student__student_user = request.user.id)
            print(answer_sheet,answer_sheet.student, answer_sheet.answer_upload,"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            context = {
            'exams':exams,
            'terms':terms,
            'title':'Answer Sheet',
            'answer_sheet':answer_sheet
            }
            return render(request, 'exam/students/view_answersheet.html', context)
        except:
            context = {
            'exams':exams,
            'terms':terms,
            'title':'Answer Sheet',
            }
            return render(request, 'exam/students/view_answersheet.html', context)

    context = {
        'title':'Answer Sheet',
        'exams':exams,
        'terms':terms,
    }
    return render(request, 'exam/students/view_answersheet.html', context)