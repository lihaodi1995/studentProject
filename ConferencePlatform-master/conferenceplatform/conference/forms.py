from django import forms
import pytz

class ConferenceInfoForm(forms.Form):
    title = forms.CharField(max_length=200)
    subject = forms.CharField(max_length=200)
    introduction = forms.CharField()
    soliciting_requirement = forms.CharField()
    register_requirement = forms.CharField()
    template_no = forms.IntegerField()
    # accept_start = forms.DateTimeField()
    accept_due = forms.DateTimeField()
    # modify_due = forms.DateTimeField()
    register_start = forms.DateTimeField()
    register_due = forms.DateTimeField()
    conference_start = forms.DateTimeField()
    conference_due = forms.DateTimeField()
    paper_template = forms.FileField() # 需上传
    activities = forms.CharField() # json对象
    venue = forms.CharField()

class ActivityInfoForm(forms.Form):
    start_time = forms.DateTimeField()
    end_time = forms.DateTimeField()
    place = forms.CharField(max_length=200)
    activity = forms.CharField(max_length=200)