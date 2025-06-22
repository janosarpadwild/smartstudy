from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from SmartStudyApp import models

# User serializers

class LoginSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=5) 
    email = serializers.EmailField()
    password = serializers.CharField(max_length=50, write_only=True)      
    def validate_password(self, value):
        validate_password(value)
        return value

class NewPasswordSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=12)
    email = serializers.EmailField()
    
class NewEmailSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=9)
    email = serializers.EmailField()
    new_email = serializers.EmailField()
    new_email_repeat = serializers.EmailField()
    password = serializers.CharField(max_length=50, write_only=True)
    def validate_password(self, value):
        validate_password(value)
        return value

class ChangePasswordSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=15)
    permission_code = serializers.CharField(max_length=24, write_only=True)
    password = serializers.CharField(max_length=50, write_only=True)
    password_repeat = serializers.CharField(max_length=50, write_only=True)    
    def validate_password(self, value):
        validate_password(value)
        return value

class ChangeEmailSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=15)
    permission_code = serializers.CharField(max_length=24, write_only=True)    

class LockAccountSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=15)
    lock_code = serializers.CharField(max_length=24, write_only=True)
    
#-------------------------------------------------------------------------------
# Secretary get serializers

class GenericGetSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=25)

class GetTeacherSubjectsSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=25)
    teacher_id = serializers.IntegerField()

class GetCoursesSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=25)
    class_id = serializers.IntegerField()


class GetStudentsByClassSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=25)
    class_id = serializers.IntegerField()

#--------------------------------------------------------------------------------
# Secretary post serializers

class NewTeacherSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=25)    
    email = serializers.EmailField()
    name = serializers.CharField()
    subjects = serializers.ListField()

class EditTeacherSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=25)    
    id = serializers.IntegerField()
    name = serializers.CharField()
    subjects = serializers.ListField()

class NewStudentSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=25)
    email = serializers.EmailField()
    name = serializers.CharField()
    class_id = serializers.IntegerField() 

class EditStudentSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=25)
    id = serializers.IntegerField()
    name = serializers.CharField()

class AddToClassSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=25)
    students = serializers.ListField()
    class_id = serializers.IntegerField() 

class AdmissionDischargeArchiveSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=25)
    user = serializers.CharField(max_length=25)
    user_ids = serializers.ListField()

class NewClassSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=25)
    name = serializers.CharField()
    class_id = serializers.IntegerField()

class TakeTransmitDeleteClassSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=25)
    id = serializers.IntegerField()

class NewCourseSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=25)
    class_id = serializers.IntegerField()
    course_name = serializers.CharField()
    subject_name = serializers.CharField()

class EditCourseSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=25)
    course_id = serializers.IntegerField()
    course_name = serializers.CharField()


class DeleteCourseSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=25)
    course_id = serializers.IntegerField()

class AddTeacherSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=25)
    class_id = serializers.IntegerField()
    course_id = serializers.IntegerField()
    teacher_id = serializers.IntegerField()

class RemoveTeacherSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=25)
    course_id = serializers.IntegerField()
    teacher_id = serializers.IntegerField()

#--------------------------------------------------------------------------------
# Student get serializers

class GetTopicsSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=25)

# get_tutorial
# get_practise_task
# finished_tutorial
# task_answer
class TaskTutorialSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=25)
    course_id = serializers.IntegerField()
    topic_id = serializers.IntegerField()
    subtopic_id = serializers.IntegerField()

# get_subtopics
# get_test_tasks
# get_test_result
class TestTasksSubtopicsSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=25)
    course_id = serializers.IntegerField()
    topic_id = serializers.IntegerField()

#--------------------------------------------------------------------------------
# Student post serializers
class TaskAnswerSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=25)
    course_id = serializers.IntegerField()
    topic_id = serializers.IntegerField()
    subtopic_id = serializers.IntegerField()
    task_id = serializers.IntegerField()
    test = serializers.BooleanField()
    answer = serializers.FloatField()

#

#--------------------------------------------------------------------------------
# Teacher get serializers
class GetClassesSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=25)

class GetSubjectTopicsSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=25)

# Defined in secretary as well
"""class GetCoursesSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=25)
    class_id = serializers.IntegerField()"""

class GetTeacherTopicsSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=25)
    class_id = serializers.IntegerField()
    course_id = serializers.IntegerField()

class GetStudentResultSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=25)
    class_id = serializers.IntegerField()
    course_id = serializers.IntegerField()
    student_id = serializers.IntegerField()

class GetSubtopicsSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=25)
    topic_id = serializers.IntegerField()

class GetTaskSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=25)
    topic_id = serializers.IntegerField()
    subtopic_id = serializers.IntegerField()

#--------------------------------------------------------------------------------
# Teacher set serializers

class SetCoursesSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=25)
    class_id = serializers.IntegerField()
    course_id = serializers.IntegerField()
    course_topic = serializers.ListField()
