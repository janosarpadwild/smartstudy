import logging
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.core.exceptions import ObjectDoesNotExist
from SmartStudyApp.models import CompletedSubTopic, CompletedTopic, CourseTopic, SubTopic, TaskProgress, TestProgress, TestResult, Topic, User, Class, TeacherSubject, Subject, TeacherCourse, Course

from django.db.models import Q, F, Value, CharField, Case, When
from django.db import transaction
from django.shortcuts import get_object_or_404

#POST Serializers
from SmartStudyApp.serializers import NewTeacherSerializer, EditTeacherSerializer, NewStudentSerializer, EditStudentSerializer, AddToClassSerializer, AdmissionDischargeArchiveSerializer, NewClassSerializer, TakeTransmitDeleteClassSerializer, NewCourseSerializer, EditCourseSerializer, DeleteCourseSerializer, AddTeacherSerializer, RemoveTeacherSerializer

#GET Serializers
from SmartStudyApp.serializers import GenericGetSerializer, GetTeacherSubjectsSerializer, GetCoursesSerializer, GetStudentsByClassSerializer

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

available_secretary_actions = ['get_classes', 'get_teachers', 'get_students', 'get_teacher_subjects', 'get_subjects', 'get_courses', 'get_teachers_subjects', 'get_students_by_class',
                               'new_teacher', 'edit_teacher', 'new_student', 'edit_student', 'add_to_class', 'admission', 'discharge', 'archive', 'take_class', 'new_class', 'transmit_class', 'delete_class', 'new_course', 'save_course', 'delete_course', 'add_teacher']

class SecretaryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        secretary = request.user
        match request.data['action']:
            case 'new_teacher':
                serializer = NewTeacherSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.new_teacher(secretary, serializer)
            case 'edit_teacher':
                serializer = EditTeacherSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.edit_teacher(secretary, serializer)
            case 'new_student':
                serializer = NewStudentSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.new_student(secretary, serializer)
            case 'edit_student':
                serializer = EditStudentSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.edit_student(secretary, serializer)
            case 'add_to_class':
                serializer = AddToClassSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.add_to_class(secretary, serializer)
            case 'admission':
                serializer = AdmissionDischargeArchiveSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.admission(secretary, serializer)
            case 'discharge':
                serializer = AdmissionDischargeArchiveSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.discharge(secretary, serializer)
            case 'archive':
                serializer = AdmissionDischargeArchiveSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.archive(secretary, serializer)
            case 'take_class':
                serializer = TakeTransmitDeleteClassSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.take_class(secretary, serializer)
            case 'new_class':
                serializer = NewClassSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.new_class(secretary, serializer)
            case 'transmit_class':
                serializer = TakeTransmitDeleteClassSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.transmit_class(secretary, serializer)
            case 'delete_class':
                serializer = TakeTransmitDeleteClassSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.delete_class(secretary, serializer)
            case 'new_course':
                serializer = NewCourseSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.new_course(secretary, serializer)
            case 'save_course':
                serializer = EditCourseSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.save_course(secretary, serializer)
            case 'delete_course':
                serializer = DeleteCourseSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.delete_course(secretary, serializer)
            case 'add_teacher':
                serializer = AddTeacherSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.add_teacher(secretary, serializer)
            case 'remove_teacher':
                serializer = RemoveTeacherSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.remove_teacher(secretary, serializer)
            case _:
                return Response()

    def get(self, request):
        secretary = request.user
        match request.data['action']:
            case 'get_classes':
                serializer = GenericGetSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.get_classes(secretary, serializer)
            case 'get_teachers':
                serializer = GenericGetSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.get_teachers(secretary, serializer)
            case 'get_students':
                serializer = GenericGetSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.get_students(secretary, serializer)            
            case 'get_students_by_class':
                serializer = GetStudentsByClassSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.get_students_by_class(secretary, serializer)
            case 'get_teacher_subjects':
                serializer = GetTeacherSubjectsSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.get_teacher_subjects(secretary, serializer)
            case 'get_subjects':
                serializer = GenericGetSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.get_subjects(secretary, serializer)
            case 'get_courses':
                serializer = GetCoursesSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.get_courses(secretary, serializer)
            case 'get_teachers_subjects':
                serializer = GenericGetSerializer(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                except (DRFValidationError):
                    return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                return self.get_teachers_subjects(secretary, serializer)
            case _:
                return Response()

    #----------------------------------------------------------------------------------------------
    #GET    

    def get_classes(self, secretary, serializer):
        class_list = Class.objects.filter(
            Q(secretary_id=secretary) | Q(secretary_id__isnull=True),
            school_id=secretary.school_id,
        ).annotate(
            class_name=F('name'),
            secretary_name=Case(
                When(secretary_id=secretary, then=F('secretary_id__name')),
                default=Value(''),
                output_field=CharField()
            )
        ).values(
            'id',
            'class_name',
            'secretary_name',
        ).order_by('class_name')
        result = {'classes': list(class_list)}
        return Response(data=result, status=status.HTTP_200_OK, content_type=json)
    
    def get_teachers(self, secretary, serializer):
        teachers_list = User.objects.filter(
            Q(role='TEACHER') & (Q(secretary_id=secretary) | Q(secretary_id__isnull=True)),
            school_id=secretary.school_id,
            is_active=True
        ).annotate(
            teacher_name=F('name'),
            secretary_name=Case(
                When(secretary_id=secretary, then=F('secretary_id__name')),
                default=Value(''),
                output_field=CharField()
            )
        ).values(
            'id',
            'teacher_name',
            'email',
            'secretary_name',
            'archived',
        ).order_by('teacher_name')
        result = {'teachers': list(teachers_list)}
        return Response(data=result, status=status.HTTP_200_OK, content_type=json)

    def get_students(self, secretary, serializer):
        students_list = User.objects.filter(
            Q(role='STUDENT') & (Q(secretary_id=secretary) | Q(secretary_id__isnull=True)),
            school_id=secretary.school_id,
            is_active=True
        ).annotate(
            student_name=F('name'),
            secretary_name=Case(
                When(secretary_id=secretary, then=F('secretary_id__name')),
                default=Value(''),
                output_field=CharField()
            )
        ).values(
            'id',
            'student_name',
            'email',
            'secretary_name',
            'class_id',
            'archived',
        ).order_by('student_name')
        result = {'students': list(students_list)}
        return Response(data=result, status=status.HTTP_200_OK, content_type=json)

    def get_students_by_class(self, secretary, serializer):
        try:       
            class_id = serializer.validated_data['class_id']
        except KeyError:
            logger.error(f"Required data is missing from the serializer. {self.get_view_name()}, {self.get_students_by_class.__name__}")
            raise DRFValidationError("Required data is missing from the serializer.")  
        try:
            Class.objects.get(
                id=class_id,
                school_id=secretary.school_id,
                secretary_id=secretary
            )
        except Class.DoesNotExist:
            return Response({"error": "The secretary does not have access to this class."}, status=status.HTTP_400_BAD_REQUEST)
        students_list = User.objects.filter(
            role='STUDENT',
            secretary_id=secretary,
            class_id=class_id,
            school_id=secretary.school_id,
            is_active=True,
            archived=False
        ).annotate(
            student_name=F('name')
        ).values(
            'id',
            'student_name',
            'email'
        ).order_by('student_name')
        result = {'students': list(students_list)}
        return Response(data=result, status=status.HTTP_200_OK, content_type=json)

    def get_teacher_subjects(self, secretary, serializer):
        teacher_id = serializer.validated_data['teacher_id']
        teacher_subjects_list = TeacherSubject.objects.filter(
            teacher_id=teacher_id,
            teacher_id__secretary_id=secretary,
            teacher_id__school_id=secretary.school_id,
        ).values_list('subject_name__name', flat=True)    
        sorted_subjects = sorted(list(teacher_subjects_list))
        result = {'teacher_subjects': sorted_subjects}    
        return Response(data=result, status=status.HTTP_200_OK, content_type=json)  

    def get_subjects(self, secretary, serializer):
        subject_list = Subject.objects.all().values_list('name', flat=True)
        sorted_subjects = sorted(subject_list)
        result = {'subjects': sorted_subjects}
        return Response(data=result, status=status.HTTP_200_OK)
  

    def get_courses(self, secretary, serializer):
        try:       
            class_id = serializer.validated_data['class_id']
        except KeyError:
            logger.error(f"Required data is missing from the serializer. {self.get_view_name()}, {self.get_courses.__name__}")
            raise DRFValidationError("Required data is missing from the serializer.")  
        
        courses = Course.objects.filter(
            class_id=class_id,
            class_id__secretary_id=secretary
        ).order_by('name')
        result = []

        for course in courses:
            teacher_courses = TeacherCourse.objects.filter(course_id=course.id)
            teachers = [{'teacher_id': tc.teacher_id.id, 'teacher_name': tc.teacher_id.name} for tc in teacher_courses]

            result.append({
                'id': course.id,
                'course_name': course.name,
                'subject': course.subject_name.name,
                'teachers': teachers
            })
        result = {'courses': result}
        return Response(data=result, status=status.HTTP_200_OK, content_type=json)  

    def get_teachers_subjects(self, secretary, serializer):
        teachers = User.objects.filter(
            role='TEACHER',
            secretary_id=secretary,
            school_id=secretary.school_id,
            is_active=True
        ).values('id', 'name').order_by('name')

        teacher_list = []
        for teacher in teachers:
            subject_names = TeacherSubject.objects.filter(teacher_id=teacher['id']).values_list('subject_name__name', flat=True)
            teacher_list.append({
                'id': teacher['id'],
                'teacher_name': teacher['name'],
                'subjects': list(subject_names)
            })
        result = {'teachers_subjects': teacher_list}
        return Response(data=result, status=status.HTTP_200_OK, content_type=json)  

    #--------------------------------------------------------------------------
    #POST

    def new_teacher(self, secretary, serializer):
        try:
            teacher_name = serializer.validated_data['name']
            teacher_email = serializer.validated_data['email']
            subjects = serializer.validated_data['subjects']
        except KeyError:
            logger.error(f"Required data is missing from the serializer. {self.get_view_name()}, {self.new_teacher.__name__}")
            raise DRFValidationError("Required data is missing from the serializer.")  
        
        with transaction.atomic():
            try:
                new_teacher = User.objects.create(
                    email=teacher_email,
                    name=teacher_name,
                    role='TEACHER',
                    school_id=secretary.school_id,
                    secretary_id=secretary
                )
                # Create TeacherSubject objects for each subject
                for subject_name in subjects:
                    subject = Subject.objects.get(name=subject_name)
                    TeacherSubject.objects.create(
                        teacher_id=new_teacher,
                        subject_name=subject
                    )
            except Exception as e:
                return Response({"error": "User already exists."}, status=status.HTTP_400_BAD_REQUEST)
                # Handle any exceptions that occur during the creation process
                # This ensures that if any part of the process fails, changes are rolled back
                raise e
        return Response(data={}, status=status.HTTP_200_OK, content_type=json)
        
            
    def edit_teacher(self, secretary, serializer): 
        try:       
            teacher_id = serializer.validated_data['id']
            teacher_name = serializer.validated_data['name']
            subjects = serializer.validated_data['subjects']
        except KeyError:
            logger.error(f"Required data is missing from the serializer. {self.get_view_name()}, {self.edit_teacher.__name__}")
            raise DRFValidationError("Required data is missing from the serializer.")  
        try:
            teacher = User.objects.get(
                id=teacher_id,
                school_id=secretary.school_id,
                secretary_id=secretary,
                is_active=True,
                archived=False
            )
            teacher.name = teacher_name
            teacher.save(update_fields=['name'])
        except User.DoesNotExist:
            return Response({"error": "The secretary does not have access to this user."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch existing Subject objects for the subjects in the new subjects list
        existing_subjects = Subject.objects.filter(name__in=subjects)

        # Update TeacherSubject objects associated with the teacher user
        with transaction.atomic():
            try:
                # Delete TeacherSubjects not in the new subjects list
                TeacherSubject.objects.filter(teacher_id=teacher_id).exclude(subject_name__name__in=subjects).delete()

                # Create new TeacherSubjects for existing subjects in the new subjects list
                for subject in existing_subjects:
                    TeacherSubject.objects.get_or_create(teacher_id=teacher, subject_name=subject)
                teacher_subject_names = TeacherSubject.objects.filter(
                    teacher_id=teacher_id
                ).values_list('subject_name', flat=True)

                # Delete TeacherCourse objects where the Course.subject_name is not in the teacher's subject names
                TeacherCourse.objects.filter(                    
                    ~Q(course_id__subject_name__in=teacher_subject_names),
                    teacher_id=teacher_id
                ).delete()
            except Exception as e:
                # Handle any exceptions that occur during the creation process
                # This ensures that if any part of the process fails, changes are rolled back
                raise e
        return Response(data={}, status=status.HTTP_200_OK, content_type=json)

    def new_student(self, secretary, serializer):
        try:
            student_name = serializer.validated_data['name']
            student_email = serializer.validated_data['email']
            class_id = serializer.validated_data['class_id']
        except KeyError:
            logger.error(f"Required data is missing from the serializer. {self.get_view_name()}, {self.new_student.__name__}")
            raise DRFValidationError("Required data is missing from the serializer.")  
        try:
            if class_id==-1:
                User.objects.create(
                        email=student_email,
                        name=student_name,
                        role='STUDENT',
                        school_id=secretary.school_id,
                        secretary_id=secretary
                    )
            else:
                class_ = Class.objects.get(
                    id=class_id,
                    school_id=secretary.school_id,
                    secretary_id=secretary
                )
                student = User.objects.create(
                    email=student_email,
                    name=student_name,
                    role='STUDENT',
                    school_id=secretary.school_id,
                    secretary_id=secretary,
                    class_id=class_
                )
                new_courses = Course.objects.filter(
                    class_id = class_
                )

                for course in new_courses:
                    new_coursetopics = CourseTopic.objects.filter(
                        course_id = course,
                        available = True
                    )
                    for coursetopic in new_coursetopics:
                        subtopics = SubTopic.objects.filter(
                            topic_id = coursetopic.topic_id
                        )
                        for subtopic in subtopics:
                            CompletedSubTopic.objects.create(
                                student_id = student,
                                course_id = course,
                                subtopic_id = subtopic,
                                number = subtopic.number
                            )
                        CompletedTopic.objects.create(
                            student_id = student,
                            course_id = course,
                            topic_id = coursetopic.topic_id
                        )
                        TestResult.objects.create(student_id = student,
                            course_id = course,
                            topic_id = coursetopic.topic_id
                        )
        except Exception as e:
            return Response({"error": "User already exists."}, status=status.HTTP_400_BAD_REQUEST)
            # Handle any exceptions that occur during the creation process
            # This ensures that if any part of the process fails, changes are rolled back
            raise e
        return Response(data={}, status=status.HTTP_200_OK, content_type=json)

    def edit_student(self, secretary, serializer):
        try:       
            student_id = serializer.validated_data['id']
            student_name = serializer.validated_data['name']
        except KeyError:
            logger.error(f"Required data is missing from the serializer. {self.get_view_name()}, {self.edit_student.__name__}")
            raise DRFValidationError("Required data is missing from the serializer.")  
        try:
            student = User.objects.get(
                id=student_id,
                school_id=secretary.school_id,
                secretary_id=secretary,
                is_active=True,
                archived=False
            )
            student.name = student_name
            student.save(update_fields=['name'])
        except User.DoesNotExist:
            return Response({"error": "The secretary does not have access to this user."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={}, status=status.HTTP_200_OK, content_type=json)

    def add_to_class(self, secretary, serializer):
        try:
            class_id = serializer.validated_data['class_id']
            students = serializer.validated_data['students']
        except KeyError:
            logger.error(f"Required data is missing from the serializer. {self.get_view_name()}, {self.add_to_class.__name__}")
            raise DRFValidationError("Required data is missing from the serializer.")  
        with transaction.atomic():
            try:
                students = User.objects.filter(
                    id__in=students,
                    school_id=secretary.school_id,
                    role='STUDENT',
                    is_active=True
                ).filter(
                    Q(secretary_id=secretary) | Q(secretary_id__isnull=True)
                )

                class_ = Class.objects.get(
                    id=class_id,
                    school_id=secretary.school_id,
                    secretary_id=secretary
                )

                new_courses = Course.objects.filter(
                    class_id = class_
                )

                for student in students:   
                    old_courses = Course.objects.filter(
                        class_id=student.class_id
                    )
                    for course in old_courses:
                        TaskProgress.objects.filter(
                            student_id=student,
                            course_id=course,
                        ).delete()
                        CompletedSubTopic.objects.filter(
                            student_id=student,
                            course_id=course,
                        ).delete()
                        CompletedTopic.objects.filter(
                            student_id=student,
                            course_id=course,
                        ).delete()
                        TestProgress.objects.filter(
                            student_id=student,
                            course_id=course,
                        ).delete()
                        TestResult.objects.filter(
                            student_id=student,
                            course_id=course,
                        ).delete()

                    for course in new_courses:
                        new_coursetopics = CourseTopic.objects.filter(
                            course_id = course,
                            available = True
                        )
                        for coursetopic in new_coursetopics:
                            subtopics = SubTopic.objects.filter(
                                topic_id = coursetopic.topic_id
                            )
                            for subtopic in subtopics:
                                CompletedSubTopic.objects.create(
                                    student_id = student,
                                    course_id = course,
                                    subtopic_id = subtopic,
                                    number = subtopic.number
                                )
                            CompletedTopic.objects.create(
                                student_id = student,
                                course_id = course,
                                topic_id = coursetopic.topic_id
                            )
                            TestResult.objects.create(student_id = student,
                                course_id = course,
                                topic_id = coursetopic.topic_id
                            )
                    student.class_id = class_
                    student.secretary_id = secretary
                    student.archived = False
                    student.save(update_fields=['class_id', 'secretary_id', 'archived'])
            except ObjectDoesNotExist:
                # Handle case where student with provided ID does not exist
                # You might want to raise an exception or return an appropriate response
                raise ObjectDoesNotExist
        return Response(data={}, status=status.HTTP_200_OK, content_type=json)

    def admission(self, secretary, serializer):
        try:
            user_type = serializer.validated_data['user']
            users = serializer.validated_data['user_ids']
        except KeyError:
            logger.error(f"Required data is missing from the serializer. {self.get_view_name()}, {self.admission.__name__}")
            raise DRFValidationError("Required data is missing from the serializer.")  
        with transaction.atomic():
            try:
                admission_list = User.objects.filter(
                    id__in=users,
                    secretary_id__isnull=True,
                    school_id=secretary.school_id,
                    is_active=True
                )

                for user in admission_list:
                    user.secretary_id = secretary
                    user.archived = False
                    user.save(update_fields=['secretary_id', 'archived'])
            except ObjectDoesNotExist:
                # Handle case where teacher with provided ID does not exist
                # You might want to raise an exception or return an appropriate response
                raise ObjectDoesNotExist
        return Response(data={}, status=status.HTTP_200_OK, content_type=json)
        
    def discharge(self, secretary, serializer):
        try:
            user_type = serializer.validated_data['user']
            users = serializer.validated_data['user_ids']
        except KeyError:
            logger.error(f"Required data is missing from the serializer. {self.get_view_name()}, {self.discharge.__name__}")
            raise DRFValidationError("Required data is missing from the serializer.")  
        with transaction.atomic():
            try:
                admission_list = User.objects.filter(
                    id__in=users,
                    secretary_id=secretary,
                    school_id=secretary.school_id,
                    is_active=True,
                    archived=False                  
                )

                for user in admission_list:
                    user.secretary_id = None
                    user.class_id = None
                    user.save(update_fields=['secretary_id', 'class_id'])
            except ObjectDoesNotExist:
                # Handle case where teacher with provided ID does not exist
                # You might want to raise an exception or return an appropriate response
                raise ObjectDoesNotExist
        return Response(data={}, status=status.HTTP_200_OK, content_type=json)

    def archive(self, secretary, serializer):
        try:
            user_type = serializer.validated_data['user']
            users = serializer.validated_data['user_ids']
        except KeyError:
            logger.error(f"Required data is missing from the serializer. {self.get_view_name()}, {self.archive.__name__}")
            raise DRFValidationError("Required data is missing from the serializer.") 
        with transaction.atomic():
            try:
                admission_list = User.objects.filter(
                    Q(id__in=users) &
                    Q(school_id=secretary.school_id) &
                    Q(is_active=True) &
                    Q(archived=False) &
                    (Q(secretary_id=secretary) | Q(secretary_id=None))
                )

                for user in admission_list:
                    old_courses = Course.objects.filter(
                        class_id=user.class_id
                    )
                    for course in old_courses:
                        TaskProgress.objects.filter(
                            student_id=user,
                            course_id=course,
                        ).delete()
                        CompletedSubTopic.objects.filter(
                            student_id=user,
                            course_id=course,
                        ).delete()
                        CompletedTopic.objects.filter(
                            student_id=user,
                            course_id=course,
                        ).delete()
                        TestProgress.objects.filter(
                            student_id=user,
                            course_id=course,
                        ).delete()
                        TestResult.objects.filter(
                            student_id=user,
                            course_id=course,
                        ).delete()
                    user.secretary_id = None
                    user.archived = True
                    user.class_id = None
                    user.save(update_fields=['secretary_id', 'archived', 'class_id'])
            except ObjectDoesNotExist:
                # Handle case where teacher with provided ID does not exist
                # You might want to raise an exception or return an appropriate response
                raise ObjectDoesNotExist
        return Response(data={}, status=status.HTTP_200_OK, content_type=json)

    def take_class(self, secretary, serializer):
        try:
            class_id = serializer.validated_data['id']
        except KeyError:
            logger.error(f"Required data is missing from the serializer. {self.get_view_name()}, {self.take_class.__name__}")
            raise DRFValidationError("Required data is missing from the serializer.") 
        try:
            class_obj = Class.objects.get(
                id=class_id,
                school_id=secretary.school_id,
                secretary_id__isnull=True
            )
        except Class.DoesNotExist:
            return Response({"error": "The secretary does not have access to this class."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            try:
                class_obj.secretary_id = secretary
                class_obj.save(update_fields=['secretary_id'])

                students = User.objects.filter(
                    class_id=class_id,
                    role='STUDENT',
                    secretary_id__isnull=True,
                    is_active=True,
                    archived=False,
                    school_id=secretary.school_id
                )
                for student in students:
                    student.secretary_id = secretary
                    student.save(update_fields=['secretary_id'])
            except ObjectDoesNotExist:
                # Handle case where class with provided ID does not exist
                # You might want to raise an exception or return an appropriate response
                raise ObjectDoesNotExist
        return Response(data={}, status=status.HTTP_200_OK, content_type=json)

    def new_class(self, secretary, serializer):
        try:
            class_name = serializer.validated_data['name']
            class_id = serializer.validated_data['class_id']
        except KeyError:
            logger.error(f"Required data is missing from the serializer. {self.get_view_name()}, {self.new_class.__name__}")
            raise DRFValidationError("Required data is missing from the serializer.") 
        if class_id==-1:
            try:
                new_class = Class.objects.create(
                    name=class_name,
                    secretary_id=secretary,
                    school_id=secretary.school_id
                )
                return Response({'class_id':new_class.id})
            except Exception as e:
                # Handle any exceptions that occur during the creation process
                # This ensures that if any part of the process fails, changes are rolled back
                raise e
        else:
            with transaction.atomic():
                try:
                    new_class = Class.objects.get(
                        id=class_id,
                        secretary_id=secretary,
                        school_id=secretary.school_id
                    )
                    new_class.name = class_name
                    new_class.save(update_fields=['name'])
                    return Response({'class_id':new_class.id})
                except Exception as e:
                    # Handle any exceptions that occur during the creation process
                    # This ensures that if any part of the process fails, changes are rolled back
                    raise e
        return Response(data={}, status=status.HTTP_200_OK, content_type=json)
        
    def transmit_class(self, secretary, serializer):
        try:
            class_id = serializer.validated_data['id']
        except KeyError:
            logger.error(f"Required data is missing from the serializer. {self.get_view_name()}, {self.transmit_class.__name__}")
            raise DRFValidationError("Required data is missing from the serializer.") 
        try:
            class_obj = Class.objects.get(
                id=class_id,
                school_id=secretary.school_id,
                secretary_id=secretary
            )
        except Class.DoesNotExist:
            return Response({"error": "The secretary does not have access to this class."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            try:
                class_obj.secretary_id = None
                class_obj.save(update_fields=['secretary_id'])

                students = User.objects.filter(
                    class_id=class_id,
                    role='STUDENT',
                    secretary_id=secretary,
                    school_id=secretary.school_id,
                    is_active = True,
                    archived=False
                )
                for student in students:
                    student.secretary_id = None
                    student.save(update_fields=['secretary_id'])

            except ObjectDoesNotExist:
                # Handle case where class with provided ID does not exist
                # You might want to raise an exception or return an appropriate response
                raise ObjectDoesNotExist
        return Response(data={}, status=status.HTTP_200_OK, content_type=json)
        
    def delete_class(self, secretary, serializer):
        try:
            class_id = serializer.validated_data['id']
        except KeyError:
            logger.error(f"Required data is missing from the serializer. {self.get_view_name()}, {self.delete_class.__name__}")
            raise DRFValidationError("Required data is missing from the serializer.") 
        with transaction.atomic():
            try:
                User.objects.filter(
                    class_id=class_id,
                    secretary_id=secretary,
                    school_id=secretary.school_id,
                    is_active = True
                ).update(
                    secretary_id=None,
                    class_id=None,
                    archived=True
                )
                # Delete the Class object with the provided class_id
                # Delete the Course objects where class_id is a foreign key
                # Delete all objects where deleted courses are foreign keys
                try:
                    Class.objects.get(
                        id=class_id,
                        secretary_id=secretary,
                        school_id=secretary.school_id
                    ).delete()
                except Class.DoesNotExist:
                    return Response({"error": "The secretary does not have access to this class."}, status=status.HTTP_400_BAD_REQUEST)
            except ObjectDoesNotExist:
                # Handle case where class with provided ID does not exist
                # You might want to raise an exception or return an appropriate response
                raise ObjectDoesNotExist
        return Response(data={}, status=status.HTTP_200_OK, content_type=json)
            
    def new_course(self, secretary, serializer):
        try:
            class_id = serializer.validated_data['class_id']
            course_name = serializer.validated_data['course_name']
            subject_name = serializer.validated_data['subject_name']
        except KeyError:
            logger.error(f"Required data is missing from the serializer. {self.get_view_name()}, {self.new_course.__name__}")
            raise DRFValidationError("Required data is missing from the serializer.") 
        try:
            class_ = Class.objects.get(
                id=class_id,
                secretary_id=secretary,
                school_id=secretary.school_id
            )
        except Class.DoesNotExist:
            return Response({"error": "The secretary does not have access to this class."}, status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            try:
                subject = Subject.objects.get(
                    name = subject_name
                )
                # Create a new Course object
                course = Course.objects.create(
                    name=course_name,
                    class_id=class_,
                    subject_name=subject
                )
                topics = Topic.objects.filter(subject_name=subject_name)
                for topic in topics:
                    CourseTopic.objects.create(
                        course_id=course,
                        topic_id=topic,
                    )
            except Exception as e:
                # Handle any exceptions that occur during the creation process
                # This ensures that if any part of the process fails, changes are rolled back
                raise e
        return Response(data={}, status=status.HTTP_200_OK, content_type=json)

    def save_course(self, secretary, serializer):
        try:
            course_id = serializer.validated_data['course_id']
            name = serializer.validated_data['course_name']
        except KeyError:
            logger.error(f"Required data is missing from the serializer. {self.get_view_name()}, {self.save_course.__name__}")
            raise DRFValidationError("Required data is missing from the serializer.") 
        try:
            course = Course.objects.get(
                id=course_id,
                class_id__secretary_id=secretary.id,
                class_id__school_id=secretary.school_id
            )
            course.name = name
            course.save(update_fields=['name'])
        except Course.DoesNotExist:
            return Response({"error": "The secretary does not have access to this course."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={}, status=status.HTTP_200_OK, content_type=json)
        
    def delete_course(self, secretary, serializer):
        try:
            course_id = serializer.validated_data['course_id']
        except KeyError:
            logger.error(f"Required data is missing from the serializer. {self.get_view_name()}, {self.delete_course.__name__}")
            raise DRFValidationError("Required data is missing from the serializer.") 
        try:
            Course.objects.get(
                id=course_id,
                class_id__secretary_id=secretary,
                class_id__school_id=secretary.school_id
            ).delete()
        except Course.DoesNotExist:
            return Response({"error": "The secretary does not have access to this course."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={}, status=status.HTTP_200_OK, content_type=json)

        
    def add_teacher(self, secretary, serializer):
        try:
            class_id = serializer.validated_data['class_id']
            course_id = serializer.validated_data['course_id']
            teacher_id = serializer.validated_data['teacher_id']
        except KeyError:
            logger.error(f"Required data is missing from the serializer. {self.get_view_name()}, {self.add_teacher.__name__}")
            raise DRFValidationError("Required data is missing from the serializer.") 
        try:
            course = Course.objects.get(
                id=course_id,
                class_id=class_id,
                class_id__secretary_id=secretary,
                class_id__school_id=secretary.school_id
            )
        except Course.DoesNotExist:
            return Response({"error": "The secretary does not have access to this course."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            teacher = User.objects.get(
                id=teacher_id,
                role='TEACHER',
                secretary_id=secretary,
                school_id=secretary.school_id,
                is_active=True,
                archived=False
            )
        except User.DoesNotExist:
            return Response({"error": "The secretary does not have access to this user."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            TeacherSubject.objects.get(teacher_id=teacher, subject_name=course.subject_name)
        except TeacherSubject.DoesNotExist:
            return Response({'error':"The teacher does not teaches this subject"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                TeacherCourse.objects.create(
                    teacher_id=teacher,
                    course_id=course
                )
            except Exception as e:
                # Handle any exceptions that occur during the creation process
                # This ensures that if any part of the process fails, changes are rolled back
                raise e
        return Response(data={}, status=status.HTTP_200_OK, content_type=json)
    
    def remove_teacher(self, secretary, serializer):
        try:
            course_id = serializer.validated_data['course_id']
            teacher_id = serializer.validated_data['teacher_id']
        except KeyError:
            logger.error(f"Required data is missing from the serializer. {self.get_view_name()}, {self.remove_teacher.__name__}")
            raise DRFValidationError("Required data is missing from the serializer.")
        try:
            TeacherCourse.objects.get(
                teacher_id=teacher_id,
                teacher_id__secretary_id=secretary,
                teacher_id__archived=False,
                teacher_id__is_active=True,
                course_id=course_id
            ).delete()

        except TeacherCourse.DoesNotExist:
            return Response({'error':"The teacher does not teaches this subject"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={}, status=status.HTTP_200_OK, content_type=json)