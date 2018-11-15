from flask_wtf import FlaskForm
from wtforms import TextAreaField, IntegerField, StringField, SubmitField, SelectField
from wtforms.validators import InputRequired, DataRequired, NumberRange
from flask_uploads import UploadSet
from flask_wtf.file import FileField, FileAllowed, FileRequired

upsr = UploadSet('files', extensions=('xls', 'xlsx', 'pdf', 'doc', 'docx', 'txt', 'zip', '7z', 'rar'))
up_corrected = UploadSet('files', extensions=('zip', 'rar'))


class CourseForm(FlaskForm):
    outline = TextAreaField('课程大纲', validators=[InputRequired()])
    outlet_attachment = FileField('大纲附件')
    teamsize_max = IntegerField('课程人数上限', validators=[DataRequired(), NumberRange(min=1, message='至少需要一个人')])
    teamsize_min = IntegerField('课程人数下限', validators=[DataRequired(), NumberRange(min=1, message='至少需要一个人')])
    no_miss = IntegerField('全勤分数', validators=[InputRequired(), NumberRange(min=0, max=100, message='分数在0-100')])
    miss_1 = IntegerField('一次缺勤', validators=[InputRequired(), NumberRange(min=0, max=100, message='分数在0-100')])
    miss_2 = IntegerField('两次缺勤', validators=[InputRequired(), NumberRange(min=0, max=100, message='分数在0-100')])
    miss_3 = IntegerField('三次缺勤', validators=[InputRequired(), NumberRange(min=0, max=100, message='分数在0-100')])
    miss_4 = IntegerField('四次缺勤', validators=[InputRequired(), NumberRange(min=0, max=100, message='分数在0-100')])
    miss_5 = IntegerField('五次及以上缺勤', validators=[InputRequired(), NumberRange(min=0, max=100, message='分数在0-100')])

    def validate(self):
        if not super(CourseForm, self).validate():
            return False
        if not self.teamsize_min.data <= self.teamsize_max.data:
            self.teamsize_min.errors.append('下限人数不多于上限')
            self.teamsize_max.errors.append('上限人数不少于下限')
            return False
        return True


class HomeworkForm(FlaskForm):
    name = StringField('作业名', validators=[DataRequired()])
    base_requirement = TextAreaField('作业要求', validators=[DataRequired()])
    time = StringField('持续时间', validators=[DataRequired()])
    weight = IntegerField('权重', validators=[DataRequired()])
    max_submit_attempts = IntegerField('最大提交次数', validators=[DataRequired()])


class UploadResourceForm(FlaskForm):
    up = FileField(validators=[
        FileAllowed(upsr, u'xls, xlsx, pdf, doc, docx, txt, zip, 7z, rar'),
        FileRequired(u'文件未选择!')])
    submit = SubmitField(u'上传')


class UploadCorrected(FlaskForm):
    up_corrected = FileField(validators=[FileAllowed(up_corrected, u'zip and rar only'),
                                         FileRequired(u'文件未选择!')])
    submit = SubmitField(u'上传')


class AcceptTeam(FlaskForm):
    id = IntegerField(validators=[InputRequired()])
    # button = SubmitField('通过')


class RejectTeam(FlaskForm):
    id = IntegerField(validators=[InputRequired()])
    # button = SubmitField('拒绝')
    reason = TextAreaField('拒绝理由', validators=[InputRequired()])


class MoveForm(FlaskForm):
    student = IntegerField('学生id', validators=[DataRequired()])
    pending_teams = SelectField('可以加入的组',
                                choices=[],
                                coerce=int)


class AttendanceForm(FlaskForm):
    info = StringField("备注")
    time_delta = IntegerField("签到开放时长")


class PlusForm(FlaskForm):
    name = StringField('加分项名', validators=[DataRequired()])
    weight = StringField('加分最大分值', validators=[DataRequired()])
