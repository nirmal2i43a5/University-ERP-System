# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or
# field names.
from ast import arg
from msilib import Table
from django.db import models


class AcademicGrade(models.Model):
    id = models.BigAutoField(primary_key=True)
    assignment_status = models.CharField(max_length=50, blank=True, null=True)
    grade = models.IntegerField(blank=True, null=True)
    grade_status = models.BooleanField()
    feedback = models.CharField(max_length=255, blank=True, null=True)
    answer_upload = models.CharField(max_length=500, blank=True, null=True)
    date_submitted = models.DateTimeField()
    updated_at = models.DateTimeField()
    assignment = models.ForeignKey("TblAssignment", models.DO_NOTHING)
    student = models.ForeignKey("TblCustomuser", models.DO_NOTHING)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "academic_grade"


class AttendanceAttendance(models.Model):
    id = models.BigAutoField(primary_key=True)
    faculty = models.CharField(max_length=100)
    attendance_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    section = models.ForeignKey(
        "TblSection",
        models.DO_NOTHING,
        blank=True,
        null=True)
    semester = models.ForeignKey(
        "TblSemester", models.DO_NOTHING, blank=True, null=True
    )
    session_year = models.ForeignKey(
        "TblSessionyear", models.DO_NOTHING, blank=True, null=True
    )
    subject = models.ForeignKey(
        "TblSubject",
        models.DO_NOTHING,
        blank=True,
        null=True)

    class Meta:
        managed = False
        db_table = "attendance_attendance"


