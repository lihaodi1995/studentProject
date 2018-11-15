def get_student_list(request):
    if request.method == 'POST':
        course = request.POST['course']
        course_obj = Course.objects.get(code = course)
        course_id = course_obj.id
        member_list = TeamMember.objects.filter(course = course_id)
        student_list = []
        for member in member_list:
            student = Student.objects.get(id = member.student.id)
            student_dict = {}
	    student_dict['username'] = student.username
            student_dict['name'] = student.name
            student_dict['phone'] = student.phone
            student_dict['email'] = student.email
            student_list.append(student_dict)
        final_response = {}
        final_response['student_list'] = student_list
	
        return JsonResponse(final_response)

def get_homework_list(request):
    if request.method == 'POST':
        course = request.POST['course']
        course_obj = Course.objects.get(code = course)
        course_id = course_obj.id

        homework_list = Homework.objects.filter(course = course_id)
	
        result_list = []
        for hw in homework_list:
            homework = {}
            homework['name'] = hw.name
            homework['start_time'] = hw.start_time
            homework['end_time'] = hw.end_time
            homework['times'] = hw.times
            homework['score'] = hw.score
            result_list.append(homework)
	print result_list
        final_response = {}
        final_response['homework_list'] = result_list
        return JsonResponse(final_response)

def get_team_homework_list(request):
    if request.method == 'POST':
        homework_name = request.POST['homework_name']
        course = request.session['current_course']
	homework = request.session['current_homework']
        team_homework = TeamHomework.objects.filter(Homework = homework)
        thw_list = []
        for thw in team_homework:
            homework = {}
            team_id = thw.team
            team_member = TeamMember.objects.filter(team = team_id)

            for member in team_member:
                if member.role == 'sm':
                    student = Student.objects.get(id = member.student.id)
		    homework['sender'] = student.name
                    break
            homework['time'] = thw.time
            homework['score'] = thw.score
            root = Meta.objects.get(key = 'root')
            homework_path = os.path.dirname(root) + '/' + course.semester + '/' + course.name + '/' + 'homeworks' + '/' + homework.name + '/' + homework['sender']
            homework_file = os.listdir(homework_path)
            homework['url'] = homework_path + '/' + homework_file[0]
            thw_list.append(homework)
	print thw_list
        final_response = {}
        final_response['team_homework_list'] = thw_list
        return JsonResponse(final_response)

def get_information(request):
    if request.method == 'GET':
        json_response = {}

        try:
            meta = Meta.objects.get(key = 'semester_weeks')
            json_response['weeks'] = int(meta.value)
            json_response['teacher_username'] = []
            json_response['teacher_name'] = []
            json_response['student_username'] = []
            json_response['student_name'] = []

            teacher = Teacher.objects.all()
            for teacher_item in teacher:
                json_response['teacher_username'].append(teacher_item.username)
                json_response['teacher_name'].append(teacher_item.name)

            student = Student.objects.all()
            for student_item in student:
                json_response['student_username'].append(student_item.username)
                json_response['student_name'].append(student_item.name)
            json_response['success'] = True

            return JsonResponse(json_response)
        except ObjectDoesNotExist:
            json_response['success'] = False
            json_response['error_msg'] = 'no semester'
            return JsonResponse(json_response)

def set_course_info(request):
    if request.method == 'POST':
        if request.session['identity'] == 'teacher':
            course_name = request.POST['course_name']
            course = None
            semester = Meta.objects.get(key = 'semester_name').value
            try:
                course = Course.objects.get(name = course_name, semester = semester)
            except ObjectDoesNotExist:
                json_response['info'] = 'error'
                return JsonResponse(json_response)

            description = request.POST['description']
            info = request.POST['info']

            course.description = description
            course.info = info
            course.save()

            outline = request.POST.get('outline', None)
            if outline != None:
                root = Meta.objects.get(key = 'root').value
                outline_path = root + '//' + semester + '//' + course_name + '//' + 'outline.html'
                with open(outline,'wb') as f:
                    f.write(outline)
            elif request.FILES.get('file', None) != None:
                root = Meta.objects.get(key = 'root').value
                outline_path = root + '//' + semester + '//' + course_name + '//' + 'outline.html'
                if os.path.exists(outline_path):
                    os.remove(outline_path)
                save_file(request.FILES['file'], outline_path)
                
        else:
            semester = Meta.objects.get(key = 'semester_name').value
            course = Course()
            course.name = request.POST['course_name']
            course.code = request.POST['course_code']
            course.credit = request.POST['course_credit']
            course.semester = semester
            course.start_week = request.POST['start_week']
            course.end_week = request.POST['end_week']
            course.save()

        final_response = {}
        final_response['info'] = 'success'
        return JsonResponse(final_response)

