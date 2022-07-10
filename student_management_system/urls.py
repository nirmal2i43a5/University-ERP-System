"""student_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.views.generic.base import RedirectView
from django.views.i18n import JavaScriptCatalog
from student_management_system.views import get_user_by_role_ajax
from student_management_system.views import home as main_home
from student_management_system.views import (superuser_home,
# a_level_home,bachelor_home,master_home,
                                             mass_delete
                                            )
from django.contrib.auth import views as auth_views


# from rest_framework import routers
# from school_apps.formapi import views
# router =routers.SimpleRouter()
# router.register(r'forms', views.formTemplateView, 'forms')  

urlpatterns = [
    # path('api/', include(router.urls)) ,
    path('home/',superuser_home, name ="superuser_home"),
    # path('home/', admin_home,name = 'admin-home'),
    
    
    path('api/v1/', include('student_management_system.api', namespace='api')),
    path('admin/', admin.site.urls),
    # path('logs/', HistoryLogs.as_view(), name ="history_log"),
    path('common/mass/delete/<app>/<model>/', mass_delete, name ="mass_delete"),
    path('dashboard/', main_home.as_view(), name ="home"),
   
    # path('a_level_home/',a_level_home,name = "a_level_home"),
    # path('bachelor_home/',bachelor_home,name = "bachelor_home"),
    # path('master_home/',master_home,name = "master_home"),
    path('get_user_by_role/', get_user_by_role_ajax, name ="get_user_by_role"),
    path('',include('student_management_app.urls',namespace='admin_app')),
    path('',include('school_apps.teacher.urls',namespace='teacher')),
    path('',include('school_apps.student.urls',namespace='student')),
    path('parent/',include('school_apps.parents.urls',namespace='parent')),
    path('viewer/',include('viewer.urls',namespace='viewer')),

    path('',include('school_apps.courses.urls',namespace='courses')),
    path('extrauser/',include('school_apps.extrausers.urls',namespace='extrauser')),
    path('',include('school_apps.customusers.urls',namespace='customuser')),
    path('',include('school_apps.announcement.urls',namespace='announcement')),
    path('administrator/',include('school_apps.administrator.urls',namespace='administrator')),
    path('',include('school_apps.attendance.urls',namespace='attendance_app')),
    path('',include('school_apps.school_settings.urls',namespace='setting_app')),
    path('',include('school_apps.user_profile.urls')),
    path('',include('school_apps.role_permission.urls',namespace='role_app')),
    path('notifications/', include('school_apps.notifications.urls',namespace='notifications')),
    path('', include('school_apps.academic.urls',namespace='academic')),
    path('', include('school_apps.email_sms.urls',namespace='email_sms')),
    path('', include('school_apps.transports.urls',namespace='transport')),
    path('', include('school_apps.routine.urls',namespace='routine')),
    path('', include('school_apps.complain.urls',namespace='complain')),
    path('library/', include('school_apps.library.urls',namespace='library')),
    path('', include('school_apps.student_certificate.urls',namespace='certificate')),
    path('', include('school_apps.log_history.urls',namespace='user_history')),
    path('', include('school_apps.classroom.urls',namespace='classroom')),
     path('exam/',include('school_apps.exam.urls',namespace='exam')),
     
    path('schedule/',include('schedule.urls')),
    
    # ------------------------------------I have commented the functionality of this app -----------------------------
    # path('',include('school_apps.inventory.urls',namespace='inventory')),
    # path('visitor/',include('school_apps.visitor.urls',namespace='visitor')),
    # path('enquiry/',include('school_apps.enquiry.urls',namespace='enquiry')),
    # path('api/', include('school_apps.formapi.urls')),
    
    
    
    # ------------------------------------------------------------------------------------------------------
      
    #For resetting password via email follow below four link 
    path('password/reset/',auth_views.PasswordResetView.as_view(template_name = 'passwordreset/password_reset_email.html'), 
		 name = "password_reset"),
	
	path('password/reset/done/',auth_views.PasswordResetDoneView.as_view(template_name = 'passwordreset/password_reset_sent.html'), 
		 name = "password_reset_done"),
	
	path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='passwordreset/password_reset_form.html'),
		 name="password_reset_confirm"),  
	   
	 #<token> check  for valid user or not--><uidb64> user id encoded in base 64--this email is sent to the user
	 #<uidb64> helps to know user who request for password
	path('reset/complete/',auth_views.PasswordResetCompleteView.as_view(template_name='passwordreset/password_reset_complete.html'),
		 name="password_reset_complete"),
    

    
    #for admin js
    path('jsi18n', JavaScriptCatalog.as_view(), name='js-catlog'),
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
    ),

    #api
    
    
    
]#+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

handler404 = 'student_management_system.views.error_404'

if settings.DEBUG:
    # import debug_toolbar
    # urlpatterns = [path('__debug__/', include('debug_toolbar.urls'))] + urlpatterns
    
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # if apps.is_installed("silk"):
    # urlpatterns = [path("silk/", include("silk.urls",namespace='silk'))] + urlpatterns
    
    
    

    
    
