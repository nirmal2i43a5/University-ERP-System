from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import StudentSerializer
from rest_framework import viewsets
from student_management_app.models import Student
from school_apps.log_history.models import UserLog
from django.db.models import Q

    

class StudentApiView(viewsets.ModelViewSet):
    queryset = Student.objects.filter(student_user__is_active = 1)
    serializer_class = StudentSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    # http_method_names = ['get']

            
    # search_fields = ['stu_id','roll_no','student_user__full_name','student_user__username''contact',]
    # def get_queryset(self, *args, **kwargs):
        
    #     if self.request.GET.get('stu_id'):
    #         data = Student.objects.filter(stu_id=self.request.GET.get('stu_id'))
    #         return data
    #     if self.request.GET.get('student_user__full_name'):
    #         data = Student.objects.filter(student_user__full_name=self.request.GET.get('student_user__full_name'))
    #         return data
    #     if self.request.GET.get('roll_no'):
    #         data = Student.objects.filter(roll_no=self.request.GET.get('roll_no'))
    #         return data
    #     if self.request.GET.get('student_user__username'):
    #         data = Student.objects.filter(student_user__username=self.request.GET.get('student_user__username'))
    #         return data
    #     if self.request.GET.get('contact'):
    #         data = Student.objects.filter(contact=self.request.GET.get('contact'))
    #         return data
    
    #     def get_serializer(self, *args, **kwargs):
    #         serializer_class = self.get_serializer_class()
    #     # print(serializer_class)
    #         kwargs['context'] = self.get_serializer_context()
    #         return serializer_class(*args, **kwargs)