from django.urls import path
from . import views
from student_management_system.views import exam_home

app_name = 'exam'

urlpatterns = [
   path('question/add/',views.QuestionPaperUpload.as_view(),name = 'question-add'),
   path('question/edit/<str:pk>/',views.qustion_paper_update,name = 'question-edit'),
   path('question/index/',views.QuestionListView.as_view(),name = 'question-index'),
   # path('question/mark/add/<str:questionpaper_id>/',views.EachQuestionMarkAdd.as_view(),name = 'each-mark-add'),
   path('question/mark/add/<str:questionpaper_id>/',views.each_question_mark_create,name = 'each-mark-add'),
   path('question/mark/<str:pk>/',views.EachQuestionMarkView.as_view(),name = 'each-mark-index'),
   path('subquestion/mark/<str:mainquestion_id>/',views.sub_question_marks_show,name = 'sub-question-mark-index'),
   path('question/mark/<str:questionpaperid>/<str:pk>/',views.qustionpaper_mark_update,name = 'each-mark-edit'),
   path('student/questionpaper/',views.StudentQuestionPaperView.as_view(),name = 'student-questionpaper-view'),
   path('student/answerupload/<exampk>/',views.StudentUploadAnswer.as_view(),name = 'student-upload-answer'),
   path('student-answer/<str:examid>/',views.TeacherViewAnswer.as_view(),name = 'teacher-view-answer'),
   path('grade/add/<str:studentid>/<str:answerid>/',views.TeacherAddGrade.as_view(),name = 'student-grade-add'),
   path('grade/add/',views.add_student_grade ,name = 'student-ajax-grade-add-question'),
   path('grade/sub/',views.add_student_grade_sub ,name = 'subquestion_grade'),
   path('ajax/examselect',views.fill_exam_select_ajax ,name = 'fill_exam_select_ajax'),
   path('view_answer_sheet/',views.view_answer_sheet ,name = 'view_answer_sheet'),
   path('check_paper/',views.check_exam_paper ,name = 'check_exam_paper'),

   
   
   #  path('answer/save/',views.save_student_answer ,name = 'save_student_answer'),
]

