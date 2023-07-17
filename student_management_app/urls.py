from django.urls import path

# from student_management_app.views.Admin_views import administrative_views
from school_apps.administrator import views as administrative_views

from school_apps.student.student_views import views as student_views
from school_apps.teacher.teacher_views import views as teacher_views
from school_apps.parents import views as parent_views
from school_apps.extrausers import views as user_views

from school_apps.admin_user import views as admin_user_views
from student_management_system.views import user_home, routine_home, academic_home


app_name = "admin_app"

urlpatterns = [
    # for teacher
    path("add_teacher/", teacher_views.add_teacher, name="add_staff"),
    path("manage_teacher/", teacher_views.manage_teacher, name="manage_staff"),
    path(
        "edit_teacher/<str:staff_id>/",
        teacher_views.edit_teacher,
        name="edit_staff"),
    path("search_teacher/", teacher_views.search_teacher, name="search_staff"),
    path(
        "delete_teacher/<str:staff_id>/",
        teacher_views.delete_teacher,
        name="delete_staff",
    ),
    # #for view_staff and  staff_file_view
    path(
        "view_teacher/<str:teacher_id>/",
        teacher_views.view_teacher,
        name="view_teacher",
    ),
    path(
        "add_teacher_document/<str:teacher_id>/",
        teacher_views.add_teacher_document,
        name="add_teacher_document",
    ),
    path(
        "edit_teacher_document/",
        teacher_views.edit_teacher_document,
        name="edit_teacher_document",
    ),
    path(
        "delete_teacher_document/<str:teacher_id>/<str:document_id>/",
        teacher_views.delete_teacher_document,
        name="delete_teacher_document",
    ),
    # for parent
    path("add_parent/", parent_views.add_parent, name="add_parent"),
    path("manage_parent/", parent_views.manage_parent, name="manage_parent"),
    path(
        "edit_parent/<str:parent_id>/",
        parent_views.edit_parent,
        name="edit_parent"),
    path(
        "delete_parent/<str:parent_id>/",
        parent_views.delete_parent,
        name="delete_parent",
    ),
    # for view_parent
    path(
        "view_parent/<str:parent_id>/",
        parent_views.view_parent,
        name="view_parent"),
    path(
        "add_parent_document/<str:parent_id>/",
        parent_views.add_parent_document,
        name="add_parent_document",
    ),
    path(
        "edit_parent_document/",
        parent_views.edit_parent_document,
        name="edit_parent_document",
    ),
    path(
        "delete_parent_document/<str:parent_id>/<str:document_id>/",
        parent_views.delete_parent_document,
        name="delete_parent_document",
    ),
    # for user like driver,receptionist------
    path("add_user/", user_views.add_user, name="add_user"),
    path("manage_user/", user_views.manage_user, name="manage_user"),
    path("edit_user/<str:user_id>/", user_views.edit_user, name="edit_user"),
    path(
        "delete_user/<str:user_id>/",
        user_views.delete_user,
        name="delete_user"),
    # for view_user
    path(
        "view_extrauser/<str:extrauser_id>/",
        user_views.view_extrauser,
        name="view_extrauser",
    ),
    path(
        "add_extrauser_document/<str:extrauser_id>/",
        user_views.add_extrauser_document,
        name="add_extrauser_document",
    ),
    path(
        "edit_extrauser_document/",
        user_views.edit_extrauser_document,
        name="edit_extrauser_document",
    ),
    path(
        "delete_extrauser_document/<str:extrauser_id>/<str:document_id>/",
        user_views.delete_extrauser_document,
        name="delete_extrauser_document",
    ),
    # for student
    path("add_student/", student_views.add_student, name="add_student"),
    path(
        "student_file_upload/",
        student_views.student_file_upload,
        name="student_file_upload",
    ),
    path(
        "student_id_card/<str:pk>/",
        student_views.student_id_card,
        name="student_id_card",
    ),
    path(
        "manage_student/",
        student_views.manage_student,
        name="manage_student"),
    path(
        "restore_inactive_student/<pk>/",
        student_views.restore_inactive_students,
        name="restore_inactive_students",
    ),
    path(
        "inactive_students/", student_views.inactive_students, name="inactive_students"
    ),
    path(
        "student_bulk_photo_upload/",
        student_views.student_bulk_photo_upload,
        name="student_bulk_photo_upload",
    ),
    path(
        "make_student_inactive/<pk>/",
        student_views.make_student_inactive,
        name="make_student_inactive",
    ),
    path(
        "edit_student/<str:student_id>/",
        student_views.edit_student,
        name="edit_student",
    ),
    path(
        "delete_student/<pk>/",
        student_views.delete_student,
        name="delete_student"),
    path(
        "attendance_view/",
        student_views.attendance_view,
        name="attendance_view"),
    # for view_student and student_file_view
    path(
        "view_student/<str:student_id>/",
        student_views.view_student,
        name="view_student",
    ),
    path(
        "add_student_document/<str:student_id>/",
        student_views.add_student_document,
        name="add_student_document",
    ),
    # path('edit_student_document/<str:student_id>/<str:document_id>/', student_views.edit_student_document, name="edit_student_document"),
    path(
        "edit_student_document/",
        student_views.edit_student_document,
        name="edit_student_document",
    ),
    path(
        "delete_student_document/<str:student_id>/<str:document_id>/",
        student_views.delete_student_document,
        name="delete_student_document",
    ),
    # for session year
    path(
        "add_manage_session/",
        administrative_views.add_manage_session_year,
        name="add_manage_session",
    ),
    path(
        "edit_session/<str:session_id>/",
        administrative_views.edit_session,
        name="edit_session",
    ),
    path(
        "delete_session/<str:session_id>/",
        administrative_views.delete_session,
        name="delete_session",
    ),
    # for student group
    path(
        "manage_studentgroup/",
        administrative_views.add_manage_group,
        name="add_manage_group",
    ),
    path(
        "edit_studentgroup/<str:group_id>/",
        administrative_views.edit_group,
        name="edit_group",
    ),
    path(
        "delete_studentgroup/<str:group_id>/",
        administrative_views.delete_group,
        name="delete_group",
    ),
    path(
        "add_sociallink/",
        administrative_views.add_sociallink,
        name="add_sociallink"),
    path(
        "manage_sociallink/",
        administrative_views.manage_sociallink,
        name="manage_sociallink",
    ),
    path(
        "edit_sociallink/<str:sociallink_id>/",
        administrative_views.edit_sociallink,
        name="edit_sociallink",
    ),
    path(
        "delete_sociallink/<str:sociallink_id>/",
        administrative_views.delete_sociallink,
        name="delete_sociallink",
    ),
    # for admin
    path(
        "add_system_admin/",
        admin_user_views.add_admin,
        name="add_system_admin"),
    path(
        "manage_system_admin/",
        admin_user_views.manage_system_admin,
        name="manage_system_admin",
    ),
    path(
        "edit_system_admin/<str:admin_id>/",
        admin_user_views.edit_system_admin,
        name="edit_system_admin",
    ),
    path(
        "delete_system_admin/<str:admin_id>/",
        admin_user_views.delete_system_admin,
        name="delete_system_admin",
    ),
    # Sidebar module manage
    path("user-management/", user_home, name="user-management"),
]
