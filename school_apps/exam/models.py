from django.db import models
from django.db.models.fields import related
from school_apps.courses.models import Exams, application_form,studentgrades
from student_management_app.models import (CustomUser, Subject, SessionYear, Staff, Student, Semester,
                                           Section, ExtraUser,Subject)
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings
import os

# Create your models here.


class QuestionPaper(models.Model):
    exam = models.OneToOneField(Exams, on_delete=models.CASCADE,null = True)
    file = models.FileField(upload_to="questionpapers")
    draft = models.BooleanField(_('Save as Draft'),default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Term : {self.exam.term}-{self.exam.semester}-{self.exam.subject_id}'



class Question(models.Model):
    question_paper = models.ForeignKey(QuestionPaper, on_delete=models.CASCADE, null=True)
    question_no = models.CharField(max_length=100)
    total_marks = models.FloatField(null = True, blank=True)
    student = models.ManyToManyField(Student, through='QuestionGrade')
    # file = models.FileField(upload_to="",blank=True, null=True)
    question_description = models.TextField(null = True, blank=True)
    has_sub_question = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # @property
    # def get_sub_total_marks(self,*args, **kwargs):
    #     question_instance = get_object_or_404(Question,pk = self.pk)
    #     sub_question_marks = question_instance.sub_questions.all()
    #     sub_total_marks = []
    #     for mark in sub_question_marks :
    #         sub_total_marks.append(mark.total_marks)
    #     print(sub_question_marks,"==============================")
    #     return sum(sub_question_marks)
            
    def __str__(self) -> str:
        return f'{self.question_no} - Total Marks : {self.total_marks}'




class SubQuestion(models.Model):
    question_paper = models.ForeignKey(QuestionPaper, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, related_name = 'sub_questions')
    question_no = models.CharField(max_length=100,null = True, blank=True)
    total_marks = models.FloatField(null = True, blank=True)
    student = models.ManyToManyField(Student, through='SubQuestionGrade')
    question_description = models.TextField(null = True, blank=True)
    # file = models.FileField(upload_to="",blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.question.question_no}({self.question_no}) - Total Marks : {self.total_marks}'


class QuestionGrade(models.Model):
        
    student = models.ForeignKey(Student, on_delete=models.CASCADE,null = True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE,null=True)
    # subquestion = models.ForeignKey(SubQuestion, on_delete=models.CASCADE,null=True,blank=True)
    marks = models.FloatField(null=True)
    # answer_upload = models.FileField(upload_to = 'Student_answers', null=True)
    feedback = models.TextField(_("Teacher Feedback"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.student.student_user.full_name) + " " + str(self.marks)
    
    # def save(self, *args, **kwargs):
    #     print("in save")
    #     exam_instance = self.question.question_paper.exam
    #     student_instance= self.student
    #     applicationform_instance = application_form.objects.get(term=exam_instance.term, student=student_instance)
    #     student_grade  = studentgrades.objects.get(exam_id = exam_instance, application_id = applicationform_instance)

    #     questions = Question.objects.filter(question_paper__exam=exam_instance)
    #     total_marks = 0
    #     for item in questions:
    #         try:
    #             q_marks = QuestionGrade.objects.get(question=item, student=student_instance)
    #             marks = q_marks.marks
    #             print(marks, "marks")
    #             total_marks+= marks
    #         except:
    #             print(item,"marks not found")
    
    #     student_grade.marks = total_marks
    #     student_grade.save()

class SubQuestionGrade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    sub_question = models.ForeignKey(SubQuestion, on_delete=models.CASCADE)
    marks = models.FloatField(null=True)
    feedback = models.TextField(_("Teacher Feedback"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.student.student_user.full_name) + " " + str(self.sub_question.question_no) +" " +str(self.marks)

    
    
class AnswerSheet(models.Model):
    questionpaper_status = (
     ('Assigned',"Assigned"),('Completed','Completed')
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE,null=True)
    exam = models.ForeignKey(Exams, on_delete=models.CASCADE,null = True)
    answer_upload = models.FileField(upload_to = 'Student_answers/student_answers', null=True,blank=True)
    graded_sheet = models.FileField(upload_to='Student_answers/graded_sheets', null=True,blank=True)
    questionpaper_status = models.CharField(choices = questionpaper_status,  max_length=50, default = 'Assigned',null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super(AnswerSheet, self).__init__(*args, **kwargs)
        self.__answer_upload_name = self.answer_upload.name
        self.__graded_sheet_name = self.graded_sheet.name
        self.__original_graded_sheet = self.graded_sheet

    def save(self, *args, **kwargs):
        print('in save---------------------------------------------------')
        print(self.__answer_upload_name)
        print(self.__graded_sheet_name)

        print(self.graded_sheet == self.__original_graded_sheet)

        super().save(*args, **kwargs)

# @receiver(pre_save, sender=AnswerSheet)  #overwrite existing file
# def file_update(sender, **kwargs):
#     answer_sheet_instance = kwargs['instance']
#     if (answer_sheet_instance.graded_sheet != super.__original_graded_sheet):
#         if answer_sheet_instance.graded_sheet:
#             path = answer_sheet_instance.graded_sheet.path
#             name = answer_sheet_instance.graded_sheet.name
#             url = os.path.join(settings.MEDIA_ROOT, 'Student_answers/graded_sheets/'+name)

#             print('path: ', path ,'\n url:', url,'\n name:', name)
#             os.remove(url)


class ExamAttendance(models.Model):
    semester=models.ForeignKey(Semester,on_delete=models.DO_NOTHING, null=True)
    section=models.ForeignKey(Section,on_delete=models.DO_NOTHING, null=True)
    subject=models.ForeignKey(Subject,on_delete=models.DO_NOTHING, null=True)
    attendance_date=models.DateField(null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    session_year=models.ForeignKey(SessionYear,on_delete=models.CASCADE,null=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    # def __str__(self):
    #     return self.attendance_date

    

class ExamAttendanceReport(models.Model):
    attendance_choices = (
        ('Present','Present'),('Absent(Informed)','Absent(Informed)'),('Absent(Not Informed)','Absent(Not Informed)'),
        ('Late','Late'),
        ('Excused','Excused'),
    )
    
    student=models.ForeignKey(Student,on_delete=models.DO_NOTHING, null=True)
    staff=models.ForeignKey(Staff,on_delete=models.DO_NOTHING, null=True)
    extra_user=models.ForeignKey(ExtraUser,on_delete=models.DO_NOTHING, null=True)
    attendance=models.ForeignKey(ExamAttendance,on_delete=models.CASCADE)
    status = models.CharField(max_length = 50,choices = attendance_choices , blank=True)
    remarks = models.CharField(max_length=250, null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.student}'


