# from uploadcsv.models import Section, Student
# from django.http.response import HttpResponse
# from django.shortcuts import render
# import csv, io
# from .models import *
# ​
# # Create your views here.
# ​
# def index(request):
#     if request.method == "GET":
#         return render(request, 'uploadcsv/index.html')
#     else:
#         csv_file = request.FILES['file']
# ​
#     if not csv_file.name.endswith('.csv'):
#         print("Invalid file")
    
#     data_set = csv_file.read().decode('UTF-8')
#     io_string = io.StringIO(data_set)
#     next(io_string)
# ​
#     for column in csv.reader(io_string, delimiter=',', quotechar="|"):
#         batch = column[1]
#         stu_id = column[2]
#         roll_no = column[3]
#         name = column[4]
#         gender = column[5]
#         shift = column[6]
#         section = Section.objects.get_or_create(name = column[7])
#         course = column[8]
#         faculty = column[9]
#         program = column[10]
#         status = column[11]
#         home_phone = column[12]
#         contact = column[13]
# ​
#         parent_obj = Parent.objects.create(
#             father_name = column[14],
#             father_phone = column[15],
#             mother_name = column[16],
#             mother_phone = column[17],
#             local_guardian_name= column[18],
#             local_guardian_phone =column[19]
#         )
# ​
#         permanent_address = column[20]
#         temporary_address = column[21]
#         dob_es = column[22]
#         dob_bs = column[23]
#         blood_group = column[24]
#         optional_subject = column[25]
#         gpa = column[26]
# ​
#         student_obj= 
# ​
#     return HttpResponse("OK")
