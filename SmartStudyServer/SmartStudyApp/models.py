from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework.authtoken.models import Token
from django.conf import settings

class CustomToken(Token):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='auth_tokens', on_delete=models.CASCADE)
    used = models.BooleanField(default=False)
    last_activity = models.DateTimeField(auto_now=True)

class School(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField()

class Class(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField()
    school_id = models.ForeignKey(School, on_delete=models.CASCADE)
    secretary_id = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField()
    password = models.CharField()    
    archived = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    school_id = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True)
    secretary_id = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    class_id = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)

    ROLE_CHOICES = [
        ('SECRETARY', 'Secretary'),
        ('TEACHER', 'User'),
        ('STUDENT', 'User'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

class PermissionCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField()
    new_email = models.EmailField(null=True, blank=True)
    permission_code = models.CharField()
    expiration_time = models.DateTimeField()

class LockAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lock_code = models.CharField()
    expiration_time = models.DateTimeField()

class Subject(models.Model):
    name = models.CharField(primary_key=True)

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField()
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE)

class Topic(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField()
    number = models.PositiveSmallIntegerField()
    description = models.TextField()
    subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE)

class SubTopic(models.Model):
    id = models.AutoField(primary_key=True)
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField()
    number = models.PositiveSmallIntegerField()
    parameters = models.JSONField()
    tutorial_description = models.JSONField()

class Task(models.Model):
    id = models.AutoField(primary_key=True)
    subtopic_id = models.ForeignKey(SubTopic, on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField()
    parameters = models.JSONField()
    question = models.TextField()
    answer = models.CharField()
    unit = models.CharField()

class TeacherSubject(models.Model):
    subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher_id = models.ForeignKey(User, on_delete=models.CASCADE)
    
class TeacherCourse(models.Model):
    teacher_id = models.ForeignKey(User, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)

class CourseTopic(models.Model):    
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE)
    test_task_number = models.PositiveSmallIntegerField(default=0)
    test_required_percentage = models.PositiveSmallIntegerField(default=0)
    available = models.BooleanField(default=False)

class TaskProgress(models.Model):#student creates during finish tutorial
    student_id = models.ForeignKey(User, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    parameters = models.JSONField()
    question = models.TextField()
    answer = models.FloatField()
    unit = models.CharField()
    completed = models.BooleanField(default=False)

class CompletedSubTopic(models.Model):#teacher creates it during enable
    student_id = models.ForeignKey(User, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    subtopic_id = models.ForeignKey(SubTopic, on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField()
    completed_tutorial = models.BooleanField(default=False)
    completed_subtopic = models.BooleanField(default=False)

class CompletedTopic(models.Model):#teacher creates it during enable
    student_id = models.ForeignKey(User, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE)    
    completed_topic = models.BooleanField(default=False)

class TestProgress(models.Model):#student creates during test start
    student_id = models.ForeignKey(User, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    parameters = models.JSONField()
    question = models.TextField()
    answer = models.FloatField()
    unit = models.CharField()
    completed = models.BooleanField(default=False)

class TestResult(models.Model):#teacher creates it during enable
    student_id = models.ForeignKey(User, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE)    
    last_correct_answers = models.PositiveSmallIntegerField(default=0)
    best_correct_answers = models.PositiveSmallIntegerField(default=0)
