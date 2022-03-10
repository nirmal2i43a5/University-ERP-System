from rest_framework.fields import ReadOnlyField
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import CustomUser
from middleware.user_log.models import UserLog
from prabhu_apps.members.employee.api.serializers import EmployeeSerializer

class UserSerializer(ModelSerializer):
    employee = EmployeeSerializer()
    employee_id = serializers.ReadOnlyField(source="employee.employee_id",default="")
    employee_name = serializers.ReadOnlyField(source="employee.full_name",default="")
    employee_branch = serializers.ReadOnlyField(source="employee.branch_id.branch_name",default="")
    employee_department = serializers.ReadOnlyField(source="employee.department_id.name",default="")

    class Meta:
        model = CustomUser
        fields = ['id','employee','employee_id','employee_name','employee_branch','employee_department','is_staff','email','date_joined','last_login']

class UserLogSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserLog
        fields = '__all__'