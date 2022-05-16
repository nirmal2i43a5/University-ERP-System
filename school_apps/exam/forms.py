from django import forms
from school_apps.courses.models import Exams
from school_apps.exam.models import Question, QuestionPaper, QuestionGrade, SubQuestion
from django.forms import inlineformset_factory
from student_management_app.models import Semester, Section, Subject, SubjectTeacher



class QuestionPaperUploadForm(forms.ModelForm):
    class Meta:
        model = QuestionPaper
        fields = '__all__'
    
    exam = forms.ModelChoiceField(required = False, label= '',empty_label = 'Choose Subject',
                                     queryset = Exams.objects.all())

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        print(user)
        if user:
            exam = self.fields['exam']
            subjects = SubjectTeacher.objects.filter(teacher = user).values_list('subject', flat=True)
            exam_list = Exams.objects.filter(subject_id__in = subjects)
            exam.queryset = exam_list
        if user.is_superuser:# or user|has_group:'Admin':
            exam = self.fields['exam']
            exam.queryset = Exams.objects.all()


class QuestionMark(forms.ModelForm):
    question_description = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'rows': 1, 'cols': 20,"placeholder": "Enter Question Description"}))
    total_marks = forms.FloatField(required=False,  widget=forms.NumberInput(
        attrs={"placeholder": " Enter  Total Marks(Fill this Only if you do not have sub question)", }))
    question_no = forms.CharField( widget=forms.TextInput(
        attrs={"placeholder": " Enter  Question No", }))
 
    class Meta:
        model = Question
        fields = '__all__'
        exclude = ('student','question_paper')
    
class SubQuestionMark(forms.ModelForm):
    question_description = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'rows': 2, 'cols': 10 }))
    class Meta:
        model = SubQuestion
        fields = '__all__'
        exclude = ('student','question_paper','question',)
        widgets = {
			'question_no': forms.TextInput(attrs={'class': 'formset-field'}),
			'total_marks': forms.TextInput(attrs={'class': 'formset-field sub_question_mark'}),
			'question_description': forms.TextInput(attrs={'class': 'formset-field','rows': 3, 'cols': 20 })
		}
    
# SubQuestionMarkFormset=inlineformset_factory(Question,SubQuestion, form=SubQuestionMark, extra=1)


class QuestionGradeForm(forms.ModelForm):
    # feedback = forms.CharField(required=False, widget=forms.Textarea(
    #     attrs={'rows': 2, 'cols': 10 }))
    class Meta:
        model = QuestionGrade
        fields = '__all__'
        exclude = ('student','feedback',)
        


#for managing details
class StudentDetailsSearch(forms.Form):

    semester = forms.ModelChoiceField(label= '',empty_label = 'Choose Semester',
                                      queryset = Semester.objects.all(),widget=forms.Select(attrs = {'class':'col-md-12'}))
    section = forms.ModelChoiceField(label= '',empty_label = 'Choose Section', widget=forms.Select(attrs={'class':'col-md-12'}),
                                     queryset = Section.objects.all())
    subject = forms.ModelChoiceField(required = False, label= '',empty_label = 'Select Subject',widget=forms.Select(attrs={'class':'col-md-12'}),
                                     queryset = Subject.objects.all())
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            subject = self.fields['subject']
            subject.queryset = subject.queryset.filter(staff_user=user)
        if user.is_superuser:# or user|has_group:'Admin':
            subject = self.fields['subject']
            subject.queryset = Subject.objects.all()
    


