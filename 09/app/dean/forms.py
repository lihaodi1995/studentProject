from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import IntegerField, TextAreaField, StringField, SelectField
from wtforms.validators import DataRequired, InputRequired, Length
from flask_uploads import UploadSet

ups = UploadSet('files', extensions=('xls', 'xlsx'))


class AddSemesterForm(FlaskForm):
    id = IntegerField('学期', validators=[DataRequired()])
    base_info = TextAreaField('学期基本信息')
    time = StringField('学期时间', validators=[DataRequired()])


class CourseForm(FlaskForm):
    semester = SelectField('学期', choices=[], validators=[InputRequired()], coerce=int)
    name = StringField('课程名称', validators=[InputRequired()])
    course_info = TextAreaField('课程基本信息', validators=[])
    place = StringField('地点', validators=[Length(0, 50)])
    credit = IntegerField('学分', validators=[DataRequired()])
    stuff_info = FileField('学生老师信息', validators=[
            FileAllowed(ups, '只接受xls(或xlsx)文件!'),
            FileRequired('文件未选择!')])
