1)Before migrating data to database comment below path in student_management_system/urls.py and uncomment after you migrate
   # path('', include('school_apps.classroom.urls',namespace='classroom')),

2)Before loading fixtures comment 
   create_user_profile and save_user_profile in student_management_app/signals.py other wise I may get duplicate id error create by post save

   and then uncomment it

3)Admin Group is for Plus-Two level
4)Even after i create superadmin from i may there 