class AttendanceAttendancereport(models.Model):
    id = models.BigAutoField(primary_key=True)
    status = models.CharField(max_length=50)
    remarks = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    attendance = models.ForeignKey(AttendanceAttendance, models.DO_NOTHING)
    extra_user = models.ForeignKey(
        "TblExtrauser", models.DO_NOTHING, blank=True, null=True
    )
    staff = models.ForeignKey(
        "TblStaff",
        models.DO_NOTHING,
        blank=True,
        null=True)
    student = models.ForeignKey(
        "TblStudent",
        models.DO_NOTHING,
        blank=True,
        null=True)

    class Meta:
        managed = False
        db_table = "attendance_attendancereport"


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = "auth_group"


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey("AuthPermission", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_group_permissions"
        unique_together = (("group", "permission"),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey("DjangoContentType", models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "auth_permission"
        unique_together = (("content_type", "codename"),)


class CoursesApplicationForm(models.Model):
    application_id = models.CharField(primary_key=True, max_length=255)
    status = models.BooleanField()
    application_date = models.DateField()
    remarks = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    semester = models.ForeignKey("TblSemester", models.DO_NOTHING)
    student = models.ForeignKey("TblStudent", models.DO_NOTHING)
    term = models.ForeignKey("CoursesTerm", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "courses_application_form"


class CoursesExams(models.Model):
    exam_id = models.CharField(primary_key=True, max_length=100)
    exam_title = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=5)
    exam_format = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField()
    full_marks = models.IntegerField()
    pass_marks = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    semester = models.ForeignKey(
        "TblSemester", models.DO_NOTHING, blank=True, null=True
    )
    subject_id = models.ForeignKey("TblSubject", models.DO_NOTHING)
    term = models.ForeignKey("CoursesTerm", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "courses_exams"


class CoursesSelectedcourses(models.Model):
    id = models.BigAutoField(primary_key=True)
    year = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    semester = models.ForeignKey("TblSemester", models.DO_NOTHING)
    student_id = models.ForeignKey("TblStudent", models.DO_NOTHING)
    subject_id = models.ForeignKey("TblSubject", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "courses_selectedcourses"


class CoursesStudentgrades(models.Model):
    id = models.BigAutoField(primary_key=True)
    marks = models.FloatField()
    grade = models.CharField(max_length=6)
    passed = models.BooleanField()
    exam_type = models.BooleanField()
    is_absent = models.BooleanField()
    rank = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    application_id = models.ForeignKey(
        CoursesApplicationForm, models.DO_NOTHING)
    exam_id = models.ForeignKey(CoursesExams, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "courses_studentgrades"


class CoursesTerm(models.Model):
    term_id = models.CharField(primary_key=True, max_length=30)
    year = models.IntegerField()
    term_name = models.CharField(max_length=25)
    type = models.CharField(max_length=5)
    start_date = models.DateField()
    end_date = models.DateField()
    exam_centre = models.CharField(max_length=30)
    is_published = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    course_category = models.ForeignKey(
        "StudentManagementAppCoursecategory",
        models.DO_NOTHING,
        blank=True,
        null=True)

    class Meta:
        managed = False
        db_table = "courses_term"


class CoursesTermRanking(models.Model):
    id = models.BigAutoField(primary_key=True)
    total_marks = models.IntegerField()
    rank = models.IntegerField()
    student = models.ForeignKey("TblStudent", models.DO_NOTHING)
    term = models.ForeignKey(CoursesTerm, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "courses_term_ranking"


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey(
        "DjangoContentType", models.DO_NOTHING, blank=True, null=True
    )
    user = models.ForeignKey("TblCustomuser", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "django_admin_log"


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "django_content_type"
        unique_together = (("app_label", "model"),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "django_migrations"


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "django_session"


class ExamAnswersheet(models.Model):
    id = models.BigAutoField(primary_key=True)
    answer_upload = models.CharField(max_length=100, blank=True, null=True)
    graded_sheet = models.CharField(max_length=100, blank=True, null=True)
    questionpaper_status = models.CharField(
        max_length=50, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    exam = models.ForeignKey(
        CoursesExams,
        models.DO_NOTHING,
        blank=True,
        null=True)
    student = models.ForeignKey(
        "TblStudent",
        models.DO_NOTHING,
        blank=True,
        null=True)

    class Meta:
        managed = False
        db_table = "exam_answersheet"


class ExamExamattendance(models.Model):
    id = models.BigAutoField(primary_key=True)
    attendance_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    section = models.ForeignKey(
        "TblSection",
        models.DO_NOTHING,
        blank=True,
        null=True)
    semester = models.ForeignKey(
        "TblSemester", models.DO_NOTHING, blank=True, null=True
    )
    session_year = models.ForeignKey(
        "TblSessionyear", models.DO_NOTHING, blank=True, null=True
    )
    subject = models.ForeignKey(
        "TblSubject",
        models.DO_NOTHING,
        blank=True,
        null=True)

    class Meta:
        managed = False
        db_table = "exam_examattendance"


class ExamExamattendancereport(models.Model):
    id = models.BigAutoField(primary_key=True)
    status = models.CharField(max_length=50)
    remarks = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    attendance = models.ForeignKey(ExamExamattendance, models.DO_NOTHING)
    extra_user = models.ForeignKey(
        "TblExtrauser", models.DO_NOTHING, blank=True, null=True
    )
    staff = models.ForeignKey(
        "TblStaff",
        models.DO_NOTHING,
        blank=True,
        null=True)
    student = models.ForeignKey(
        "TblStudent",
        models.DO_NOTHING,
        blank=True,
        null=True)

    class Meta:
        managed = False
        db_table = "exam_examattendancereport"


class ExamQuestion(models.Model):
    id = models.BigAutoField(primary_key=True)
    question_no = models.CharField(max_length=100)
    total_marks = models.FloatField(blank=True, null=True)
    question_description = models.TextField(blank=True, null=True)
    has_sub_question = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    question_paper = models.ForeignKey(
        "ExamQuestionpaper", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "exam_question"


class ExamQuestiongrade(models.Model):
    id = models.BigAutoField(primary_key=True)
    marks = models.FloatField(blank=True, null=True)
    feedback = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    question = models.ForeignKey(
        ExamQuestion,
        models.DO_NOTHING,
        blank=True,
        null=True)
    student = models.ForeignKey(
        "TblStudent",
        models.DO_NOTHING,
        blank=True,
        null=True)

    class Meta:
        managed = False
        db_table = "exam_questiongrade"


class ExamQuestionpaper(models.Model):
    id = models.BigAutoField(primary_key=True)
    file = models.CharField(max_length=100)
    draft = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    exam = models.OneToOneField(
        CoursesExams,
        models.DO_NOTHING,
        blank=True,
        null=True)

    class Meta:
        managed = False
        db_table = "exam_questionpaper"


class ExamSubquestion(models.Model):
    id = models.BigAutoField(primary_key=True)
    question_no = models.CharField(max_length=100, blank=True, null=True)
    total_marks = models.FloatField(blank=True, null=True)
    question_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    question = models.ForeignKey(
        ExamQuestion,
        models.DO_NOTHING,
        blank=True,
        null=True)
    question_paper = models.ForeignKey(
        ExamQuestionpaper, models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "exam_subquestion"


class ExamSubquestiongrade(models.Model):
    id = models.BigAutoField(primary_key=True)
    marks = models.FloatField(blank=True, null=True)
    feedback = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    student = models.ForeignKey("TblStudent", models.DO_NOTHING)
    sub_question = models.ForeignKey(ExamSubquestion, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "exam_subquestiongrade"


class LibraryBarcode(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    barcode = models.CharField(max_length=100)
    country_id = models.CharField(max_length=2)
    manufacturer_id = models.CharField(max_length=6)
    product_id = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = "library_barcode"


class LibraryBookentry(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    summary = models.TextField()
    isbn = models.IntegerField(primary_key=True)
    language = models.TextField()
    quantity = models.IntegerField()
    price = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField()
    category = models.ForeignKey("LibraryCategory", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "library_bookentry"


class LibraryBookissue(models.Model):
    id = models.BigAutoField(primary_key=True)
    isbn = models.CharField(max_length=200)
    quantity = models.IntegerField()
    issue_date = models.DateTimeField()
    expirydate = models.DateField()
    issue_id = models.ForeignKey("LibraryIssue", models.DO_NOTHING)
    title = models.ForeignKey(LibraryBookentry, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "library_bookissue"


class LibraryBookrenew(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200)
    quantity = models.IntegerField()
    member_name = models.CharField(max_length=200)
    renew_date = models.DateTimeField()
    expirydate = models.DateField()
    isbn = models.ForeignKey(LibraryBookissue, models.DO_NOTHING)
    member_id = models.ForeignKey(
        "LibraryLibrarymemberprofile",
        models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "library_bookrenew"


class LibraryBookreturn(models.Model):
    id = models.BigAutoField(primary_key=True)
    isbn = models.CharField(max_length=200)
    quantity = models.IntegerField()
    return_date = models.DateTimeField()
    issue_id = models.ForeignKey(
        "LibraryIssue", models.DO_NOTHING, blank=True, null=True
    )
    title = models.ForeignKey(LibraryBookentry, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "library_bookreturn"


class LibraryCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "library_category"


class LibraryIssue(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateField()
    member = models.ForeignKey(
        "LibraryLibrarymemberprofile",
        models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "library_issue"


class LibraryLibrarymemberprofile(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_type = models.CharField(max_length=30)
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200)
    status = models.CharField(max_length=30)
    user_photo = models.CharField(max_length=100, blank=True, null=True)
    permanent_address = models.CharField(max_length=300)
    temporary_address = models.CharField(max_length=300)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=200)
    telephone_no = models.CharField(max_length=15, blank=True, null=True)
    mobile_no = models.CharField(unique=True, max_length=15)
    email = models.CharField(unique=True, max_length=254)
    gender = models.CharField(max_length=30)
    occupation = models.CharField(max_length=300)
    birth_of_date = models.DateField()
    subject = models.CharField(max_length=300, blank=True, null=True)
    academic_year = models.CharField(max_length=20, blank=True, null=True)
    faculty = models.CharField(max_length=100, blank=True, null=True)
    roll_no = models.CharField(max_length=100, blank=True, null=True)
    library_card_no = models.CharField(max_length=100, blank=True, null=True)
    membership_started_at = models.DateTimeField(blank=True, null=True)
    membership_ended_at = models.DateTimeField(blank=True, null=True)
    opac_id = models.CharField(
        db_column="OPAC_id", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    opac_password = models.CharField(
        db_column="OPAC_password", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    qr_code = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField()
    approved_by = models.CharField(max_length=250, blank=True, null=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    rejected_by = models.CharField(max_length=250, blank=True, null=True)
    rejected_at = models.DateTimeField(blank=True, null=True)
    remarks = models.CharField(max_length=500, blank=True, null=True)
    rejected_remarks = models.CharField(max_length=500, blank=True, null=True)
    borrowed_books = models.IntegerField()
    member = models.OneToOneField(
        "TblCustomuser", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "library_librarymemberprofile"


class LibraryReturn(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateField()
    member = models.ForeignKey(LibraryLibrarymemberprofile, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "library_return"


class LogHistoryUserlog(models.Model):
    id = models.BigAutoField(primary_key=True)
    object_id = models.IntegerField(blank=True, null=True)
    app_name = models.CharField(max_length=30)
    model_name = models.CharField(max_length=30)
    action = models.SmallIntegerField()
    object_instance = models.TextField()
    ip = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField()
    user = models.ForeignKey("TblCustomuser", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "log_history_userlog"


class NotificationsNotification(models.Model):
    id = models.BigAutoField(primary_key=True)
    post = models.CharField(max_length=200, blank=True, null=True)
    notification_type = models.IntegerField()
    is_seen = models.BooleanField()
    type = models.CharField(max_length=20)
    created_at = models.DateTimeField()
    created_by = models.ForeignKey(
        "TblCustomuser", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "notifications_notification"


class ScheduleCalendar(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    slug = models.CharField(unique=True, max_length=200)

    class Meta:
        managed = False
        db_table = "schedule_calendar"


class ScheduleCalendarrelation(models.Model):
    id = models.BigAutoField(primary_key=True)
    object_id = models.IntegerField()
    distinction = models.CharField(max_length=20)
    inheritable = models.BooleanField()
    calendar = models.ForeignKey(ScheduleCalendar, models.DO_NOTHING)
    content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "schedule_calendarrelation"


class ScheduleEvent(models.Model):
    id = models.BigAutoField(primary_key=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField()
    end_recurring_period = models.DateTimeField(blank=True, null=True)
    color_event = models.CharField(max_length=10)
    calendar = models.ForeignKey(ScheduleCalendar, models.DO_NOTHING)
    creator = models.ForeignKey(
        "TblCustomuser", models.DO_NOTHING, blank=True, null=True
    )
    rule = models.ForeignKey(
        "ScheduleRule",
        models.DO_NOTHING,
        blank=True,
        null=True)

    class Meta:
        managed = False
        db_table = "schedule_event"


class ScheduleEventrelation(models.Model):
    id = models.BigAutoField(primary_key=True)
    object_id = models.IntegerField()
    distinction = models.CharField(max_length=20)
    content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING)
    event = models.ForeignKey(ScheduleEvent, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "schedule_eventrelation"


class ScheduleOccurrence(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    cancelled = models.BooleanField()
    original_start = models.DateTimeField()
    original_end = models.DateTimeField()
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField()
    event = models.ForeignKey(ScheduleEvent, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "schedule_occurrence"


class ScheduleRule(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=32)
    description = models.TextField()
    frequency = models.CharField(max_length=10)
    params = models.TextField()

    class Meta:
        managed = False
        db_table = "schedule_rule"


class SilkProfile(models.Model):
    name = models.CharField(max_length=300)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    time_taken = models.FloatField(blank=True, null=True)
    file_path = models.CharField(max_length=300)
    line_num = models.IntegerField(blank=True, null=True)
    end_line_num = models.IntegerField(blank=True, null=True)
    func_name = models.CharField(max_length=300)
    exception_raised = models.BooleanField()
    dynamic = models.BooleanField()
    request = models.ForeignKey(
        "SilkRequest",
        models.DO_NOTHING,
        blank=True,
        null=True)

    class Meta:
        managed = False
        db_table = "silk_profile"


class SilkProfileQueries(models.Model):
    id = models.BigAutoField(primary_key=True)
    profile = models.ForeignKey(SilkProfile, models.DO_NOTHING)
    sqlquery = models.ForeignKey("SilkSqlquery", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "silk_profile_queries"
        unique_together = (("profile", "sqlquery"),)


class SilkRequest(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    path = models.CharField(max_length=190)
    query_params = models.TextField()
    raw_body = models.TextField()
    body = models.TextField()
    method = models.CharField(max_length=10)
    start_time = models.DateTimeField()
    view_name = models.CharField(max_length=190, blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    time_taken = models.FloatField(blank=True, null=True)
    encoded_headers = models.TextField()
    meta_time = models.FloatField(blank=True, null=True)
    meta_num_queries = models.IntegerField(blank=True, null=True)
    meta_time_spent_queries = models.FloatField(blank=True, null=True)
    pyprofile = models.TextField()
    num_sql_queries = models.IntegerField()
    prof_file = models.CharField(max_length=300)

    class Meta:
        managed = False
        db_table = "silk_request"


class SilkResponse(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    status_code = models.IntegerField()
    raw_body = models.TextField()
    body = models.TextField()
    encoded_headers = models.TextField()
    request = models.OneToOneField(SilkRequest, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "silk_response"


class SilkSqlquery(models.Model):
    query = models.TextField()
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    time_taken = models.FloatField(blank=True, null=True)
    traceback = models.TextField()
    request = models.ForeignKey(
        SilkRequest,
        models.DO_NOTHING,
        blank=True,
        null=True)
    identifier = models.IntegerField()
    analysis = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "silk_sqlquery"


class StudentManagementAppBranch(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = "student_management_app_branch"


class StudentManagementAppCoursecategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "student_management_app_coursecategory"


class StudentManagementAppDepartment(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = "student_management_app_department"


class StudentManagementAppSemesterteacher(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    semester = models.ForeignKey(
        "TblSemester", models.DO_NOTHING, blank=True, null=True
    )
    teacher = models.ForeignKey("TblCustomuser", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "student_management_app_semesterteacher"


class StudentManagementAppSubjectteacher(models.Model):
    id = models.BigAutoField(primary_key=True)
    section = models.ForeignKey(
        "TblSection",
        models.DO_NOTHING,
        blank=True,
        null=True)
    subject = models.ForeignKey("TblSubject", models.DO_NOTHING)
    teacher = models.ForeignKey("TblCustomuser", models.DO_NOTHING)
    semester = models.ForeignKey(
        "TblSemester", models.DO_NOTHING, blank=True, null=True
    )
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "student_management_app_subjectteacher"
        unique_together = (("subject", "section"),)


class TblAdminuser(models.Model):
    class Meta:
        managed = False
        db_table = "tbl_Adminuser"


class TblAssignment(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateTimeField()
    file = models.CharField(max_length=500, blank=True, null=True)
    draft = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    subject = models.ForeignKey(
        "TblSubject",
        models.DO_NOTHING,
        db_column="Subject_id",
        blank=True,
        null=True)  # Field name made lowercase.
    section = models.ForeignKey(
        "TblSection",
        models.DO_NOTHING,
        blank=True,
        null=True)
    semester = models.ForeignKey("TblSemester", models.DO_NOTHING)
    teacher = models.ForeignKey(
        "TblCustomuser", models.DO_NOTHING, blank=True, null=True
    )
    course = models.ForeignKey(
        "TblCourse",
        models.DO_NOTHING,
        blank=True,
        null=True)
    course_category = models.ForeignKey(
        StudentManagementAppCoursecategory,
        models.DO_NOTHING,
        blank=True,
        null=True)

    class Meta:
        managed = False
        db_table = "tbl_Assignment"


class TblCertificatetemplate(models.Model):
    id = models.BigAutoField(primary_key=True)
    certificate_number = models.CharField(max_length=50)
    date_of_issue = models.DateField()
    salutations = models.CharField(max_length=50, blank=True, null=True)
    passed_year = models.IntegerField()
    photo = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateField()
    updated_at = models.DateField()
    certificate_name = models.CharField(max_length=250)
    theme = models.CharField(max_length=50)
    main_middle_text = models.TextField()
    top_heading_title = models.TextField()
    top_heading_left = models.TextField()
    top_heading_middle = models.TextField()
    top_heading_right = models.TextField()
    footer_left_text = models.TextField()
    footer_middle_text = models.TextField()
    footer_right_text = models.TextField()
    background_image = models.CharField(max_length=100)
    student = models.ForeignKey(
        "TblStudent",
        models.DO_NOTHING,
        blank=True,
        null=True)

    class Meta:
        managed = False
        db_table = "tbl_Certificatetemplate"


class TblComplain(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    description = models.TextField()
    attachment = models.CharField(max_length=500)
    created_at = models.DateField()
    updated_at = models.DateField()
    user = models.OneToOneField("TblCustomuser", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "tbl_Complain"


class TblCourse(models.Model):
    id = models.BigAutoField(primary_key=True)
    course_name = models.CharField(max_length=255, blank=True, null=True)
    course_code = models.CharField(max_length=50)
    course_description = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    course_category = models.ForeignKey(
        StudentManagementAppCoursecategory,
        models.DO_NOTHING,
        blank=True,
        null=True)
    department = models.ForeignKey(
        StudentManagementAppDepartment,
        models.DO_NOTHING,
        blank=True,
        null=True)

    class Meta:
        managed = False
        db_table = "tbl_Course"


class TblCustomuser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=254, blank=True, null=True)
    user_type = models.ForeignKey(
        AuthGroup,
        models.DO_NOTHING,
        blank=True,
        null=True)

    class Meta:
        managed = False
        db_table = "tbl_Customuser"


class TblCustomuserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    customuser = models.ForeignKey(TblCustomuser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "tbl_Customuser_groups"
        unique_together = (("customuser", "group"),)


class TblCustomuserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    customuser = models.ForeignKey(TblCustomuser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "tbl_Customuser_user_permissions"
        unique_together = (("customuser", "permission"),)


class TblDocumentfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    file = models.CharField(max_length=500)
    created_at = models.DateField()
    updated_at = models.DateField()
    extra_user = models.ForeignKey(
        "TblExtrauser", models.DO_NOTHING, blank=True, null=True
    )
    parent = models.ForeignKey(
        "TblParent",
        models.DO_NOTHING,
        blank=True,
        null=True)
    staff = models.ForeignKey(
        "TblStaff",
        models.DO_NOTHING,
        blank=True,
        null=True)
    student = models.ForeignKey(
        "TblStudent",
        models.DO_NOTHING,
        blank=True,
        null=True)

    class Meta:
        managed = False
        db_table = "tbl_Documentfile"


class TblEnotes(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    file = models.CharField(max_length=500)
    note_category = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    course = models.ForeignKey(
        TblCourse,
        models.DO_NOTHING,
        blank=True,
        null=True)
    course_category = models.ForeignKey(
        StudentManagementAppCoursecategory,
        models.DO_NOTHING,
        blank=True,
        null=True)
    semester = models.ForeignKey("TblSemester", models.DO_NOTHING)
    subject = models.ForeignKey("TblSubject", models.DO_NOTHING)
    section = models.ForeignKey("TblSection", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "tbl_Enotes"


class TblExtrauser(models.Model):
    id = models.BigAutoField(primary_key=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=20)
    religion = models.CharField(max_length=100)
    contact = models.CharField(unique=True, max_length=30)
    address = models.CharField(max_length=255)
    join_date = models.DateField(blank=True, null=True)
    image = models.CharField(max_length=100, blank=True, null=True)
    status = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    branch = models.ForeignKey(
        StudentManagementAppBranch, models.DO_NOTHING, blank=True, null=True
    )
    extra_user = models.OneToOneField(
        TblCustomuser, models.DO_NOTHING, blank=True, null=True
    )
    role = models.ForeignKey(
        AuthGroup,
        models.DO_NOTHING,
        blank=True,
        null=True)

    class Meta:
        managed = False
        db_table = "tbl_Extrauser"


class TblHoliday(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    from_date = models.DateField()
    to_date = models.DateField()
    image = models.CharField(max_length=100, blank=True, null=True)
    details = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "tbl_Holiday"


class TblOptionalsubject(models.Model):
    id = models.BigAutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    subject_id = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    course = models.ForeignKey(TblCourse, models.DO_NOTHING)
    semester = models.ForeignKey("TblSemester", models.DO_NOTHING)
    staff_user = models.ForeignKey(TblCustomuser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "tbl_Optionalsubject"


class TblParent(models.Model):
    id = models.BigAutoField(primary_key=True)
    home_phone = models.CharField(max_length=30, blank=True, null=True)
    father_name = models.CharField(max_length=100, blank=True, null=True)
    father_phone = models.CharField(max_length=30, blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True, null=True)
    mother_phone = models.CharField(max_length=30, blank=True, null=True)
    local_guardian_name = models.CharField(
        max_length=100, blank=True, null=True)
    local_guardian_phone = models.CharField(
        max_length=30, blank=True, null=True)
    father_email = models.CharField(max_length=254, blank=True, null=True)
    father_profession = models.CharField(max_length=255, blank=True, null=True)
    father_office = models.CharField(max_length=100, blank=True, null=True)
    mother_profession = models.CharField(max_length=255, blank=True, null=True)
    mother_email = models.CharField(max_length=254, blank=True, null=True)
    mother_office = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    image = models.CharField(max_length=100, blank=True, null=True)
    status = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    parent_user = models.OneToOneField(
        TblCustomuser, models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "tbl_Parent"


class TblRoutine(models.Model):
    id = models.BigAutoField(primary_key=True)
    routine_file = models.CharField(max_length=500)
    college_year = models.CharField(max_length=50, blank=True, null=True)
    day = models.CharField(max_length=100, blank=True, null=True)
    starting_time = models.TimeField(blank=True, null=True)
    ending_time = models.TimeField(blank=True, null=True)
    room = models.CharField(max_length=100, blank=True, null=True)
    course = models.ForeignKey(
        TblCourse,
        models.DO_NOTHING,
        blank=True,
        null=True)
    course_category = models.ForeignKey(
        StudentManagementAppCoursecategory,
        models.DO_NOTHING,
        blank=True,
        null=True)
    section = models.ForeignKey(
        "TblSection",
        models.DO_NOTHING,
        blank=True,
        null=True)
    semester = models.ForeignKey("TblSemester", models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "tbl_Routine"


class TblSection(models.Model):
    id = models.BigAutoField(primary_key=True)
    section_name = models.CharField(max_length=100)
    capacity = models.IntegerField(blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    course_category = models.ForeignKey(
        StudentManagementAppCoursecategory,
        models.DO_NOTHING,
        blank=True,
        null=True)
    semester = models.ForeignKey(
        "TblSemester", models.DO_NOTHING, blank=True, null=True
    )
    staff = models.ForeignKey(
        TblCustomuser,
        models.DO_NOTHING,
        blank=True,
        null=True)
    course = models.ForeignKey(
        TblCourse,
        models.DO_NOTHING,
        blank=True,
        null=True)

    class Meta:
        managed = False
        db_table = "tbl_Section"


class TblSectionSubject(models.Model):
    id = models.BigAutoField(primary_key=True)
    section = models.ForeignKey(TblSection, models.DO_NOTHING)
    subject = models.ForeignKey("TblSubject", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "tbl_Section_subject"
        unique_together = (("section", "subject"),)


class TblSemester(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    semester_value = models.IntegerField(blank=True, null=True)
    description = models.TextField()
    status = models.BooleanField()
    course_category = models.ForeignKey(
        StudentManagementAppCoursecategory,
        models.DO_NOTHING,
        blank=True,
        null=True)
    course = models.ForeignKey(
        TblCourse,
        models.DO_NOTHING,
        blank=True,
        null=True)

    class Meta:
        managed = False
        db_table = "tbl_Semester"


class TblSessionyear(models.Model):
    id = models.BigAutoField(primary_key=True)
    session_start_year = models.DateField()
    session_end_year = models.DateField()

    class Meta:
        managed = False
        db_table = "tbl_Sessionyear"


class TblSettings(models.Model):
    id = models.BigAutoField(primary_key=True)
    logo = models.CharField(max_length=100, blank=True, null=True)
    site_title = models.CharField(max_length=100, blank=True, null=True)
    phone_no = models.CharField(max_length=20, blank=True, null=True)
    system_email = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    academic_year = models.IntegerField(blank=True, null=True)
    footer = models.CharField(max_length=100, blank=True, null=True)
    version = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "tbl_Settings"


class TblSociallink(models.Model):
    id = models.BigAutoField(primary_key=True)
    role = models.CharField(max_length=100)
    facebook = models.CharField(max_length=200)
    twitter = models.CharField(max_length=200)
    linkedin = models.CharField(max_length=200)
    google_plus = models.CharField(max_length=200)
    created_at = models.DateField()
    updated_at = models.DateField()
    user = models.OneToOneField(TblCustomuser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "tbl_Sociallink"


class TblStaff(models.Model):
    id = models.BigAutoField(primary_key=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=20)
    religion = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    contact = models.CharField(unique=True, max_length=30)
    join_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    image = models.CharField(max_length=100, blank=True, null=True)
    status = models.BooleanField()
    department = models.ForeignKey(
        StudentManagementAppDepartment,
        models.DO_NOTHING,
        blank=True,
        null=True)
    staff_user = models.OneToOneField(TblCustomuser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "tbl_Staff"


class TblStaffCourses(models.Model):
    id = models.BigAutoField(primary_key=True)
    staff = models.ForeignKey(TblStaff, models.DO_NOTHING)
    coursecategory = models.ForeignKey(
        StudentManagementAppCoursecategory, models.DO_NOTHING
    )

    class Meta:
        managed = False
        db_table = "tbl_Staff_courses"
        unique_together = (("staff", "coursecategory"),)


class TblStudent(models.Model):
    id = models.BigAutoField(primary_key=True)
    join_year = models.CharField(max_length=50, blank=True, null=True)
    stu_id = models.CharField(unique=True, max_length=50)
    roll_no = models.CharField(max_length=10, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    shift = models.CharField(max_length=20, blank=True, null=True)
    faculty = models.CharField(max_length=50, blank=True, null=True)
    program = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(max_length=50)
    contact = models.CharField(max_length=30)
    permanent_address = models.CharField(max_length=255)
    temporary_address = models.CharField(max_length=255)
    dob = models.DateField(blank=True, null=True)
    blood_group = models.CharField(max_length=25)
    gpa = models.CharField(max_length=50, blank=True, null=True)
    previous_school_name = models.CharField(
        max_length=100, blank=True, null=True)
    image = models.CharField(max_length=100, blank=True, null=True)
    barcode = models.CharField(max_length=100)
    register_no = models.CharField(
        unique=True,
        max_length=250,
        blank=True,
        null=True)
    religion = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.CharField(max_length=255, blank=True, null=True)
    extra_curricular_activities = models.CharField(max_length=255)
    state = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    course = models.ForeignKey(
        TblCourse,
        models.DO_NOTHING,
        blank=True,
        null=True)
    course_category = models.ForeignKey(
        StudentManagementAppCoursecategory,
        models.DO_NOTHING,
        blank=True,
        null=True)
    group = models.ForeignKey(
        "TblStudentgroup", models.DO_NOTHING, blank=True, null=True
    )
    guardian = models.ForeignKey(
        TblParent,
        models.DO_NOTHING,
        blank=True,
        null=True)
    optional_subject = models.ForeignKey(
        "TblSubject", models.DO_NOTHING, blank=True, null=True
    )
    section = models.ForeignKey(
        TblSection,
        models.DO_NOTHING,
        blank=True,
        null=True)
    semester = models.ForeignKey(
        TblSemester,
        models.DO_NOTHING,
        blank=True,
        null=True)
    student_user = models.OneToOneField(
        TblCustomuser, models.DO_NOTHING, blank=True, null=True
    )
    subject = models.ForeignKey(
        "TblSubject",
        models.DO_NOTHING,
        blank=True,
        null=True)
    transport = models.ForeignKey(
        "TblTransport", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "tbl_Student"


class TblStudentgroup(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = "tbl_Studentgroup"


class TblSubject(models.Model):
    subject_id = models.BigAutoField(primary_key=True)
    faculty = models.CharField(max_length=50)
    subject_name = models.CharField(max_length=255)
    subject_code = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    course = models.ForeignKey(
        TblCourse,
        models.DO_NOTHING,
        blank=True,
        null=True)
    course_category = models.ForeignKey(
        StudentManagementAppCoursecategory,
        models.DO_NOTHING,
        blank=True,
        null=True)
    semester = models.ForeignKey(TblSemester, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "tbl_Subject"


class TblSyllabus(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    file = models.CharField(max_length=500)
    description = models.TextField()
    course_category = models.ForeignKey(
        StudentManagementAppCoursecategory,
        models.DO_NOTHING,
        blank=True,
        null=True)
    semester = models.ForeignKey(TblSemester, models.DO_NOTHING)
    course = models.ForeignKey(
        TblCourse,
        models.DO_NOTHING,
        blank=True,
        null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    subject = models.ForeignKey(TblSubject, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "tbl_Syllabus"


class TblTransport(models.Model):
    id = models.BigAutoField(primary_key=True)
    route_name = models.CharField(max_length=100)
    route_fare = models.DecimalField(max_digits=10, decimal_places=2)
    no_of_vehicle = models.IntegerField()
    driver_name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "tbl_Transport"


class TblUserrole(models.Model):
    id = models.BigAutoField(primary_key=True)
    role = models.CharField(max_length=100)
    user = models.OneToOneField(TblCustomuser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "tbl_Userrole"


class TblNotice(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    file = models.CharField(max_length=100, blank=True, null=True)
    notice = models.TextField(blank=True, null=True)
    status = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    created_by = models.ForeignKey(
        TblCustomuser, models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "tbl_notice"
