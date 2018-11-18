from django.db import models

# Create your models here.
class Group(models.Model):
    group_id = models.AutoField(primary_key = True)
    group_name = models.CharField(max_length = 32)
    admin = models.IntegerField(default = 0)
    #admin = models.ForeignKey('UserAuth.User', on_delete = models.SET_NULL, null = True)
    group_auth = models.OneToOneField('Authorization', on_delete = models.CASCADE, null = True)

class Authorization(models.Model):
    authorization_id = models.AutoField(primary_key = True)
    # group_name = models.CharField(max_length = 32)
    # corporate_url = models.CharField(max_length = 256, help_text = "a list of urls, stored as json", null = True)
    
    AUTH_STATUS = (
        ('g', 'Granted'),
        ('r', 'Rejected'),
        ('p', 'Pending'),
    )

    status = models.CharField(max_length = 1, choices = AUTH_STATUS, blank = False, default = 'p')
    nature = models.CharField(max_length = 32) # 性质
    service = models.CharField(max_length = 32) # 服务领域
    register_code = models.CharField(max_length = 32) # 登记证号
    organ_code = models.CharField(max_length = 32) # 组织机构代码
    found_date = models.DateTimeField('found') # 成立时间
    legal_person = models.CharField(max_length = 32) # 法人
    legal_person_contact = models.CharField(max_length = 32) # 法人联系方式
    fund = models.IntegerField(default=0) # 注册资金
    fund_source = models.CharField(max_length = 32) # 经费来源
    active_area = models.CharField(max_length = 32) # 活动地域
    location = models.CharField(max_length = 32) # 组织地址
    zipcode = models.CharField(max_length = 32) # 地址邮编
    tele = models.CharField(max_length = 32) # 电话
    cert_url = models.CharField(max_length = 64) # 证书URL
    validate_start = models.DateTimeField('validate start') # 证书起始日期
    Validate_end = models.DateTimeField('validate end') # 证书结束日期