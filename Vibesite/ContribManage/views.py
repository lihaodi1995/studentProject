# Create your views here.
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import threading
from UserContrib.models import Contribution
from UserAuth.models import User
from utils import sendmail
from django.http import HttpResponse
@csrf_exempt
@require_http_methods(["POST"])
def result(request,contribution_id):
    try:
        result = request.POST.get('re')
        comment = request.POST.get('comment')
        request.session['meeting_label'] = 'contribution'
        contribution = Contribution.objects.get(contribution_id=contribution_id)
        contribution.result = result
        if result != 'r':
            comment = None
        contribution.comment = comment
        contribution.save()
        user = User.objects.get(user_id = contribution.user_id)
        if result == 'r':
            content = '%s的%s稿件投递结果为不通过,评审意见%s'%(user.user_name,contribution.title,contribution.comment)
        elif result == 'g':
            content = '%s的%s稿件投递结果为通过'%(user.user_name,contribution.title)
        if result != 'p':
            thread_new = myThread(1,user.email,'NVolatile通知邮件', content) 
            thread_new.start()
        res = HttpResponse("修改成功")
    except Exception as e:
        res= HttpResponse("修改失败")
    return res
    
class myThread(threading.Thread):
    def __init__(self,threadID,email,message,html):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.email = email
        self.message = message
        self.html = html
    def run(self):
        sendmail.sendmail([self.email], self.message, self.html)