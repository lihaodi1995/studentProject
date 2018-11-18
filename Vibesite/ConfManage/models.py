from django.db import models
from django.utils import timezone
# Create your models here.
class ConferenceRegistration(models.Model):
    registration_id = models.AutoField(primary_key = True)
    
    REG_TYPE = (
        ('a', 'Audit'),
        ('p', 'Participate'),
    )
    type = models.CharField(max_length = 1, choices = REG_TYPE, blank = False, default = 'a')

    RES_STATUS = (
        ('g', 'Granted'),
        ('r', 'Rejected'),
        ('p', 'Pending'),
    )
    result = models.CharField(max_length = 1, choices = RES_STATUS, blank = False, default = 'p')

    # 这里我们把注册的信息改成一对多关系
    # real_name = models.CharField(max_length = 32)

    # GENDER = (
    #     ('m', 'Male'),
    #     ('f', 'Female'),
    # )
    # user_gender = models.CharField(max_length = 1, choices = GENDER, blank = True, default = 'm')

    # accomodation = models.BooleanField(default = False)
    user_who_paid = models.IntegerField(null=True, default=-1) # 用来找到注册用户id
    conf_which_id = models.IntegerField(null=True, default=-1) # 用来找到会议id
    payment = models.CharField(max_length = 64, null = True, help_text = "url")    

class Conference(models.Model):
    conf_id = models.AutoField(primary_key = True)
    title = models.CharField(max_length = 64)
    introduction = models.CharField(max_length = 255)
    # contribution_deadline = models.DateTimeField('ddl')
    inform_date = models.DateTimeField('inform', null = True)
    register_date_start = models.DateTimeField('register date start')
    register_date_end = models.DateTimeField('register date end')
    submit_date_start = models.DateTimeField('first submit date start')
    submit_date_end = models.DateTimeField('first submit date end')
    modify_date_start = models.DateTimeField('modify contrib date start')
    modify_date_end = models.DateTimeField('modify contrib date end')
    conference_date = models.DateTimeField('conf')
    arrangement = models.CharField(max_length = 255, null = True)
    fee = models.FloatField(null = True, default = 0)
    logistics = models.CharField(max_length = 255, help_text = 'transportations and accomodations', null = True)
    contact = models.CharField(max_length = 32, null = True)
    template = models.CharField(max_length = 128, null = True)

    group = models.ForeignKey('GroupAuth.Group', on_delete = models.SET_NULL, null = True)

    # 返回会议状态
    def getState(self):
        now = timezone.now()
        if now < self.submit_date_start:
            state = '暂不可投稿'
        elif now <self.submit_date_end:
            state = "初稿投稿中"
        elif now < self.modify_date_start:
            state = "初稿投稿截止"
        elif now < self.modify_date_end:
            state = "修改稿投稿中"
        elif now < self.register_date_start:
            state = "修改稿投稿截止"
        elif now < self.register_date_end:
            state = "注册中"
        elif now < self.conference_date:
            state = "注册截止"
        else:
            state = "已经举办"
        return state

class PushMessages(models.Model):
    conference = models.ForeignKey('Conference', on_delete = models.CASCADE)
    time = models.DateTimeField()
    phase = models.IntegerField(default = 0)

class RegisteredUser(models.Model):
    real_name = models.CharField(max_length = 32)
    GENDER = (
        ('m', 'Male'),
        ('f', 'Female'),
    )
    user_gender = models.CharField(max_length = 1, choices = GENDER, blank = True, default = 'm')
    contact = models.CharField(max_length=64)
    accomodation = models.BooleanField(default = False)
    # 与会议注册保持多对一关系，用户注册会议时填写多个参会人信息
    user_register = models.ForeignKey('ConferenceRegistration', on_delete = models.SET_NULL, null = True)

'''
class Template(models.Model):
    template_id = models.AutoField(primary_key = True)
    template_file = models.CharField(max_length = 128, null = True)
    '''