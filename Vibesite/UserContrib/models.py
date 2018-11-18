from django.db import models


# Create your models here.
class Contribution(models.Model):
    contribution_id = models.AutoField(primary_key = True)

    RES_STATUS = (
        ('g', 'Granted'),
        ('r', 'Rejected'),
        ('p', 'Pending'),
    )
    result = models.CharField(max_length = 1, choices = RES_STATUS, blank = False, default = 'p')

    comment = models.CharField(max_length=2048, null= True)
    modified_times = models.IntegerField(default = 0)
    last_modified = models.DateTimeField('modified')
    author = models.CharField(max_length = 512)
    title = models.CharField(max_length = 255)
    organization = models.CharField(max_length = 512, null = True)

    abstract = models.CharField(max_length = 1024)
    url = models.CharField(max_length = 64)
    register_status = models.BooleanField(default = False)

    user = models.ForeignKey('UserAuth.User', on_delete = models.CASCADE, null = True)
    conference = models.ForeignKey('ConfManage.Conference', on_delete = models.CASCADE, null = True)
    contib_reg = models.OneToOneField('ConfManage.ConferenceRegistration', on_delete = models.CASCADE, null = True)

    def tolist(self):

        return zip(self.author.split(';'),self.organization.split(';'))