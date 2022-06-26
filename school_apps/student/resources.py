
from import_export import resources, fields, widgets
from student_management_app.models import Student, CustomUser

class StudentResource(resources.ModelResource):
    student_user = fields.Field(
        column_name='student_user',
        attribute='student_user_id',
        widget=widgets.ForeignKeyWidget(CustomUser, 'student_user__full_name'))    
    class Meta:
        model = Student
        fields = (
            'id','join_year','stu_id','roll_no','student_user','gender','shift','semester','section','course','faculty','program','status','contact',
            'permanent_address','temporary_address','dob','blood_group','optional_subject','gpa','previous_school_name',
        )
        
        # export_order = ('id', 'price', 'author', 'name')