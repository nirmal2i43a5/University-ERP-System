from django.urls import path
from .views import * 
app_name = 'library'
urlpatterns = [
    #-------------------------------- login logout url -----------------------------------------
    # path('login/', login_page, name='login'),
    # path('logout/', logout_page, name='logout'),

    # ---------------------------------- Book categories ------------------------------------------
    path('category_list/', category_list, name='category_list'),
    path('add_categories/', CategoryAddView, name='add_categories'),
    path('edit_categories/<int:pk>', CategoryUpdateView, name='edit_categories'),
    path('view_category/<int:pk>', CategoryFullView, name='view_categories'),
    path('del_categories/<int:pk>', CategoryDeleteView.as_view(), name='del_categories'),

    #--------------------------------- book url --------------------------------------------------
    path('book_list/', book_list, name='book_list'),
    path('add_book/', add_book, name='add_book'),
    path('view_book/<int:pk>', view_book, name='view_book'),
    path('edit_book/<int:pk>', edit_book, name='edit_book'),
    path('del_book/<int:pk>', BookDeleteView.as_view(), name='del_book'),
    path('', book_list, name='book_list'),
    #---------------------------------- member url ------------------------------------------------
    path('member_list/', member_list, name='member_list'),
    path('add_member/', add_member, name='add_member'),
    path('edit_member/<int:pk>', edit_member, name='edit_member'),
    path('member_detail/<int:pk>', member_detail, name='member_detail'),
    path('del_member/<int:pk>', MemberDeleteView.as_view(), name='del_member'),

    #----------------------------------- book issue url ---------------------------------------------- 
    path('book_issue_list/', book_issue_list, name='book_issue_list'),
    path('issue/create/<int:pk>',BookIssueCreateView.as_view(),name='bookissue-create'),#pk for member
    # path('book_issue/', book_issue, name='book_issue'),
    path('book_issue_edit/<int:issue_id>', book_issue_edit, name='book_issue_edit'),
    path('book_issue_detail/<int:pk>', book_issue_detail.as_view(), name='book_issue_detail'),
    path('del_book_issue/<int:pk>', BookIssueDeleteView.as_view(), name='del_book_issue'),

    #------------------------------------ book return url ---------------------------------------------
    # path('book_return/', book_return, name='book_return'),
    path('<int:pk>/return/',BookReturnView.as_view(),name='book-return'),
    path('book_return_list/', book_return_list, name = 'book_return_list'),
    path('book_return/', book_return, name='book_return'),

    path('book_return_edit/<int:pk>', book_return_edit, name='book_return_edit'),
    path('book_return_detail/<int:pk>', book_return_detail, name='book_return_detail'),
    path('del_book_return/<int:pk>', BookReturnDeleteView.as_view(), name='del_book_return'),

    # ------------------------------------ book renew url -----------------------------------------------
    path('book_renew_list/', book_renew_list, name='book_renew_list'),
    path('book_renew/', book_renew, name='book_renew'),
    path('book_renew_edit/<int:pk>', book_renew_edit, name='book_renew_edit'),
    path('book_renew_detail/<int:pk>', book_renew_detail, name='book_renew_detail'),
    path('del_book_renew/<int:pk>', BookRenewDeleteView.as_view(), name='del_book_renew'),
]