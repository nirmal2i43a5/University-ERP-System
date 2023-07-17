from django.urls import path
from school_apps.classroom.views import (
    classroom,
    plus_two_class,
    bachelor_class,
    master_class,
    classroom_contents,
)


app_name = "classroom"

urlpatterns = [
    path("school/classroom/", classroom, name="school-classroom"),
    path("plus-two/classroom/", classroom, name="plus-two-classroom"),
    path("bachelor/classroom/", classroom, name="bachelor-classroom"),
    path("master/classroom/", classroom, name="master-classroom"),
    path(
        "school/classroom/<str:pk>/",
        classroom_contents,
        name="school-classroom-contents",
    ),
    path(
        "plus-two/classroom/<str:pk>/",
        classroom_contents,
        name="plus-two-classroom-contents",
    ),
    path(
        "bachelor/classroom/<str:pk>/",
        classroom_contents,
        name="bachelor-classroom-contents",
    ),
    path(
        "master/classroom/<str:pk>/",
        classroom_contents,
        name="master-classroom-contents",
    ),
]
