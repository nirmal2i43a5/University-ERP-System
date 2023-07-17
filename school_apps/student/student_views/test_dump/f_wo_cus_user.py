# # import pandas as pd
# import csv,io
# def student_file_upload(request):
#     if request.method == "GET":
#         return render(request, 'admin_templates/students/file_upload.html')
#     else:
#         csv_file = request.FILES['studentfile']
#     if not csv_file.name.endswith('.csv'):
#         print("Invalid file")
#     data_set = csv_file.read().decode('latin-1')
#     io_string = io.StringIO(data_set)

#     next(io_string)
#     file_data = csv.reader(io_string, delimiter=',', quotechar="|")
#     for column in file_data:
#         # print(column)
#         batch = column[1]#batch
#         # print(batch,"-----batch-----------")
#         student_id = column[2]
#         # print(student_id,"------stu id---------------")
#         roll_no = column[3]
#         name = column[4]
#         gender = column[5]
#         shift = column[6]
#         section = column[7]
#         course = column[8]
#         faculty = column[9]
#         program = column[10]
#         status = column[11]
#         home_phone = column[12]
#         contact = column[13]
#         permanent_address = column[21]
#         temporary_address = column[22]
#         dob_es = column[23]
#         dob_bs = column[24]
#         blood_group = column[25]
#         optional_subject = column[26]
#         gpa = column[27]
#         # parsing date
#         # dob = datetime.datetime.strptime(dob_es, "%d/%m/%y")

#         parent_obj = Parent.objects.create(
#         home_phone = home_phone,
#         father_name=column[14],
#         father_phone=column[15],
#         mother_name=column[16],
#         mother_phone=column[17],
#         local_guardian_name=column[18],
#         local_guardian_phone=column[19]
#          )

#         fname = column[4].split()[0]
#         # print(fname,"-------------------")
#         stu_username = fname + f'{student_id}'
#         # print(stu_username,"-------------username student")
#         role = Group.objects.get(name = 'Student')

#         # customuser_object = CustomUser.objects.create_user(
#         #         username = stu_username, password='password', user_type=role, full_name=column[4])

#         sem = Semester.objects.get(name = batch)
#         # print(customuser_object,"--------------customur obj")
#         student_obj = Student.objects.create(
#             semester=sem,
#             stu_id= column[2],
#             roll_no=roll_no,
#             # student_user =  CustomUser.objects.create_user(username = column[2], password='password', user_type=role, full_name=column[4]),
#             gender = gender,
#             shift=shift,
#             course=course,
#             faculty=faculty,
#             program = program,
#             status=status,
#             contact=contact,
#             guardian = parent_obj,
#             permanent_address = permanent_address,
#             temporary_address = temporary_address,
#             dob = dob_es,
#             blood_group = blood_group,
#             # optional_subject = Subject.objects.get(subject_name = optional_subject),
#             optional_subject = optional_subject,
#             gpa=gpa,
#             previous_school_name=column[28],
#             section = Section.objects.get(semester = sem, section_name = section),
#         )
#         print(student_obj.stu_id,"-------------student obj------------")

#     return HttpResponse("OK")
