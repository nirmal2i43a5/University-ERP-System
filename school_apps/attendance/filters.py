import django_filters
from django_filters import DateFilter
from django import forms
from attendance.models import Attendance


class StudentAttendanceFilter(django_filters.FilterSet):
    attendance_date = DateFilter(
        widget=forms.DateInput(
            attrs={
                "type": "date"}))

    class Meta:
        model = Attendance
        fields = ["attendance_date"]
