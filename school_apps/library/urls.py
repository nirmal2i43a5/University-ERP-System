from django.urls import path
from .views import *
from student_management_system.views import library_home

app_name = "library"
urlpatterns = [
    # ---------------------------------- Book categories ---------------------
    path("book/category/", category_list, name="category_list"),
    path("add_categories/", add_category, name="add_categories"),
    path("edit_categories/<int:pk>", view_category, name="edit_categories"),
    path("view_category/<int:pk>", update_category, name="view_categories"),
    path(
        "del_categories/<int:pk>", CategoryDeleteView.as_view(), name="del_categories"
    ),
    # --------------------------------- book url -----------------------------
    path("book_list/", book_list, name="book_list"),
    path("add_book/", add_book, name="add_book"),
    path("view_book/<int:pk>/", view_book, name="view_book"),
    path("edit_book/<int:pk>/", edit_book, name="edit_book"),
    path("del_book/<int:pk>/", BookDeleteView.as_view(), name="del_book"),
    # ---------------------------------- member url --------------------------
    path("member_list/", member_list, name="member_list"),
    path("add_member/", add_member, name="add_member"),
    path("edit_member/<int:pk>/", edit_member, name="edit_member"),
    path("member_detail/<int:pk>/", member_detail, name="member_detail"),
    path(
        "del_member/<int:pk>/",
        MemberDeleteView.as_view(),
        name="del_member"),
    # ----------------------------------- book issue url ---------------------
    path("book_issue_list/", book_issue_list, name="book_issue_list"),
    # path('issue/create/<int:pk>/',BookIssueCreateView.as_view(),name='bookissue-create'),#pk for member
    # path('issue_member_list/', issue_member_list, name='issue_member_list'),
    path("renew_issue/", renew_issue, name="renew_issue"),
    path("return_issue/", return_issue, name="return_issue"),
    path("book_issue/", book_issue, name="book_issue"),
    path("book_issue_edit/<int:issue_id>/", book_issue_edit, name="book_issue_edit"),
    path(
        "book_issue_detail/<int:pk>/",
        book_issue_detail.as_view(),
        name="book_issue_detail",
    ),
    path(
        "del_book_issue/<int:pk>/", BookIssueDeleteView.as_view(), name="del_book_issue"
    ),
    # ------------------------------------ book return url ---------------------------------------------
    # path('<int:pk>/return/',BookReturnView.as_view(),name='book-return'),#pk is member
    path("book_return_list/", book_return_list, name="book_return_list"),
    path(
        "issue_list_for_return/<int:pk>/",
        issue_list_for_return,
        name="issue_list_for_return",
    ),
    path("book_return/<int:pk>/", book_return, name="book_return"),
    path("book_return_edit/<int:pk>/", book_return_edit, name="book_return_edit"),
    path("book_return_detail/<int:pk>/", book_return_detail, name="book_return_detail"),
    path(
        "del_book_return/<int:pk>/",
        BookReturnDeleteView.as_view(),
        name="del_book_return",
    ),
    # ------------------------------------ book renew url -----------------------------------------------
    path("book_renew_list/", book_renew_list, name="book_renew_list"),
    path(
        "issue_list_for_renew/<int:pk>/",
        issue_list_for_renew,
        name="issue_list_for_renew",
    ),
    path("book_renew_edit/<int:pk>/", book_renew_edit, name="book_renew_edit"),
    path("book_renew_detail/<int:pk>/", book_renew_detail, name="book_renew_detail"),
    path(
        "del_book_renew/<int:pk>/", BookRenewDeleteView.as_view(), name="del_book_renew"
    ),
    path("book_renew/<int:pk>/", book_renew, name="book_renew"),
    # ------------------------------------ Fine Management url -----------------------------------------------
    path("set_default_fine/", set_default_fine, name="set_default_fine"),
    path("add_library_fine/", add_library_fine, name="add_library_fine"),
    path("library_fine_list/", library_fine_list, name="library_fine_list"),
    path("edit_library_fine/<int:pk>/", edit_library_fine, name="edit_library_fine"),
    path(
        "del_library_fine/<int:pk>/",
        LibraryFineDeleteView.as_view(),
        name="del_library_fine",
    ),
    path("library-management/", library_home, name="library-management"),
]
