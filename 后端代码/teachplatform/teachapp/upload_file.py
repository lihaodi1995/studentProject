from django shortcuts import JsonResponse
import os

from teachapp.models import Meta

def saveFile(file, path):
    f = open(path, 'wb+')
    for chunk in file.chunks():
        f.write(chunk)
    f.close()

def uploadResource(request):
    if request.method == 'POST':
        resource_file = request.FILES['']

        saveFile(resource_file, request.session['current_directory'])

        final_response = {}
        final_response['file_path'] = request.session['current_directory']
        return final_response


def createDirectory(request):
    if request.method == 'POST':
        dir_name = request.POST['dir_name']
        new_path = request.session['current_dir'] + '/' + dir_name

        final_response = {}
        if(os.path.exists(new_path)):
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

def uploadHomework(request):
    if request.method == 'POST':
        homework_file = request.FILES['']

        semester = Meta.objects.get(key = 'semester')
        course = ''
        homework = ''
        team = ''
        path = semester + '/' + course + '/' + 'homeworks/' + homework + '/' + team + '/' + homework_file.name

        saveFile(homework_file, path)

        final_response = {}
        final_response['file_path'] = path
        return JsonResponse(final_response)