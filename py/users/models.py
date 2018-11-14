from django.db import models


# Create your models here.
class User(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=30)
    role = models.IntegerField()
    password = models.CharField(max_length=100)
    email = models.EmailField()
    gender = models.CharField(max_length=10)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)

    def __unicode__(self):
        return self.id


class Semester(models.Model):
    name = models.CharField(max_length=30)
    start_time = models.DateField()
    end_time = models.DateField()

    def __unicode__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=30)
    outline = models.TextField()
    credit = models.IntegerField()
    semester = models.ForeignKey(Semester)
    weeks = models.TextField()
    time = models.TextField()
    address = models.TextField()
    team_people_upper_limit = models.IntegerField(null=True)
    team_people_lower_limit = models.IntegerField(null=True)
    status = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name


class Teacher(models.Model):
    user = models.ForeignKey(User)
    position = models.CharField(max_length=30)


class CourseTeacher(models.Model):
    course = models.ForeignKey(Course)
    teacher = models.ForeignKey(Teacher)


class Student(models.Model):
    user = models.ForeignKey(User)
    major = models.CharField(max_length=30)
    department = models.CharField(max_length=30)
    class_name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.user.name


class Team(models.Model):
    name = models.CharField(max_length=30)
    people_number = models.IntegerField()
    head = models.ForeignKey(Student)
    status = models.CharField(max_length=20)
    course = models.ForeignKey(Course, null=True)
    submitter = models.ForeignKey(Student, related_name='submitter', null=True)

    def __unicode__(self):
        return self.name

class StudentTeamInfo(models.Model):
    team = models.ForeignKey(Team)
    student = models.ForeignKey(Student)
    course = models.ForeignKey(Course)
    role = models.CharField(max_length=20, null=True)
    score = models.FloatField(null=True)
    weight = models.FloatField(null=True)


class Apply(models.Model):
    apply_people = models.ForeignKey(Student)
    team = models.ForeignKey(Team)
    time = models.CharField(max_length=20)
    refusal = models.TextField()
    apply_status = models.CharField(max_length=30)


class Assignment(models.Model):
    course = models.ForeignKey(Course)
    name = models.CharField(max_length=30)
    detail = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    allow_submit_times = models.IntegerField()
    score = models.FloatField(null=True)
    score_percentage = models.FloatField()
    type = models.CharField(max_length=20, null=True)

    def __unicode__(self):
        return self.name


class File(models.Model):
    type = models.CharField(max_length=20)
    name = models.TextField(null=True)
    address = models.CharField(max_length=100)
    submitter = models.CharField(max_length=20)
    time = models.DateTimeField(auto_now_add=True)
    size = models.IntegerField()


class CourseFile(models.Model):
    course = models.ForeignKey(Course)
    file = models.ForeignKey(File)


class AssignmentFile(models.Model):
    assignment = models.ForeignKey(Assignment)
    file = models.ForeignKey(File)


class AssignmentSubmitRecord(models.Model):
    team = models.ForeignKey(Team)
    assignment = models.ForeignKey(Assignment)
    submit_times = models.IntegerField()
    course = models.ForeignKey(Course)
    submitter = models.ForeignKey(Student)
    text = models.TextField()
    file_set = models.TextField()
    time = models.DateTimeField()
    status = models.CharField(max_length=20, null=True)


class ReviseRecord(models.Model):
    team = models.ForeignKey(Team)
    assignment = models.ForeignKey(Assignment)
    course = models.ForeignKey(Course)
    teacher = models.ForeignKey(Teacher)
    file = models.ForeignKey(File,null = True)
    score = models.FloatField()
    comment = models.TextField()


class SelectCourse(models.Model):
    course = models.ForeignKey(Course)
    student = models.ForeignKey(Student)
    score = models.FloatField(null=True)
    comment = models.TextField(null=True)


class Tag(models.Model):
    course = models.ForeignKey(Course)
    tag = models.CharField(max_length=20)


class TagRecord(models.Model):
    file = models.ForeignKey(File)
    tag = models.ForeignKey(Tag)


class ChatRecord(models.Model):
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    content = models.TextField()
    date = models.DateTimeField()


class OperateRecord(models.Model):
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    content = models.TextField()


class AttendanceRecord(models.Model):
    course = models.ForeignKey(Course)
    student = models.ForeignKey(Student)
    times = models.IntegerField()
    time = models.DateTimeField()

class GradeItem(models.Model):
    course = models.ForeignKey(Course)
    name = models.CharField(max_length=30)
    maxscore = models.FloatField()
    ratio = models.FloatField()
    type = models.CharField(max_length=45,null=True)

class GradeRecord(models.Model):
    gradeitem = models.ForeignKey(GradeItem,null=True)
    team = models.ForeignKey(Team)
    score = models.FloatField()
    course = models.ForeignKey(Course)
