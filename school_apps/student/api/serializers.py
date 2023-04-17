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
    # section = serializers.CharField(source='section.section_name', read_only=True)
    father_phone = serializers.CharField(source='guardian.father_phone', read_only=True)
    username = serializers.CharField(source='student_user.username', read_only=True)
    full_name = serializers.CharField(source='student_user.full_name', read_only=True)
    section = serializers.SerializerMethodField()

    '''I use get_section only to return None because ajax datatables return error if value is empty'''
    def get_section(self, obj):
        section_name = obj.section.section_name if obj.section else None
        return section_name

    class Meta:
        model=Student
        fields='__all__'
