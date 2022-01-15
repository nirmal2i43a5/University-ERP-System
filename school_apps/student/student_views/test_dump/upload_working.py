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
#         batch = column[1]#batch
#         student_id = column[2]
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
#         see_gpa = column[27]
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
#         )
        
#         fname = column[4].split()[0]
#         stu_username = fname.lower() + f'{student_id}'
#         role = Group.objects.get(name = 'Student')
#         # ---
#         customuser_object = CustomUser.objects.create_user(username = stu_username, password='password', user_type=role, full_name=column[4])
#         sem = Semester.objects.get(name = batch)
     
#         customuser_object.student.stu_id = column[2]
#         customuser_object.student.roll_no = roll_no
#         customuser_object.student.gender = gender
#         customuser_object.student.shift = shift
#         customuser_object.student.semester =  Semester.objects.get(name = batch)
#         customuser_object.student.section =  Section.objects.get(semester = sem, section_name = section)
#         customuser_object.student.course = course
#         customuser_object.student.faculty = faculty
#         customuser_object.student.program = program
#         customuser_object.student.status = status
#         customuser_object.student.contact = contact
#         customuser_object.student.permanent_address = permanent_address
#         customuser_object.student.temporary_address = temporary_address
#         customuser_object.student.dob = dob_es
#         customuser_object.student.blood_group = blood_group
#         customuser_object.student.optional_subject = optional_subject
#         customuser_object.student.see_gpa = see_gpa
#         customuser_object.student.previous_school_name = column[28]
#         customuser_object.student.guardian = parent_obj
#         customuser_object.save()
#         customuser_object.groups.add(role)
        
#     return HttpResponse("OK")
