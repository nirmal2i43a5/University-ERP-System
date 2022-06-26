from rest_framework import serializers
from student_management_app.models import Student,Parent
# from django_countries.serializers import CountryFieldMixin



# class ParentSerializer(serializers.ModelSerializer):
#      class Meta:
#         model=Parent
#         fields='__all__'
    
    
    
class StudentSerializer(serializers.ModelSerializer):
    # guardian = ParentSerializer()
    semester = serializers.CharField(source='semester.name', read_only=True)
    section = serializers.CharField(source='section.section_name', read_only=True)
    # section = serializers.SerializerMethodField(read_only = True)
    father_phone = serializers.CharField(source='guardian.father_phone', read_only=True)
    username = serializers.CharField(source='student_user.username', read_only=True)
    full_name = serializers.CharField(source='student_user.full_name', read_only=True)
    class Meta:
        model=Student
        fields='__all__'
