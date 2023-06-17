from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import StudentSerializer
from rest_framework import viewsets
from student_management_app.models import Student
from django.db.models import Q
from django.db import connection
from django_filters import filters
from rest_framework_datatables.django_filters.backends import DatatablesFilterBackend
from rest_framework_datatables.django_filters.filterset import DatatablesFilterSet
from rest_framework_datatables.django_filters.filters import GlobalFilter
import django_filters
from django.db import models

class GlobalCharFilter(GlobalFilter, filters.CharFilter):
    pass

class StudentGlobalFilter(DatatablesFilterSet):
    """Filter name, artist and genre by name with icontains"""

    stu_id = GlobalCharFilter(field_name='stu_id', lookup_expr='icontains')#for this i need to use student_user in serializer to assume it as foreign key

    full_name = GlobalCharFilter(field_name='student_user__full_name', lookup_expr='icontains')#for this i need to use student_user in serializer to assume it as foreign key
    username = GlobalCharFilter(field_name='student_user__username', lookup_expr='icontains')
    email = GlobalCharFilter(field_name='student_user__email', lookup_expr='icontains')

    class Meta:
        model = Student
        fields = '__all__'
        filter_overrides = {
            models.ImageField: {
                'filter_class': django_filters.CharFilter,
                # 'extra': lambda f: {
                #     'lookup_expr': 'exact',
                # },
            },
        }


class StudentApiView(viewsets.ModelViewSet):
    queryset = Student.objects.\
    select_related('student_user', 'semester', 'section', 'guardian').\
    filter(student_user__is_active = 1)
    # values('id','image','stu_id','student_user__full_name',
    #                                                                                                     'semester__name',
    #                                                                                                     'section__section_name',
    #                                                                                                     'guardian__father_phone',
    #                                                                                                     'contact',
    #                                                                                                     'student_user__username',
    #                                                                                                     )
                                                                                                        
    serializer_class = StudentSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DatatablesFilterBackend,)
    filterset_class = StudentGlobalFilter
    http_method_names = ['get']

            
    def dispatch(self, *args, **kwargs):
        response =  super().dispatch(*args, **kwargs)
        print('------------------------employee api queries-----------------------------: {}'.format(len(connection.queries)))
        return response
    
