from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import StudentSerializer
from rest_framework import viewsets
from student_management_app.models import Student

    

class StudentApiView(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    # http_method_names = ['get']

            
    # def get_queryset(self, *args, **kwargs):
    #     queryset_list =Branch.objects.filter(is_deleted = False)
    #     if self.request.GET.get("trash"):
    #         queryset_list = Branch.objects.filter(is_deleted = True)
    #     query = self.request.GET.get("name")
    #     if query:
    #         queryset_list = queryset_list.filter(
    #                 Q(branch_name__icontains=query)|
    #                 Q(branch_id__icontains = query)
    #                 ).distinct()
    #     return queryset_list