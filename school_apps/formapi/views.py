from django.http.response import HttpResponse, JsonResponse
from student_management_app.models import Course, Department
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets
from .models import formTemplate
from school_apps.enquiry.models import Application
from .serializers import formTemplateSerializer, ApplicationSerializer
from rest_framework.authtoken.models import Token
from django.views.generic import ListView
from django.core import serializers
import json

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_detail_view(request, pk):
    
    try:
        selected_formTemplate=formTemplate.objects.get(pk=pk)
    except formTemplate.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    dept=selected_formTemplate.department
    courses = Course.objects.filter(department=dept)
    courses_query = courses.values_list('course_name','course_code')
    courses_list=list(courses_query)
    courses_json = json.dumps(courses_list)
    
    print(courses_query,'\n')
    print(courses_list,'\n')
    print(courses_json,'\n')

    serializer = formTemplateSerializer(selected_formTemplate)
    data = serializer.data
    data['prepopulate']={'courses':courses_list}
    return Response(data)


@api_view(['POST',],)
@permission_classes([IsAuthenticated])
def api_create_view(request):
    print("in view")
    serializer = formTemplateSerializer( data=request.data)
    print(request.data)

    if serializer.is_valid():
        print("valid block")
        data = serializer.validated_data
        for item in data:
            print(item)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print("invalid block")
        print("serializer data: " , serializer.data)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

@api_view(['PUT','PATCH'])
@permission_classes([IsAuthenticated])
def api_update_view(request, pk):
    try:
        selected_formTemplate=formTemplate.objects.get(pk=pk)
    except formTemplate.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = formTemplateSerializer(selected_formTemplate, data=request.data)
    data = {}
    if serializer.is_valid():
        print(serializer.validated_data)
        serializer.save()
        data['success']="Update successful"
        return Response(data=data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
@api_view(['GET',])
def allforms(request):
    templates = formTemplate.objects.all()
    count=1
    template_array=[]

    for item in templates:
        serializer = formTemplateSerializer(item)
        template_array.append(serializer.data)

    data = template_array
    return Response(data)

def viewtemplates(request):
    context = {"sess":request.session.session_key}
    return render(request, 'formapi/view_templates.html',context=context)

def formbuilder(request):
    token = Token.objects.get(user=request.user.id).key
    dept_id = request.POST['dept_id']
    dept = Department.objects.get(pk=request.POST['dept_id'])
    context = {"sess":request.session.session_key,
                "token":token,
                "dept_id":dept_id,
                'dept':dept}
    return render(request, 'formapi/form_builder.html',context=context)

def formbuilder_select(request):
    token = Token.objects.get(user=request.user).key
    dept = Department.objects.all()
    context = {"department":dept,
                }
    return render(request, 'formapi/form_builder_dept_select.html',context=context)

def formbuilder_select_edit(request):
    token = Token.objects.get(user__username='admin').key
    dept = Department.objects.all()
    context = {"department":dept,
                }
    return render(request, 'formapi/form_builder_dept_select.html',context=context)

class formTemplateListView(ListView):
    model = formTemplate
    context_object_name = 'form'
    template_name='formapi/formbuilder_edit_select.html'

def admissionform_select(request):
    token = Token.objects.get(user__username='admin').key
    dept = Department.objects.all()
    context = {"department":dept,
                }
    return render(request, 'formapi/admission_form_dept_select.html',context=context)

def formsubmit(request):
    token = Token.objects.get(user=request.user.id).key
    dept_id = request.POST['dept_id']
    dept = Department.objects.get(pk=request.POST['dept_id'])
    try:
        form = formTemplate.objects.get(department=dept, is_used=True)
        form_id=form.pk

        context = {"sess":request.session.session_key,
                "token":token,
                "dept_id":dept_id,
                'dept':dept,
                "form_id":form_id}
        return render(request, 'formapi/admission_form.html',context=context)
    except:
        form=formTemplate.objects.none()
        context = {"sess":request.session.session_key,
                "token":token,
                "dept_id":dept_id,
                'dept':dept,
                }
        return render(request, 'formapi/admission_form.html',context=context)

    

@api_view(['POST',],)
@permission_classes([IsAuthenticated])
def form_submit_view(request):
    print("in view")
    serializer = ApplicationSerializer( data=request.data)
    print(request.data)

    if serializer.is_valid():
        print("valid block")
        data = serializer.validated_data
        for item in data:
            print(item)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print("invalid block")
        print("serializer data: " , serializer.data)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

# @api_view(['GET',])
def edit_form(request, pk):
    form_id=pk
    form = formTemplate.objects.get(pk=pk)
    dept_id=form.department.pk
    token = Token.objects.get(user=request.user.id).key
    context = {'form_id':form_id,
                'dept_id':dept_id,
                'token':token}
    return render(request, 'formapi/form_edit.html', context=context)

# @api_view(['POST',],)
# def return_admission_form(request,pk):
#     Depart


class formTemplateView(viewsets.ModelViewSet):  
    serializer_class = formTemplateSerializer   
    queryset = formTemplate.objects.all()  

@api_view(['GET',],)
@permission_classes([IsAuthenticated])
def prepopulate(request, pk):
    form_id=pk
    form = formTemplate.objects.get(pk=pk)
    dept=form.department
    courses = Course.objects.filter(department=dept)
    courses_query = courses.values_list('course_name','course_code')
    courses_list=list(courses_query)
    # courses_json = json.dumps(courses_list)

    courses_json = {}

    courses_dict = {}
    for item in courses_query:
        courses_dict[item[1]]=item[0]
    
    courses_list=[]
    
    for id, item in enumerate(courses_dict):
        dump_json = {}
        dump_json["key"]=item
        dump_json["label"]=courses_dict[item]
        # courses_json[id]=dump_json
        # id+=1
        courses_list.append(dump_json)
        # print(dump_json)

    # print(courses_json)
    # print(courses_dict)
    serializer = formTemplateSerializer(form)
    data = serializer.data
    data['courses']=courses_list
    return Response(data)

@api_view(['GET',],)
@permission_classes([IsAuthenticated])
def prepopulate_courses(request, pk):
    dept=Department.objects.get(pk=pk)
    courses = Course.objects.filter(department=dept)
    courses_query = courses.values_list('course_name','course_code')
    courses_list=list(courses_query)
    form = formTemplate.objects.get(department=dept, is_used=True)
    # courses_json = json.dumps(courses_list)

    courses_json = {}

    courses_dict = {}
    for item in courses_query:
        courses_dict[item[1]]=item[0]
    
    courses_list=[]
    
    for id, item in enumerate(courses_dict):
        dump_json = {}
        dump_json["key"]=item
        dump_json["label"]=courses_dict[item]
        # courses_json[id]=dump_json
        # id+=1
        courses_list.append(dump_json)
        # print(dump_json)

    # print(courses_json)
    # print(courses_dict)
    # serializer = formTemplateSerializer(form)
    # data = serializer.data
    # data['courses']=courses_list

    dict={}
    dict['courses']=courses_list
    
    return Response(dict)

def form_selection(request):
    department =Department.objects.all()

    context ={
        'department':department
    }
    
    if request.method=='GET':
        return render(request, 'formapi/form_select.html',context=context)
    else:
        selected_department= Department.objects.get(pk=request.POST['dept_id'])
        templates = formTemplate.objects.filter(department=selected_department)

        context['templates']=templates
        return render(request, 'formapi/form_select.html',context=context)