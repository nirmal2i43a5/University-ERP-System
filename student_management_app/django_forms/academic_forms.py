from django import forms
from django.shortcuts import get_object_or_404
from student_management_app.models import CourseCategory, Semester, Section


class ClassFormSearch(forms.Form):
    semester = forms.ModelChoiceField(
        required=False,
        label="",
        empty_label="---Click Here To  Filter Class---",
        queryset=Semester.objects.all(),
    )
    section = forms.ModelChoiceField(
        required=False,
        label="",
        empty_label="---Click Here To  Filter section---",
        queryset=Section.objects.all(),
    )


class StudentFormSearch(forms.Form):
    faculty_choices = (
        ("", "-------Select Group-------"),
        ("Science", "Science"),
        ("Non-Science", "Non-Science"),
    )

    # semester = forms.ModelChoiceField(required = False, label= '',empty_label = '---Click Here To  Filter Class---', queryset = Semester.objects.all())
    section = forms.ModelChoiceField(
        required=False,
        label="",
        empty_label="---Click Here To  Filter section---",
        queryset=Section.objects.all(),
    )
    group = forms.ChoiceField(
        required=False,
        label="",
        choices=faculty_choices)

    # def init(self, args, user=None, **kwargs):
    #     super().init(args, **kwargs)
    #     a_level_course_category = get_object_or_404(CourseCategory,course_name = 'A-Level')
    #     bachelor_course_category = get_object_or_404(CourseCategory,course_name = 'Bachelor')
    #     master_course_category = get_object_or_404(CourseCategory,course_name = 'Master')

    #     if user.adminuser.course_category == a_level_course_category:
    #         semester = self.fields['semester']
    #         semester.queryset = semester.queryset.filter(course_category = a_level_course_category)
    #     if user.adminuser.course_category == bachelor_course_category:
    #         semester = self.fields['semester']
    #         semester.queryset = semester.queryset.filter(course_category = bachelor_course_category)
    #     if user.adminuser.course_category == master_course_category:
    #         semester = self.fields['semester']
    #         semester.queryset = semester.queryset.filter(course_category = master_course_category)
