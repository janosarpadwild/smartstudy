import logging
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.core.exceptions import ObjectDoesNotExist
from SmartStudyApp.models import Class, TeacherCourse, TaskProgress,  Course, CourseTopic, TeacherSubject, TestResult, SubTopic, Task, CompletedSubTopic, TestProgress, CompletedTopic, Topic, User

from django.db.models import Q, F, Value, CharField, Case, When, OuterRef, Subquery
from django.db import transaction
from django.shortcuts import get_object_or_404
from random import randint
import math

from SmartStudyApp.serializers import GetClassesSerializer, GetSubjectTopicsSerializer, GetCoursesSerializer, GetTeacherTopicsSerializer, GetStudentResultSerializer, GetSubtopicsSerializer, GetTaskSerializer, SetCoursesSerializer

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

available_teacher_actions = ['get_classes', 'get_subjects_topics', 'get_courses', 'get_topics', 'get_student_result', 'get_subtopics', 'get_task', 
                             'set_courses']

class TeacherAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        student = request.user
        match request.data['action']:
            case 'set_courses':
                serializer = SetCoursesSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.set_courses(student, serializer)
            case _:
                return Response()

    def get(self, request):
        student = request.user
        match request.data['action']:
            case 'get_classes':
                serializer = GetClassesSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.get_classes(student, serializer)
            case 'get_subjects_topics':
                serializer = GetSubjectTopicsSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.get_subjects_topics(student, serializer)
            case 'get_courses':
                serializer = GetCoursesSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.get_courses(student, serializer)
            case 'get_topics':
                serializer = GetTeacherTopicsSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.get_topics(student, serializer)
            case 'get_student_result':
                serializer = GetStudentResultSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.get_student_result(student, serializer)
            case 'get_subtopics':
                serializer = GetSubtopicsSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.get_subtopics(student, serializer)
            case 'get_task':
                serializer = GetTaskSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.get_task(student, serializer)
            case _:
                pass

    def random_numbers_with_scale(self, start, end):
        if isinstance(start, int) and isinstance(end, int):
            scale_factor = 1
        else:
            # Check if the end value is a float
            if isinstance(end, float):
                scale_factor = 10 ** len(str(end).split('.')[1])
            else:
                scale_factor = 10 ** len(str(start).split('.')[1])
        
        start_int = int(start * scale_factor)
        end_int = int(end * scale_factor)
        
        # Generate a random integer within the range
        rand_int = randint(start_int, end_int)
        
        # Scale the random integer appropriately
        scaled_number = rand_int / scale_factor
        return scaled_number

    #----------------------------------------------------------------------------------------------
    #GET

    def get_classes(self, teacher, serializer):
        #teacher_courses = TeacherCourse.objects.filter(teacher_id=teacher)
        teacher_classes = Class.objects.filter(
            course__teachercourse__teacher_id=teacher.id,
            course__teachercourse__course_id__class_id__school_id=teacher.school_id,
            course__teachercourse__course_id__class_id__secretary_id=teacher.secretary_id
        ).distinct().annotate(
            class_name=F('name')
        ).values('id', 'class_name')
        result = {'classes': list(teacher_classes)}
        return Response(data=result, status=status.HTTP_200_OK)


    def get_subjects_topics(self, teacher, serializer):
        subject_names = TeacherSubject.objects.filter(teacher_id=teacher).values_list('subject_name', flat=True)
        topics_by_subject = []

        for subject_name in subject_names:
            topics = Topic.objects.filter(
                subject_name=subject_name
            ).annotate(
                topic_name=F('name')
            ).values('id', 'topic_name', 'description')
            topic_list={subject_name:list(topics)}
            topics_by_subject.append(topic_list)

        result = {'subjects_topics':topics_by_subject}
        return Response(data=result, status=status.HTTP_200_OK, content_type=json)  

    def get_courses(self, teacher, serializer):
        try:
            class_id = serializer.validated_data['class_id']
        except KeyError:
            logger.error(f"Required data is missing from the serializer.{self.get_view_name()}, {self.get_courses.__name__}")
            raise DRFValidationError("Required data is missing from the serializer.")

        #teacher_courses = TeacherCourse.objects.filter(teacher_id=teacher)
        #courses = Course.objects.filter(class_id=class_id, id__in=teacher_courses)

        teacher_courses = TeacherCourse.objects.filter(teacher_id=teacher).values_list('course_id', flat=True)
        courses = Course.objects.filter(class_id=class_id, id__in=teacher_courses)

        course_list = []        
        for course in courses:
            print(course)
            # Retrieve all courses associated with the current class
            course_topics = CourseTopic.objects.filter(
                course_id=course,
                available=True
            ).order_by(
                'topic_id__number'
            ).values(
                'topic_id', 
                'topic_id__name', 
                'test_task_number', 
                'test_required_percentage'
            )
            topics_with_students = []
            for topic in course_topics:
                # Retrieve all students associated with the current class and course
                students = User.objects.filter(
                    class_id=class_id,
                    school_id=teacher.school_id,
                    secretary_id=teacher.secretary_id
                ).order_by('name')

                students_list = []
                for student in students:
                    # Retrieve the best_correct_answers for the current student, course, and topic
                    test_result = get_object_or_404(
                        TestResult,
                        student_id=student.id,
                        course_id=course.id,
                        topic_id=topic['topic_id'])
                    best_correct_answers = test_result.best_correct_answers

                    # Append student information to the list
                    students_list.append({
                        'id': student.id,
                        'student_name': student.name,
                        'student_email': student.email,
                        'best_correct_answers': best_correct_answers
                    })

                # Append CourseTopic information along with students to the list
                topics_with_students.append({
                    'id': topic['topic_id'],
                    'topic_name': topic['topic_id__name'],
                    'test_task_number': topic['test_task_number'],
                    'test_required_percentage': topic['test_required_percentage'],
                    'students': students_list
                })

            # Append course information along with CourseTopics and students to the result
            course_list.append({
                'id': course.id,
                course.name: topics_with_students
            })
        result={'courses':course_list}
        return Response(data=result, status=status.HTTP_200_OK, content_type=json)  

    def get_topics(self, teacher, serializer):
        try:
            class_id = serializer.validated_data['class_id']
            course_id = serializer.validated_data['course_id']
        except KeyError:
            logger.error(f"Required data is missing from the serializer.{self.get_view_name()}, {self.get_topics.__name__}")
            raise DRFValidationError("Required data is missing from the serializer.")
        
        teacher_subjects = TeacherSubject.objects.filter(teacher_id=teacher.id).values_list('subject_name', flat=True)

        course_topics = CourseTopic.objects.filter(
            course_id=course_id,
            course_id__class_id=class_id,
            course_id__subject_name__in=teacher_subjects
        ).annotate(
            topic_name=F('topic_id__name'),
            description=F('topic_id__description')
        ).order_by(
            'topic_id__number'
        ).values(
            'topic_id',
            'topic_name',
            'description',
            'available',
            'test_task_number', 
            'test_required_percentage'
        )
        result={'course_topic':list(course_topics)}
        return Response(data=result, status=status.HTTP_200_OK, content_type=json)  

    def get_student_result(self, teacher, serializer):
        try:
            class_id = serializer.validated_data['class_id']
            course_id = serializer.validated_data['course_id']
            student_id = serializer.validated_data['student_id']
        except KeyError:
            logger.error(f"Required data is missing from the serializer.{self.get_view_name()}, {self.get_student_result.__name__}")
            raise DRFValidationError("Required data is missing from the serializer.")

        course_topic_subquery = CourseTopic.objects.filter(
            course_id=OuterRef('course_id'),
            topic_id=OuterRef('topic_id'),
            available=True
        ).values(
            'test_required_percentage',
            'test_task_number'
        )

        # Main query using subquery for annotations
        test_result = TestResult.objects.filter(
            student_id=student_id,
            course_id=course_id,
            course_id__class_id=class_id,
            course_id__class_id__secretary_id=teacher.secretary_id,
            course_id__class_id__school_id=teacher.school_id,
            course_id__coursetopic__available=True
        ).annotate(
            topic_name=F('topic_id__name'),
            test_required_percentage=Subquery(course_topic_subquery.values('test_required_percentage')[:1]),
            test_task_number=Subquery(course_topic_subquery.values('test_task_number')[:1])
        ).values(
            'topic_name',
            'test_required_percentage',
            'test_task_number',
            'best_correct_answers'
        ).distinct()
        
        result={'student_results':list(test_result)}
        return Response(result)

    def get_subtopics(self, teacher, serializer):
        try:
            topic_id = serializer.validated_data['topic_id']
        except KeyError:
            logger.error(f"Required data is missing from the serializer.{self.get_view_name()}, {self.get_subtopics.__name__}")
            raise DRFValidationError("Required data is missing from the serializer.")    
        
        subject_names = TeacherSubject.objects.filter(teacher_id=teacher.id).values_list('subject_name', flat=True)
        subtopics = SubTopic.objects.filter(
            topic_id__subject_name__in=subject_names,
            topic_id=topic_id
        ).annotate(subtopic_name=F('name')).values(
            'id',
            'subtopic_name',
        )        
        result = {"subtopics": list(subtopics)}
        return Response(result)

    def get_task(self, teacher, serializer):
        try:
            topic_id = serializer.validated_data['topic_id']
            subtopic_id = serializer.validated_data['subtopic_id']
        except KeyError:
            logger.error(f"Required data is missing from the serializer.{self.get_view_name()}, {self.get_task.__name__}")
            raise DRFValidationError("Required data is missing from the serializer.")    
        subject_names = TeacherSubject.objects.filter(teacher_id=teacher.id).values_list('subject_name', flat=True)
        task = Task.objects.filter(
            subtopic_id__topic_id__subject_name__in=subject_names,
            subtopic_id__topic_id=topic_id,
            subtopic_id=subtopic_id
        ).order_by('?').first()

        if not task:
            logger.error(f"No task found matching the criteria. {self.get_view_name()}, {self.get_task.__name__}")
            raise DRFValidationError("No task found matching the criteria.")

        parameters = task.parameters
        answer = task.answer
        question = task.question
        if parameters['objects']!=[]:
            for variable in parameters['variables']:
                for i in range(len(parameters['objects'])):
                    if parameters['objects'][i][0].startswith(variable+'_line'):
                        length = str(self.random_numbers_with_scale(parameters['variables'][variable]['min'], parameters['variables'][variable]['max']))
                        if length.endswith('.0'):
                            length = length[:-2]
                        parameters['objects'][i][1].update({'length':length})
                        parameters['variables'].update({variable:length})
                        parameters['texts'][parameters['objects'][i][0]]=length+' '+parameters['texts'][parameters['objects'][i][0]]

                    if parameters['objects'][i][0].startswith(variable+'_rect'):
                        length = str(self.random_numbers_with_scale(parameters['variables'][variable]['min'], parameters['variables'][variable]['max']))
                        if length.endswith('.0'):
                            length = length[:-2]
                        if parameters['objects'][i][0][0]=='l':
                            parameters['objects'][i][1].update({'width':length})
                        parameters['variables'].update({variable:length})
                        parameters['texts'][parameters['objects'][i][0]]=length+' '+parameters['texts'][parameters['objects'][i][0]]

                    if parameters['objects'][i][0].startswith(variable+'_ellipse'):                    
                        length = str(self.random_numbers_with_scale(parameters['variables'][variable]['min'], parameters['variables'][variable]['max']))
                        if length.endswith('.0'):
                            length = length[:-2]
                        parameters['objects'][i][1].update({'width':length})
                        parameters['objects'][i][1].update({'height':length})
                        parameters['variables'].update({variable:length})
                        parameters['texts'][parameters['objects'][i][0]]=length+' '+parameters['texts'][parameters['objects'][i][0]]
                variable_value = str(int(float(parameters['variables'][variable]))) if float(parameters['variables'][variable])==int(float(parameters['variables'][variable])) else str(parameters['variables'][variable])
                answer = answer.replace('{'+variable+'}', variable_value)
                question = question.replace('{'+variable+'}', f'{variable_value} ')

            answer = round(eval(answer), 3)        
            answer = f'{int(answer)} {task.unit}' if int(answer)==answer else f'{answer} {task.unit}'
        else:
            for variable in parameters['variables']:
                length = self.random_numbers_with_scale(parameters['variables'][variable]['min'], parameters['variables'][variable]['max'])
                length = str(int(length)) if length==int(length) else str(length)
                answer = answer.replace('{'+variable+'}', length)
                question = question.replace('{'+variable+'}', f'{length} ')
            answer = answer + '=' + str(round(eval(answer), 3))

        task = {}
        task.update({'question':question})
        task.update({'answer':answer})
        task.update({'parameters':parameters})
        result = {"task": task}

        return Response(result)

    #----------------------------------------------------------------------------------------------
    #SET

    def set_courses(self, teacher, serializer):
        try:
            class_id = serializer.validated_data['class_id']
            course_id = serializer.validated_data['course_id']
            course_topic = serializer.validated_data['course_topic']
        except KeyError:
            logger.error(f"Required data is missing from the serializer. {self.get_view_name()}, {self.set_courses.__name__}")
            raise DRFValidationError("Required data is missing from the serializer.") 

        try:
            teacher_course = TeacherCourse.objects.get(
                course_id=course_id,
                course_id__class_id=class_id,
                teacher_id=teacher
            )
        except TeacherCourse.DoesNotExist:
            return Response({"error": "The teacher has no access to this course."}, status=status.HTTP_400_BAD_REQUEST)
                    
        teacher_subject_names = TeacherSubject.objects.filter(teacher_id=teacher).values_list('subject_name', flat=True)
        teacher_subject_names_list = [subject_name for subject_name in teacher_subject_names]  # Convert to list for better debugging
        try:
            for coursetopic in course_topic:
                try:
                    topic_id = coursetopic['topic_id']
                    topic_subject_name = Topic.objects.get(id=topic_id).subject_name
                    if topic_subject_name.name != teacher_course.course_id.subject_name.name:
                        return Response({"error": "The topic does not belong to this subject."}, status=status.HTTP_400_BAD_REQUEST)
                except KeyError:
                    return Response({"error": "Missing topic ID in course topic data."}, status=status.HTTP_400_BAD_REQUEST)
                except Topic.DoesNotExist:
                    return Response({"error": "This topic does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            if teacher_course.course_id.subject_name.name not in teacher_subject_names_list:
                return Response({"error": "The teacher does not teach this subject."}, status=status.HTTP_400_BAD_REQUEST)

        except KeyError:
            return Response({"error": "Invalid course topic data format."}, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            try:
                for coursetopic in course_topic:
                    try:
                        topic_id = coursetopic['topic_id']
                        old_course_topic = CourseTopic.objects.get(
                            course_id=course_id,
                            topic_id=topic_id
                        )
                        old_course_topic.available = coursetopic['available']
                        old_course_topic.test_task_number = coursetopic['test_task_number']
                        old_course_topic.test_required_percentage = coursetopic['test_required_percentage']
                        old_course_topic.save(update_fields=['available', 'test_task_number', 'test_required_percentage'])

                        if coursetopic['available']:
                            students = User.objects.filter(
                                secretary_id=teacher.secretary_id,
                                school_id=teacher.school_id,
                                archived=False,
                                is_active=True,
                                class_id=class_id
                            )
                            for student in students:
                                subtopics = SubTopic.objects.filter(topic_id=topic_id)
                                for subtopic in subtopics:
                                    subtopic_instance = SubTopic.objects.get(id=subtopic.id)
                                    course_instance = Course.objects.get(id=course_id)
                                    student_instance = User.objects.get(id=student.id)

                                    completed_subtopic, _ = CompletedSubTopic.objects.get_or_create(
                                        student_id=student_instance,
                                        course_id=course_instance,
                                        subtopic_id=subtopic_instance,
                                        number=subtopic.number
                                    )

                                topic_instance = Topic.objects.get(id=topic_id)
                                CompletedTopic.objects.get_or_create(
                                    student_id=student_instance,
                                    course_id=course_instance,
                                    topic_id=topic_instance
                                )
                                TestResult.objects.get_or_create(
                                    student_id=student_instance,
                                    course_id=course_instance,
                                    topic_id=topic_instance
                                )                              
                    except KeyError:
                        return Response({"error": "Missing required fields in course topic data."}, status=status.HTTP_400_BAD_REQUEST)
                    except CourseTopic.DoesNotExist:
                        return Response({"error": "This course topic does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                logger.error(f"An error occurred while updating course topics: {e}")
                raise e

        return Response(data={}, status=status.HTTP_200_OK, content_type="application/json")
