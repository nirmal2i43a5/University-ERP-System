1.when i delete database then i get error for schoolsetting edit form blc i give id here here but it does not exists.so solve this error by commenting context_processor and then add setting for id = 1 to solve this error
2.i directly use Group.object.get(name = 'Admin') and othre too but when i delete database and then try to runserver then this group does not exists.SO apply better technique to solve this error
3.I get this error : django.db.utils.OperationalError: no such table: auth_group 
    So,to prevent this comment signals.py blc I give group name which is not created
4.using get_or_create in signal automatiaclly create group after u migrate data first commenting and tnen 


5. in django_forms/forms.py in section ,semester, subject form (This also gives me error blc i cant get this group name)

   staff_user = forms.ModelChoiceField(label = 'Teacher Name',
                                         queryset=CustomUser.objects.\
                                         filter(user_type = Group.objects.get(name = 'Teacher'))
                                         
                                     )

