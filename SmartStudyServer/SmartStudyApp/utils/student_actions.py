import logging
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.core.exceptions import ObjectDoesNotExist
from SmartStudyApp.models import TaskProgress,  Course, CourseTopic, TestResult, SubTopic, Task, CompletedSubTopic, TestProgress, CompletedTopic, Topic

from django.db.models import Q, F, Value, CharField, Case, When
from django.db import transaction
from django.shortcuts import get_object_or_404

from random import randint
import math

from SmartStudyApp.serializers import GetTopicsSerializer, TaskTutorialSerializer, TestTasksSubtopicsSerializer, TaskAnswerSerializer

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

available_student_actions = ['get_topics', 'get_subtopics', 'get_test_result', 'get_tutorial', 'get_test_tasks', 'get_practise_tasks'
                             'finished_tutorial', 'task_answer']

class StudentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        student = request.user
        match request.data['action']:
            case 'finished_tutorial':
                serializer = TaskTutorialSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.finished_tutorial(student, serializer)
            case 'task_answer':
                serializer = TaskAnswerSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    print('invalid')
                    print(serializer)
                    print(request.data)
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.task_answer(student, serializer)
            case _:
                return Response()

    def get(self, request):
        student = request.user
        match request.data['action']:
            case 'get_topics':
                serializer = GetTopicsSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.get_topics(student, serializer)
            case 'get_subtopics':
                serializer = TestTasksSubtopicsSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.get_subtopics(student, serializer)
            case 'get_test_result':
                serializer = TestTasksSubtopicsSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.get_test_result(student, serializer)
            case 'get_tutorial':
                serializer = TaskTutorialSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.get_tutorial(student, serializer)
            case 'get_test_tasks':
                serializer = TestTasksSubtopicsSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.get_test_tasks(student, serializer)
            case 'get_practise_tasks':
                serializer = TaskTutorialSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.get_practise_tasks(student, serializer)
            case _:
                return Response()
            
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
    def get_topics(self, student, serializer):
        try:
            topic_list = []
            courses = Course.objects.filter(class_id=student.class_id)

            for course in courses:
                course_topic_list = {
                    'id': course.id,
                    f'{course.name}': []
                }
                course_topics = CourseTopic.objects.filter(course_id=course.id, available=True).order_by('topic_id__number')

                for course_topic in course_topics:
                    topic = course_topic.topic_id
                    topic_details = {
                        'id': topic.id,
                        'topic_name': topic.name,
                        'description': topic.description,
                        'test_required_percentage': course_topic.test_required_percentage,
                        'test_task_number': course_topic.test_task_number,
                    }

                    test_result = TestResult.objects.filter(
                        student_id=student.id,
                        course_id=course.id,
                        topic_id=topic.id
                    ).first()

                    if test_result:
                        topic_details["best_correct_answers"] = test_result.best_correct_answers
                    else:
                        topic_details["best_correct_answers"] = 0

                    course_topic_list[f'{course.name}'].append(topic_details)

                topic_list.append(course_topic_list)

        except Exception as e:
            logger.error(f"Error in get_topics: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        result = {'topics': topic_list}
        return Response(data=result, status=status.HTTP_200_OK, content_type="application/json")

    def get_subtopics(self, student, serializer):
        try:
            course_id = serializer.validated_data['course_id']
            topic_id = serializer.validated_data['topic_id']
        except KeyError:
            logger.error(f"Required data is missing from the serializer.{self.get_view_name()}, {self.get_subtopics.__name__}")
            raise DRFValidationError("Required data is missing from the serializer.")
        
        try:
            CourseTopic.objects.get(
                course_id=course_id,
                available=True,
                course_id__class_id=student.class_id,
                topic_id=topic_id
            )
        except CourseTopic.DoesNotExist:
            return Response({"error": "This topic is not available to the student"}, status=status.HTTP_400_BAD_REQUEST)
        
        subtopics = []
        topic_subtopics = SubTopic.objects.filter(topic_id=topic_id).order_by('number')
        
        for subtopic in topic_subtopics:
            try:
                completed_subtopic = CompletedSubTopic.objects.filter(
                    student_id=student.id,
                    course_id=course_id,
                    subtopic_id=subtopic.id
                ).first()
                subtopic_details = {
                    "id": subtopic.id,
                    "subtopic_name": subtopic.name,
                    "completed_tutorial": completed_subtopic.completed_tutorial,
                    "completed_subtopic": completed_subtopic.completed_subtopic
                }
            except CompletedSubTopic.DoesNotExist:
                subtopic_details = {
                    "id": subtopic.id,
                    "subtopic_name": subtopic.name,
                    "completed_tutorial": False,
                    "completed_subtopic": False
                }
            subtopics.append(subtopic_details)
        
        result = {"subtopics": subtopics}
        return Response(data=result, status=status.HTTP_200_OK, content_type="application/json")

        
    def get_test_result(self, student, serializer):
        try:
            course_id = serializer.validated_data['course_id']
            topic_id = serializer.validated_data['topic_id']
        except KeyError:
            logger.error(f"Required data is missing from the serializer.{self.get_view_name()}, {self.get_test_result.__name__}")
            raise DRFValidationError("Required data is missing from the serializer.")     
        try:
            course_topic = CourseTopic.objects.get(
                course_id=course_id,
                available=True,
                course_id__class_id=student.class_id,
                topic_id=topic_id
            )
        except CourseTopic.DoesNotExist:
            return Response({"error": "This topic is not available to the student"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            test_result = TestResult.objects.get(
                student_id=student,
                course_id=course_id,
                topic_id=topic_id
            )
        except TestResult.DoesNotExist:
            return Response({"error": "There is no completed test"}, status=status.HTTP_400_BAD_REQUEST)

        result = {
            "test_result": {
                'correct_answers': test_result.last_correct_answers,
                'test_task_number': course_topic.test_task_number,
                'test_required_percentage': course_topic.test_required_percentage
            }
        }     
        return Response(data=result, status=status.HTTP_200_OK, content_type=json)
    
    def get_tutorial(self, student, serializer):
        try:
            course_id = serializer.validated_data['course_id']
            topic_id = serializer.validated_data['topic_id']
            subtopic_id = serializer.validated_data['subtopic_id']
        except KeyError:
            logger.error(f"Required data is missing from the serializer.{self.get_view_name()}, {self.get_tutorial.__name__}")
            raise DRFValidationError("Required data is missing from the serializer.")
        try:
            CourseTopic.objects.get(
                course_id=course_id,
                available=True,
                course_id__class_id=student.class_id,
                topic_id=topic_id
            )
        except CourseTopic.DoesNotExist:
            return Response({"error": "This topic is not available to the student"}, status=status.HTTP_400_BAD_REQUEST)

        subtopic = get_object_or_404(
            SubTopic,
            id=subtopic_id,
            topic_id=topic_id
        )
        result = {
        'tutorial': {
            "parameters": subtopic.parameters,
            "description": subtopic.tutorial_description
            }
        }
        if subtopic.number == 1:
            return Response(data=result, status=status.HTTP_200_OK, content_type=json)
        try:
            CompletedSubTopic.objects.get(
                student_id=student,
                course_id=course_id,
                subtopic_id__topic_id=topic_id,
                number=subtopic.number - 1,
                completed_tutorial=True,
                completed_subtopic=True
            )
        except CompletedSubTopic.DoesNotExist:
            return Response({"error": "This tutorial is not available to the student"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data=result, status=status.HTTP_200_OK, content_type=json)
    
    def get_test_tasks(self, student, serializer):
        try:
            course_id = serializer.validated_data['course_id']
            topic_id = serializer.validated_data['topic_id']
        except KeyError:
            logger.error(f"Required data is missing from the serializer.{self.get_view_name()}, {self.get_test_tasks.__name__}")
            raise DRFValidationError("Required data is missing from the serializer.")
        try:
            course_topic = CourseTopic.objects.get(
                course_id=course_id,
                available=True,
                course_id__class_id=student.class_id,
                topic_id=topic_id
            )
        except CourseTopic.DoesNotExist:
            return Response({"error": "The student has no access to this coursetopic."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            CompletedTopic.objects.get(
                student_id=student,
                course_id=course_id,
                topic_id=topic_id,
                completed_topic=True
            )
        except CompletedTopic.DoesNotExist:
            return Response({"error": "The student has not completed the topic yet."}, status=status.HTTP_400_BAD_REQUEST)

        incomplete_tasks = TestProgress.objects.filter(
            student_id=student,
            course_id=course_id,
            task_id__subtopic_id__topic_id=topic_id,
            completed=False
        )

        num_tasks_to_select = max(course_topic.test_task_number - incomplete_tasks.count(), 0)
        random_tasks = Task.objects.filter(subtopic_id__topic_id=topic_id).exclude(id__in=incomplete_tasks.values_list('task_id', flat=True)).order_by('?')[:num_tasks_to_select]
        with transaction.atomic():
            try:
                TestProgress.objects.filter(
                    student_id=student,
                    course_id=course_id,
                    task_id__subtopic_id__topic_id=topic_id
                ).exclude(
                    id__in=incomplete_tasks.values_list('id', flat=True)
                ).delete()
                for task in random_tasks:
                    course = Course.objects.get(id=course_id)
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
                        #answer = f'{int(answer)} {task.unit}' if int(answer)==answer else f'{answer} {task.unit}'
                    else:
                        for variable in parameters['variables']:
                            length = str(self.random_numbers_with_scale(parameters['variables'][variable]['min'], parameters['variables'][variable]['max']))
                            answer = answer.replace('{'+variable+'}', length)
                            question = question.replace('{'+variable+'}', f'{length} ')
                        answer = round(eval(answer), 3)

                    TestProgress.objects.create(
                        student_id=student,
                        course_id=course,
                        task_id=task,
                        parameters=parameters,
                        question=question,
                        answer=answer,
                        unit=task.unit
                    )
            except Exception as e:
                raise e
            
        incomplete_tasks = TestProgress.objects.filter(
            student_id=student,
            course_id=course_id,
            task_id__subtopic_id__topic_id=topic_id,
            completed=False
        )
        result = {'tasks':list(incomplete_tasks.annotate(task_progress_id=F('task_id')).values(
            'task_progress_id',
            'parameters',
            'question',
            'unit'
        ))}
        return Response(data=result, status=status.HTTP_200_OK, content_type=json)

    
    def get_practise_tasks(self, student, serializer):
        try:
            course_id = serializer.validated_data['course_id']
            topic_id = serializer.validated_data['topic_id']
            subtopic_id = serializer.validated_data['subtopic_id']
        except KeyError:
            logger.error(f"Required data is missing from the serializer.{self.get_view_name()}, {self.get_practise_tasks.__name__}")
            raise DRFValidationError("Required data is missing from the serializer.")

        try:
            CourseTopic.objects.get(
                course_id=course_id,
                available=True,
                course_id__class_id=student.class_id,
                topic_id=topic_id
            )
        except CourseTopic.DoesNotExist:
            return Response({"error": "This topic is not available to the student"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            CompletedSubTopic.objects.get(
                student_id=student.id,
                course_id=course_id,
                subtopic_id=subtopic_id,
                completed_tutorial=True
            )
        except CompletedSubTopic.DoesNotExist:
            return Response({"error": "The student has not completed the tutorial yet."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            CompletedSubTopic.objects.get(
                student_id=student.id,
                course_id=course_id,
                subtopic_id=subtopic_id,
                completed_subtopic=True
            )
        except CompletedSubTopic.DoesNotExist:
            tasks = TaskProgress.objects.filter(
                student_id=student,
                course_id=course_id,
                task_id__subtopic_id=subtopic_id,
                completed=False
            ).order_by('task_id__number').annotate(task_progress_id=F('task_id')).values(
                'task_progress_id',
                'parameters',
                'question',
                'unit'
            )
            result = {'tasks': list(tasks)}
            return Response(data=result, status=status.HTTP_200_OK, content_type="application/json")
        else:
            try:
                with transaction.atomic():
                    TaskProgress.objects.filter(
                        student_id=student.id,
                        course_id=course_id,
                        task_id__subtopic_id=subtopic_id,
                    ).delete()
                tasks = Task.objects.filter(subtopic_id=subtopic_id).order_by('number')
                print(tasks)
            except Exception as e:
                raise e
            try:
                course = Course.objects.get(id=course_id)
                for task in tasks:
                    parameters = task.parameters
                    answer = task.answer
                    question = task.question
                    if parameters['objects'] != []:
                        for variable in parameters['variables']:
                            for i in range(len(parameters['objects'])):
                                if parameters['objects'][i][0].startswith(variable + '_line'):
                                    length = str(self.random_numbers_with_scale(parameters['variables'][variable]['min'], parameters['variables'][variable]['max']))
                                    if length.endswith('.0'):
                                        length = length[:-2]
                                    parameters['objects'][i][1].update({'length': length})
                                    parameters['variables'].update({variable: length})
                                    parameters['texts'][parameters['objects'][i][0]] = length + ' ' + parameters['texts'][parameters['objects'][i][0]]

                                if parameters['objects'][i][0].startswith(variable + '_rect'):
                                    length = str(self.random_numbers_with_scale(parameters['variables'][variable]['min'], parameters['variables'][variable]['max']))
                                    if length.endswith('.0'):
                                        length = length[:-2]
                                    if parameters['objects'][i][0][0] == 'l':
                                        parameters['objects'][i][1].update({'width': length})
                                    parameters['variables'].update({variable: length})
                                    parameters['texts'][parameters['objects'][i][0]] = length + ' ' + parameters['texts'][parameters['objects'][i][0]]

                                if parameters['objects'][i][0].startswith(variable + '_ellipse'):
                                    length = str(self.random_numbers_with_scale(parameters['variables'][variable]['min'], parameters['variables'][variable]['max']))
                                    if length.endswith('.0'):
                                        length = length[:-2]
                                    parameters['objects'][i][1].update({'width': length})
                                    parameters['objects'][i][1].update({'height': length})
                                    parameters['variables'].update({variable: length})
                                    parameters['texts'][parameters['objects'][i][0]] = length + ' ' + parameters['texts'][parameters['objects'][i][0]]
                            variable_value = str(int(float(parameters['variables'][variable]))) if float(parameters['variables'][variable]) == int(float(parameters['variables'][variable])) else str(parameters['variables'][variable])
                            answer = answer.replace('{' + variable + '}', variable_value)
                            question = question.replace('{' + variable + '}', f'{variable_value} ')
                        answer = round(eval(answer), 3)
                    else:
                        logger.info(answer)
                        for variable in parameters['variables']:
                            logger.info(variable)
                            length = self.random_numbers_with_scale(parameters['variables'][variable]['min'], parameters['variables'][variable]['max'])
                            length = str(int(length)) if length==int(length) else str(length)
                            answer = answer.replace('{'+variable+'}', length)
                            question = question.replace('{'+variable+'}', f'{length} ')
                        logger.info(answer)
                        answer = round(eval(answer), 3)

                    TaskProgress.objects.create(
                        student_id=student,
                        course_id=course,
                        task_id=task,
                        parameters=parameters,
                        question=question,
                        answer=answer,
                        unit=task.unit
                    )                    
            except Exception as e:
                raise e
        tasks = TaskProgress.objects.filter(
            student_id=student,
            course_id=course_id,
            task_id__subtopic_id=subtopic_id,
            completed=False
        ).order_by('task_id__number').annotate(task_progress_id=F('task_id')).values(
            'task_progress_id',
            'parameters',
            'question',
            'unit'
        )
        result = {'tasks': list(tasks)}
        return Response(data=result, status=status.HTTP_200_OK, content_type="application/json")


    def finished_tutorial(self, student, serializer):
        try:
            course_id = serializer.validated_data['course_id']
            topic_id = serializer.validated_data['topic_id']
            subtopic_id = serializer.validated_data['subtopic_id']
        except KeyError:
            logger.error(f"Required data is missing from the serializer.{self.get_view_name()}, {self.finished_tutorial.__name__}")
            raise DRFValidationError("Required data is missing from the serializer.")

        try:
            CourseTopic.objects.get(
                course_id=course_id,
                available=True,
                course_id__class_id=student.class_id,
                topic_id=topic_id
            )
        except CourseTopic.DoesNotExist:
            return Response({"error": "This topic is not available to the student"}, status=status.HTTP_400_BAD_REQUEST)

        subtopic = get_object_or_404(
            SubTopic,
            id=subtopic_id,
            topic_id=topic_id
        )

        completed_subtopic = get_object_or_404(
            CompletedSubTopic,
            student_id=student,
            course_id=course_id,
            subtopic_id=subtopic_id
        )

        if subtopic.number == 1 or CompletedSubTopic.objects.filter(
            student_id=student,
            course_id=course_id,
            subtopic_id__topic_id=topic_id,
            subtopic_id__number=subtopic.number - 1,
            completed_tutorial=True,
            completed_subtopic=True
        ).exists():
            try:
                with transaction.atomic():
                    completed_subtopic.completed_tutorial = True
                    completed_subtopic.save(update_fields=['completed_tutorial'])

                    tasks = Task.objects.filter(subtopic_id=subtopic_id).order_by("number")
                    course = Course.objects.get(id=course_id)
                    
                    for task in tasks:
                        parameters = task.parameters
                        answer = task.answer
                        question = task.question
                        if parameters['objects'] != []:
                            for variable in parameters['variables']:
                                for i in range(len(parameters['objects'])):
                                    if parameters['objects'][i][0].startswith(variable + '_line'):
                                        length = str(self.random_numbers_with_scale(parameters['variables'][variable]['min'], parameters['variables'][variable]['max']))
                                        if length.endswith('.0'):
                                            length = length[:-2]
                                        parameters['objects'][i][1].update({'length': length})
                                        parameters['variables'].update({variable: length})
                                        parameters['texts'][parameters['objects'][i][0]] = length + ' ' + parameters['texts'][parameters['objects'][i][0]]

                                    if parameters['objects'][i][0].startswith(variable + '_rect'):
                                        length = str(self.random_numbers_with_scale(parameters['variables'][variable]['min'], parameters['variables'][variable]['max']))
                                        if length.endswith('.0'):
                                            length = length[:-2]
                                        if parameters['objects'][i][0][0] == 'l':
                                            parameters['objects'][i][1].update({'width': length})
                                        parameters['variables'].update({variable: length})
                                        parameters['texts'][parameters['objects'][i][0]] = length + ' ' + parameters['texts'][parameters['objects'][i][0]]

                                    if parameters['objects'][i][0].startswith(variable + '_ellipse'):
                                        length = str(self.random_numbers_with_scale(parameters['variables'][variable]['min'], parameters['variables'][variable]['max']))
                                        if length.endswith('.0'):
                                            length = length[:-2]
                                        parameters['objects'][i][1].update({'width': length})
                                        parameters['objects'][i][1].update({'height': length})
                                        parameters['variables'].update({variable: length})
                                        parameters['texts'][parameters['objects'][i][0]] = length + ' ' + parameters['texts'][parameters['objects'][i][0]]
                                variable_value = str(int(float(parameters['variables'][variable]))) if float(parameters['variables'][variable]) == int(float(parameters['variables'][variable])) else str(parameters['variables'][variable])
                                answer = answer.replace('{' + variable + '}', variable_value)
                                question = question.replace('{' + variable + '}', f'{variable_value} ')

                            answer = round(eval(answer), 3)
                        else:
                            for variable in parameters['variables']:
                                length = self.random_numbers_with_scale(parameters['variables'][variable]['min'], parameters['variables'][variable]['max'])
                                length = str(int(length)) if length==int(length) else str(length)
                                answer = answer.replace(f'{{{variable}}}', length)
                                question = question.replace('{'+variable+'}', f'{length} ')
                            answer = round(eval(answer), 3)

                        TaskProgress.objects.create(
                            student_id=student,
                            course_id=course,
                            task_id=task,
                            parameters=parameters,
                            question=question,
                            answer=answer,
                            unit=task.unit
                        )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(data={}, status=status.HTTP_200_OK)
        return Response({"error": "This tutorial is not available to the student"}, status=status.HTTP_400_BAD_REQUEST)

    def task_answer(self, student, serializer):
        try:
            course_id = serializer.validated_data['course_id']
            topic_id = serializer.validated_data['topic_id']
            subtopic_id = serializer.validated_data['subtopic_id']
            task_id = serializer.validated_data['task_id']
            test = serializer.validated_data['test']
            answer = serializer.validated_data['answer']
        except KeyError:
            logger.error(f"Required data is missing from the serializer.{self.get_view_name()}, {self.task_answer.__name__}")
            raise DRFValidationError("Required data is missing from the serializer.")
        try:
            CourseTopic.objects.get(
                course_id=course_id,
                available=True,
                course_id__class_id=student.class_id,
                topic_id=topic_id
            )
        except CourseTopic.DoesNotExist:
            return Response({"error": "This topic is not available to the student"}, status=status.HTTP_400_BAD_REQUEST)

        if test:
            test_progress = get_object_or_404(
                TestProgress,
                student_id=student,
                course_id=course_id,
                task_id=task_id
            )
            with transaction.atomic():
                # Register right answer
                if test_progress.answer == round(float(answer), 3):
                    test_progress.completed = True
                    test_progress.save(update_fields=['completed'])
                all_progress = TestProgress.objects.filter(
                    student_id=student,
                    course_id=course_id,
                    task_id__subtopic_id__topic_id=topic_id,
                    completed = True
                ).count()
                test_result = get_object_or_404(
                    TestResult,
                    student_id=student,
                    course_id=course_id,
                    topic_id=topic_id,
                )
                test_result.last_correct_answers=all_progress
                test_result.save(update_fields=['last_correct_answers'])
                if all_progress>test_result.best_correct_answers:
                    test_result.best_correct_answers=all_progress
                    test_result.save(update_fields=['best_correct_answers'])
    
        else:    
            task_progress = get_object_or_404(
                TaskProgress,
                student_id=student,
                course_id=course_id,
                task_id=task_id
            )
            # Register right answer
            with transaction.atomic():
                if task_progress.answer == round(float(answer), 3):
                    task_progress.completed = True
                    task_progress.save(update_fields=['completed'])
                    all_progress = TaskProgress.objects.filter(
                        student_id=student,
                        course_id=course_id,
                        task_id__subtopic_id=subtopic_id,
                        completed = True
                    ).count()
                    all_task = Task.objects.filter(
                        subtopic_id=subtopic_id
                    ).count()
                    # Register completed subtopic
                    if all_progress==all_task:
                        """topic = Topic.objects.get(

                        )"""
                        completed_subtopic = get_object_or_404(
                            CompletedSubTopic,
                            student_id=student,
                            course_id=course_id,
                            subtopic_id=subtopic_id
                        )
                        completed_subtopic.completed_subtopic=True
                        completed_subtopic.save(update_fields=['completed_subtopic'])
                        all_progress = CompletedSubTopic.objects.filter(
                            student_id=student,
                            course_id=course_id,
                            subtopic_id__topic_id=topic_id,
                            completed_subtopic=True
                        ).count()
                        all_subtopic = SubTopic.objects.filter(
                            topic_id=topic_id
                        ).count()
                        # Register completed topic
                        if all_progress==all_subtopic:
                            completed_topic = get_object_or_404(
                                CompletedTopic,
                                student_id=student,
                                course_id=course_id,
                                topic_id=topic_id
                            )
                            completed_topic.completed_topic=True
                            completed_topic.save(update_fields=['completed_topic'])
                        return Response({'completed_subtopic':True}, status=status.HTTP_200_OK, content_type=json)
                return Response({'completed_subtopic':False}, status=status.HTTP_200_OK, content_type=json)
        return Response(data={}, status=status.HTTP_200_OK, content_type=json)

        

