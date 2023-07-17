from rest_framework.fields import ReadOnlyField
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from student_management_app.models import CustomUser
from school_apps.log_history.models import UserLog


class CustomUserSerializer(ModelSerializer):
    # employee = EmployeeSerializer()
    # employee_id = serializers.ReadOnlyField(source="employee.employee_id",default="")
    # employee_name = serializers.ReadOnlyField(source="employee.full_name",default="")
    # employee_branch = serializers.ReadOnlyField(source="employee.branch_id.branch_name",default="")
    # employee_department = serializers.ReadOnlyField(source="employee.department_id.name",default="")

    class Meta:
        model = CustomUser
        fields = "__all__"


class UserLogSerializer(ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = UserLog
        fields = "__all__"
