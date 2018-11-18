import sys,os
from .settings import BASE_DIR
sys.path.append(os.path.join(BASE_DIR, '..'))
from GroupAuth.models import Group
from UserAuth.models import User

class UserRender(object):
    def __init__(self, name, orgs=None):
        super().__init__()
        self.name = name
        self.orgs = orgs
        if self.orgs is None or len(self.orgs)==0:
            self.orgs = None
    
    @property
    def namefirst(self):
        return self.name[0]

class OrganizationRender(object):
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.name = Group.objects.filter(group_id=id)[0].group_name


class AddSharedDataMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        return self.get_response(request)
    
    def process_template_response(self, request, response):
        if response.context_data is None:
            response.context_data = {}
        if 'user_name' in request.session:
            user_name = request.session['user_name']
            user_id = request.session['user_id']
            user = User.objects.get(user_id=user_id)
            if not user.group is None:
                group_id = user.group.group_id
                group_render = [OrganizationRender(group_id)]
            else:
                group_render = None
            
            response.context_data['user_render'] = UserRender(user_name, group_render)
        return response