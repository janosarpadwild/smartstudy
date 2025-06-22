from django.contrib import admin
from .models import (CustomToken, School, Class, User, PermissionCode, LockAccount, Subject, Course, Topic, 
                     SubTopic, Task, TeacherSubject, TeacherCourse, CourseTopic, TaskProgress, CompletedSubTopic, 
                     CompletedTopic, TestProgress, TestResult)

admin.site.register(CustomToken)
admin.site.register(School)
admin.site.register(Class)
admin.site.register(User)
admin.site.register(PermissionCode)
admin.site.register(LockAccount)
admin.site.register(Subject)
admin.site.register(Course)
admin.site.register(Topic)
admin.site.register(SubTopic)
admin.site.register(Task)
admin.site.register(TeacherSubject)
admin.site.register(TeacherCourse)
admin.site.register(CourseTopic)
admin.site.register(TaskProgress)
admin.site.register(CompletedSubTopic)
admin.site.register(CompletedTopic)
admin.site.register(TestProgress)
admin.site.register(TestResult)