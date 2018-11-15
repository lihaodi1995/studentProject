
import os

from app import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand, upgrade
from app.models.models import Student, Teacher, DeanInfo, \
    Semester, Team, TeamMember, Homework ,Submission, Attachment, Course, CourseTime, SCRelationship, TCRelationship, Plus

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app,
                db=db,
                Student=Student,
                Teacher=Teacher,
                TeamMember=TeamMember,
                Course=Course)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def deploy():
    """部署数据库"""
    upgrade()
    DeanInfo.init_dean()
    Teacher.init_teacher()
    Student.init_student()

if __name__ == '__main__':
    manager.run()
