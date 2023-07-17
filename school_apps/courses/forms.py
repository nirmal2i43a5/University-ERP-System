from django.db import models
from .models import Subject, Exams, Term, CourseCategory
from student_management_app.models import Course, Department
from student_management_app.models import Subject, Semester
from django.forms import ModelForm, fields
from django import forms

# class SubjectForm(ModelForm):
#     class Meta:
#         model = Subject
#         fields = '__all__'


class CourseForm(ModelForm):
    course_category = forms.ModelChoiceField(
        queryset=CourseCategory.objects.all(), widget=forms.RadioSelect()
    )

    class Meta:
        model = Course
        fields = "__all__"


class CourseCategoryeForm(ModelForm):
    class Meta:
        model = CourseCategory
        fields = "__all__"


class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = "__all__"


class ExamsForm(ModelForm):
    exam_choices = [("Unit", "Unit Test"), ("Term", "Terminal Examination")]

    format_choices = (
        ("Open Book", "Open Book"),
        ("Close Book", "Closed Book"),
    )

    semester = forms.ModelChoiceField(
        label="Class", queryset=Semester.objects.all())
    date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "type": "date",
            }
        ),
    )
    time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(
            attrs={
                "type": "time",
            }
        ),
    )
    # exam_type=forms.ChoiceField(
    #     widget=forms.RadioSelect(), choices=exam_choices)
    exam_format = forms.ChoiceField(
        widget=forms.RadioSelect(),
        choices=format_choices)

    def __init__(self, *args, **kwargs):
        super(ExamsForm, self).__init__(*args, **kwargs)
        self.fields["exam_title"].widget.attrs["readonly"] = True
        self.fields["exam_id"].widget.attrs["readonly"] = True

    class Meta:
        model = Exams
        fields = "__all__"
        exclude = ["exam_type"]


class TermForm(ModelForm):
    course_category = forms.ModelChoiceField(
        required=True, queryset=CourseCategory.objects.all()
    )

    exam_choices = [("Unit", "Unit Test"), ("Term", "Terminal Examination")]
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "type": "date",
            }
        ),
    )

    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "type": "date",
            }
        ),
    )
    type = forms.ChoiceField(widget=forms.RadioSelect(), choices=exam_choices)

    class Meta:
        model = Term
        fields = "__all__"
        exclude = ["is_published"]
