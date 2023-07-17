from django.contrib import admin
from school_apps.exam.models import Question, QuestionPaper, QuestionGrade, AnswerSheet

# Register your models here.
admin.site.register(Question)
admin.site.register(QuestionPaper)
admin.site.register(QuestionGrade)
admin.site.register(AnswerSheet)