def set_course_by_excel(request):
    if request.method == 'POST':
        fl = request.FILES.get('file')
        baseDir = os.path.dirname(os.path.abspath(__name__))
        filedir = os.path.join(baseDir,'static')
        filename = os.path.join(filedir,fl.name)

        file_des = open(filename,'wb')
        for chrunk in fl.chunks():
            file_des.write(chrunk)
        file_des.close()

        json_response = {}
        bk = xlrd.open_workbook(filename)
        try:
            sh = bk.sheet_by_name('Sheet1')
        except:
            json_response['success'] = False
            json_response['error_msg'] = 'sheet name error'
            return JsonResponse(json_response)
        nrows = sh.nrows

        try:
            name = sh.cell_value(1, 0)
            code = sh.cell_value(1, 1)
            credit = int(sh.cell_value(1, 2))
            semester = Meta.objects.get(key = 'semester_name').value
            start_week = int(sh.cell_value(1, 3))
            end_week = int(sh.cell_value(1, 4))
            info = sh.cell_value(1, 7)
            if len(Course.objects.filter(code = code)) == 0:
                Course.objects.create(name = name, code = code, credit = credit, semester = semester, start_week = start_week, end_week = end_week, info = info)
        except:
            json_response['success'] = False
            json_response['error_msg'] = 'Add course failed, please check your content of excel'
            return JsonResponse(json_response)

        course = Course.objects.get(code = code)
        for i in range(1, nrows - 1):
            teacher_username = sh.cell_value(i, 5)
            try:
                teacher = Teacher.objects.get(username = teacher_username)
                if len(Teach.objects.filter(teacher = teacher, course = course)) == 0:
                    Teach.objects.create(teacher = teacher, course = course)
            except:
                pass
        for i in range(1, nrows - 1):
            student_username = sh.cell_value(i, 6)
            try:
                student = Student.objects.get(username = student_username)
                if len(TeamMember.objects.filter(student = student, course = course)) == 0:
                    TeamMember.objects.create(student = student, course = course)
            except:
                pass
        os.remove(filename)
        json_response['success'] = True
        return JsonResponse(json_response)

def show_course_detail(request):
    if request.method == 'POST':
        semester = Meta.objects.get(key = 'semester_name').value
        course_name = request.POST['course_name']

        course = None
        try:
            course = Course.objects.get(name = course_name, semester = semester)
        except ObjectDoesNotExist:
            HttpResponse('error')

        final_response = {}
        final_response['course_name'] = course.name
        final_response['semester'] = course.semester
        final_response['start_week'] = course.start_week
        final_response['code'] = course.code
        final_response['credit'] = course.credit
        final_response['student_num'] = TeamMember.objects.filter(course = course).count()
        final_response['info'] = course.info
        final_response['description'] = course.description
        
        root = Meta.objects.get(key = 'root')
        outline_path = os.path.dirname(root) + '/' + course.semester + '/' + course.name + '/' + 'outline.html'
        final_response['outline'] = outline_path
        
        return JsonResponse(final_response)

def set_homework(request):
    if request.method == 'POST':
        final_response = {}
        
        course_name = request.POST['course_name']

        course = None
        try:
            course = Course.objects.get(name = course_name, semester = semester)
        except ObjectDoesNotExist:
            HttpResponse('error')
        
        name = request.POST['name']
        start_time = datetime.datetime.strptime(request.POST['start_time'].replace('T', ' '), "%Y-%m-%d %H:%M")
        end_time = datetime.datetime.strptime(request.POST['end_time'].replace('T', ' '), "%Y-%m-%d %H:%M")
        score = request.POST['score']
        times = request.POST['times']
        content = request.POST['content']

        test_homework = None
        semester = Meta.objects.get(key = 'semester_name')
        try:
            test_homework = Homework.objects.get(name = course_name, course = course)
        except ObjectDoesNotExist:
            pass

        if test_homework != None:
            final_response['success'] = False
            return JsonResponse(final_response)
        else:
            Homework.objects.create(name=name, start_time=start_time, end_time=end_time, score=score, times=times, content=content)
            final_response['success'] = True

            attachment = request.FILES.get('file', None)
            if attachment != None:
                root = Meta.objects.get(key = 'root')
                attachment_dir = root + '/' + course.semester + '/' + course.name + '/homeworks' + '/' + name

                if !os.path.exists(attachment_dir):
                    os.mkdir(attachment_dir)
                    
                attachment_path = attachment_dir + '/' + attachment.name
                save_file(attachment, attachment_path)
            return JsonResponse(final_response)

