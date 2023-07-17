from django.db import models
from student_management_app.models import (
    Subject,
    SessionYear,
    Staff,
    Student,
    Semester,
    Section,
    ExtraUser,
)


class Attendance(models.Model):
    faculty_choices = (
        ("", "-------Select Group-------"),
        ("Science", "Science"),
        ("Non-Science", "Non-Science"),
    )

    faculty = models.CharField(max_length=100, choices=faculty_choices)
    semester = models.ForeignKey(
        Semester, on_delete=models.DO_NOTHING, null=True)
    section = models.ForeignKey(
        Section, on_delete=models.DO_NOTHING, null=True)
    subject = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, null=True)
    attendance_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    session_year = models.ForeignKey(
        SessionYear, on_delete=models.CASCADE, null=True)
    # student=models.ForeignKey(Student,on_delete=models.DO_NOTHING)
    # staff=models.ForeignKey(Staff,on_delete=models.DO_NOTHING)
    # status = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.semester:
            return (
                f"{self.attendance_date}:{self.semester}:{self.section}:{self.subject}"
            )
        else:
            return f"{self.attendance_date}"

    # class Meta:
    #     default_permissions = ()


class AttendanceReport(models.Model):
    attendance_choices = (
        ("Present", "Present"),
        ("Absent(Informed)", "Absent(Informed)"),
        ("Absent(Not Informed)", "Absent(Not Informed)"),
        ("Late", "Late"),
        ("Excused", "Excused"),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    extra_user = models.ForeignKey(
        ExtraUser, on_delete=models.CASCADE, null=True)
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    # status=models.BooleanField(default=False)
    # normal_status = models.CharField(max_length=50,null=True,blank=True)
    status = models.CharField(
        max_length=50,
        choices=attendance_choices,
        blank=True)
    remarks = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.staff}::{self.attendance.attendance_date}"
