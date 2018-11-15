from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, PasswordField, SubmitField, BooleanField,\
    SelectField, TextAreaField, FloatField, DateField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    identity = RadioField('类型', choices=[('0', '教务'), ('1', '教师'), ('2', '学生')],
                          default='2', validators=[DataRequired()])
    remember_me = BooleanField('记住我', default=False)

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('旧密码', validators=[DataRequired()])
    new_password = PasswordField('新密码', validators=[DataRequired(),
                                            EqualTo('new_password2', message='密码需一致')])
    new_password2 = PasswordField('新密码', validators=[DataRequired()])