def upload_homework_student(request):
    if request.method == 'POST':
        content = request.POST['content']
        attachment = request.FILES['attachment']
        
        course = request.session['current_course']
        homework = request.session['current_homework']
        username = request.session['user_name']

        student = Student.objects.get(username = username)  # one student ont team

        semester = Meta.objects.get(key = 'semester_name')
        root = Meta.objects.get(key = 'root')
        attachment_path = root + '/' + semester + '/' + course.name + '/' + 'homeworks' + '/' + homework.name + '/' + username + '/' + attachment.name
        if os.path.exists(attachment_path):
           os.remove(attachment_path) 
        save_file(attachment, attachment_path)
        final_response = {}
        final_response['info'] = 'success'
        return JsonResponse(final_response)

def upload_homework_teacher(request):
    if request.method == 'POST':
        attachment = request.FILES['file']

        course = request.session['current_course']
        homework = request.session['current_homework']
        semester = Meta.objects.get(key = 'semester_name')
        root = Meta.objects.get(key = 'root')
        
        attachment_base = root + '/' + semester + '/' + course.name + '/' + 'homeworks' + '/' + homework.name
        username_list = os.listdir(attachment_base)

        for user in username_list:
            temp_path = attachment_base + '/' + user
            test_path = temp_path + '/' + attachment.name
            if os.path.exists(test_path):
                attachment_name = attachment.name.split('.')[0]
                attachment_suffix = attachment.name.split('.')[1]
                attachment_name = attachment_name + '-modify.' + attachment_suffix

                save_file(test_path, attachment)

                final_response = {}
                final_response['info'] = 'success'
                return JsonResponse(final_response)
        

def upload_resource_teacher(request):
    if request.method == 'POST':
        course = request.session['current_course']
        current_dir = request.session['current_dir']

        attachment = request.FILES['file']

        save_file(current_dir, attachment)

        final_response = {}
        final_response['info'] = 'success'

def mark(request):
    if request.method == 'POST':
        score = request.POST['score']
        comment = request.POST['comment']

        course = request.session['current_course']
        homework = request.session['current_homework']
        owner = request.session['current_homework_student']

        tm_obj = TeamMember.objects.get(course = course, homework = homework, student = owner)
        tm_obj.score = score
        tm_obj.comment = comment
        tm_obj.save()

        final_response = {}
        final_response['info'] = 'success'
        return JsonResponse(final_response)

def save_file(temp_file, path):
    f = open(path, 'wb+')
    for chunk in temp_file.chunks():
        f.write(chunk)
    f.close()


def create_directory(request):
    if request.method == 'POST':
        dir_name = request.POST['dir_name']
        new_path = request.session['current_dir'] + '/' + dir_name

        final_response = {}
        if os.path.exists(new_path):
            final_response['create_result'] = 'exists_error'
        else:
            final_response['create_result'] = 'success'
            os.mkdir(dir_name)

        return final_response

def changeDirectory(request):
    if request.method == 'POST':
        direct = request.POST['direct']
        dir_name = request.POST['dir_name']

        file_list = []

        if(direct == 'down'):
            obj_dir = request.session['current_dir'] + '/' + dir_name
            request.session['current_dir'] = obj_dir
        else:
            obj_dir = os.path.dirname(request.session['current_dir'])
            request.session['current_dir'] = obj_dir
        
        filename_list = os.listdir(request.session['current'])
        for filename in filename_list:
            filepath = obj_dir + '/' + filename
            file_obj = {}
            file_obj['path'] = file_path
            if os.path.isdir(file_path):
                file_obj['type'] = 'dir'
            else:
                file_obj['type'] = 'file'
            file_list.append(file_obj)

        final_response = {}
        final_response['file_list'] = file_list
        return JsonResponse(final_response)
