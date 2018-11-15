from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import TextAreaField, IntegerField, StringField
from wtforms.validators import DataRequired, InputRequired, Length
from flask_uploads import UploadSet

homework_ups = UploadSet('files')


class HomeworkForm(FlaskForm):
    text = TextAreaField('作业')
    homework_up = FileField('作业附件', validators=[
        FileAllowed(homework_ups, '爷爷你上传了什么？')])


class CreateTeamForm(FlaskForm):
    team_name = StringField('团队名称', validators=[DataRequired()])
    status = IntegerField('队伍状态')


class MemberForm(FlaskForm):
    member_id = IntegerField(validators=[InputRequired])


class EditTeam(FlaskForm):
    new_name = StringField('队伍名称', validators=[DataRequired()])
