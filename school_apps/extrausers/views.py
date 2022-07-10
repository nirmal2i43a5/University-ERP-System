import json
import datetime
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from student_management_app.django_forms.forms import (
                                          AddCustomUserForm,ExtraUserForm, DocumentFileForm, EditCustomUserForm
                                          )
from student_management_app.models import (
                                         CustomUser, Staff, Student,ExtraUser, DocumentFile, Branch
                                           )
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required,permission_required



@permission_required('student_management_app.add_extrauser', raise_exception=True)
def add_user(request):
    if request.method == 'POST':  
        custom_form = AddCustomUserForm(request.POST)
        extra_user_form = ExtraUserForm(request.POST, request.FILES)
        if custom_form.is_valid() and extra_user_form.is_valid():
            email = custom_form.cleaned_data["email"]
            full_name = custom_form.cleaned_data["full_name"]
            
            date_of_birth = str(request.POST.get('dob')) 
            if date_of_birth:#using this does not give error when u save empty date
                dob =  datetime.datetime.strptime(date_of_birth, "%Y-%m-%d").date()
            else:
                dob = None
            joining_date = str(request.POST.get('join_date'))
            join_date = datetime.datetime.strptime(joining_date, "%Y-%m-%d").date()
            
            if request.FILES.get('image'):
                image_url = request.FILES['image']
            else:
                image_url = None
                
            # group, created = Group.objects.get_or_create(name=user_role)
            branch = extra_user_form.cleaned_data['branch']
            print(branch, type(branch))
            try:
                group = Group.objects.get(name=branch.name)
                print('group:', Group, 'group:', group, 'typeof:' ,type(group),"~~~~~~~~~~~~~~~~~~~~~~~")
            except:
                group= Group.objects.none()
                print("in except")
            
            # try:
            fname = full_name.split()[0]
            extra_username = fname.lower()
            test_username = full_name.lower().replace(" ","_")
            print(test_username,"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
            # #be careful whether u use integertype or other 
            user = CustomUser.objects.create_user(
                username=test_username, password='password', email=email, 
            full_name=full_name)
            
            # user.extrauser.role = extra_user_form.cleaned_data['role']
            user.extrauser.address = extra_user_form.cleaned_data["address"]  
            user.extrauser.contact = extra_user_form.cleaned_data['contact']
            user.extrauser.gender = extra_user_form.cleaned_data['gender']  
            user.extrauser.religion = extra_user_form.cleaned_data['religion']
            user.extrauser.dob = dob  
            user.extrauser.join_date = join_date
            print("upto old")
            user.extrauser.branch = branch
            print("upto branch")

            if image_url != None:
                user.extrauser.image = image_url

            user.save()
            user.extrauser.save()
            print("upto save")
            # user.groups.add(group)
            print("upto group")
            messages.success(request, "Successfully Added User")
            return redirect('admin_app:manage_user')

            # except:
            #     messages.error(request, "Failed to Add User")
            #     return redirect('admin_app:add_user')
        # else:
        #     return HttpResponse("Invalid form")
    else:
        custom_form = AddCustomUserForm()
        extra_user_form = ExtraUserForm()
      

    context = {'custom_form': custom_form, 'extra_user_form': extra_user_form, 'title':'Add Extra User'}
    return render(request, 'users/add_user.html', context)


@permission_required('student_management_app.view_extrauser', raise_exception=True)
def manage_user(request):
    user = ExtraUser.objects.all()
    context = {'users': user, 'title':'Manage Extra User'}
    return render(request, 'users/manage_user.html', context)


@permission_required('student_management_app.change_extrauser', raise_exception=True)
def edit_user(request, user_id):
    extra_user_form_instance = get_object_or_404(ExtraUser, extra_user=user_id)
    custom_form_instance = get_object_or_404(CustomUser,id = user_id )
   
    if request.method == 'POST':
        extra_user_form = ExtraUserForm(request.POST, request.FILES, instance=extra_user_form_instance)
        custom_form = EditCustomUserForm(request.POST, instance = custom_form_instance)
        
        try:
            if extra_user_form.is_valid() and custom_form.is_valid():
                extra_user_form.save()
                custom_form.save()
                messages.success(request, f'Successfully Edited {custom_form_instance.username}')
                return redirect('admin_app:manage_user')
            
        except:

            messages.error(request, f'Failed to Update {custom_form_instance.username}')
            return redirect('admin_app:edit_staff')
    else:
        extra_user_form = ExtraUserForm(instance=extra_user_form_instance)
        custom_form = EditCustomUserForm(instance = custom_form_instance)

    context = {'extra_user_form':extra_user_form, 'custom_form':custom_form, 'title':'Edit ExtraUser'}
    return render(request, 'users/edit_user.html', context)


@permission_required('student_management_app.delete_extrauser', raise_exception=True)
def delete_user(request, user_id):
    try:
        user = get_object_or_404(ExtraUser, extra_user = user_id)#i am using custom user so i use staff_user_id instead of normal staff id = staff_id
        user.delete()
        messages.success(request, f'{user.extra_user.username} is Deleted Successfully')
        return redirect('admin_app:manage_user')
    except:
        messages.error(request, f'Failed To Delete {user.extra_user.username}')
        return redirect('admin_app:manage_user')


# this is for ajax part (my ajax is success with title with title but file cannot upload so i am using above views for )
@csrf_exempt
@permission_required('student_management_app.add_extrauser_document', raise_exception=True)
def add_extrauser_document(request, extrauser_id):#for ajax part
    extrauser = get_object_or_404(ExtraUser, id = extrauser_id)
    
    if request.method=="POST":
        form=DocumentFileForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            document_id =request.POST["documentid"]#this is hidden field 
            print(document_id)
            title=request.POST.get("title")
            file=request.FILES["file"]  
            
            if(document_id==''):#if there is no product id then it has to insert data clicking on save button
                document = form.save(commit = False)
                #when i add_file then it must be the file of particular student with their respective id and i can retrieve this using _set see in view_student views function
                document.extra_user = extrauser
                
                
            else:#if not id then edit data clicking on save button 
                document = form.save(commit = False)
                document.id = document_id#for updating particular field
                document.extra_user = extrauser
            
        
            #when i add_file then it must be the file of particular extrauser with their respective id and i can retrieve this using _set see in view_extrauser views function
            document.save()
            document_value=DocumentFile.objects.filter(extra_user=extrauser).values()#this filter data to show in ajax but commit filter for database
            document_data =list(document_value)#change to json
            return JsonResponse({'status':'True','document_data':document_data, 'message':'Document is Successfully Saved'},safe=False)
        else:
            return JsonResponse({'status':0})
       
       
# logic for student_profile and add_submit data with modal form
@permission_required('student_management_app.view_extrauser_profile', raise_exception=True)
def view_extrauser(request, extrauser_id):
    try:
        extrauser = get_object_or_404(ExtraUser, id = extrauser_id)#this is the  student_id  come from student not from customuser<check in view click>
    except:
        return render(request, '404.html')

    #retrieve DocumentFile upload for particualr student using foreign key    
    extrauser_files =  extrauser.documentfile_set.all()
    
    #this is for adding document form that is in view_student
    form = DocumentFileForm()
    context = {'extrauser':extrauser,
               'extrauser_files':extrauser_files,
               'form':form
               }
    return render(request, 'users/views/main_view.html',context)


#this is for edit student document(for edit it also goes to else part in add)
@csrf_exempt
@permission_required('student_management_app.edit_extrauser_document', raise_exception=True)
def edit_extrauser_document(request):
    id=request.POST.get('documentid')
    if request.method=="POST":
        id=request.POST.get('documentid')
        
    document= get_object_or_404(DocumentFile, pk=id)
    
    file_data = json.dumps(str(document.file)) #you can't serialize the object, because it's an Image. You have to serialize the string representation of it's path.
    
    document_data={"id":document.id, "title":document.title,"file":file_data }
    """i cant see file but cant see title instance while click edit button .because i am not passing--
    "file":file as it gives file field cannt be json serailize.so ,I will solve this problem in future
    """
    return JsonResponse(document_data,safe=False)


@permission_required('student_management_app.delete_extrauser_document', raise_exception=True)
def delete_extrauser_document(request,extrauser_id, document_id):
    try:
        document = get_object_or_404(DocumentFile, id = document_id)#i am using custom user so i use staff_user_id instead of normal document id = staff_id
        document.delete()
        messages.success(request, f'Document is Deleted Successfully')
        return redirect('admin_app:view_extrauser', extrauser_id)
    except:
        messages.error(request, 'Failed To Delete Document')
        return redirect('admin_app:view_extrauser', extrauser_id)


def extrauser_log(request):
    extrausers_logs = ExtraUser.history.all()
    context = {
        'title':'ExtraUser Log',
         'extrausers_logs':extrausers_logs,
    }
    return render(request,'users/loghistory/history.html',context)

def delete_log(request):
    ExtraUser.history.all().delete()
    messages.success(request,"User logs are deleted successfully.")
    return redirect('extrauser:user_log')
    