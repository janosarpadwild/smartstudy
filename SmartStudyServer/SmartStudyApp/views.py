#from django.shortcuts import render
#import asyncio

#CAN DUPLICATE PERMISSION CODE AND LOCK CODE

from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import LoginSerializer, NewPasswordSerializer, NewEmailSerializer, ChangePasswordSerializer, ChangeEmailSerializer, LockAccountSerializer
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.mail import send_mail
from rest_framework import status
from django.utils import timezone
from rest_framework.response import Response
from .models import CustomToken, User, PermissionCode, LockAccount
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.utils.crypto import get_random_string
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .utils.student_actions import available_student_actions, StudentAPIView
from .utils.teacher_actions import available_teacher_actions, TeacherAPIView
from .utils.secretary_actions import available_secretary_actions, SecretaryAPIView

import logging

import SmartStudyApp.models
from random import randint

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

student_api_view = StudentAPIView()
teacher_api_view = TeacherAPIView()
secretary_api_view = SecretaryAPIView()

class LoginAPIView(ObtainAuthToken):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except (DRFValidationError, DjangoValidationError):
            print('inv')
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        action = serializer.validated_data['action']
        
        if action != 'login':
                return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except Exception:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if not user or not check_password(password, user.password):
            Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED, headers={'WWW-Authenticate': 'Bearer realm="api/login"'})
        if not user.is_active or user.archived:
            return Response({'error': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        CustomToken.objects.filter(user=user).delete()
        token = CustomToken.objects.create(user=user)        
        return Response({'message': 'Login successful', 'token': token.key, 'user_category': user.role, 'name': user.name}, status=status.HTTP_200_OK)

class SmartStudyAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        self.validate_user(request)
        return self.role(request)

    def post(self, request):
        action = self.validate_user(request)
        if action == 'logout':
            request.auth.used = True
            request.auth.save(update_fields=['used'])
            return Response({'message': 'Logout successful'})
        # Access authenticated user
        return self.role(request)
    
    def validate_user(self, request):
        if not request.user.is_active or request.user.archived:
            return Response( {'error': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        action = request.data.get('action')
        if action == 'logout':
            return action
        if action not in available_student_actions + available_teacher_actions + available_secretary_actions:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
    
    def role(self, request):
        user = request.user
        if user.role == 'STUDENT':
            #student_api_view = StudentAPIView()
            if request.method == "GET":
                return student_api_view.get(request)
            elif request.method == "POST":
                return student_api_view.post(request)
        elif user.role == 'TEACHER':
            #teacher_api_view = TeacherAPIView()
            if request.method == "GET":
                return teacher_api_view.get(request)
            elif request.method == "POST":
                return teacher_api_view.post(request)
        elif user.role == 'SECRETARY':
            #secretary_api_view = SecretaryAPIView()
            if request.method == "GET":
                return secretary_api_view.get(request)
            elif request.method == "POST":
                return secretary_api_view.post(request)
        return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

class NewCredentialsRequestAPIView(APIView):
    def get(self, request):
        action = request.data.get('action')
        user = None
        if action == 'new_password':
            serializer = NewPasswordSerializer(data=request.data)            
        elif action == 'new_email':
            serializer = NewEmailSerializer(data=request.data)
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            serializer.is_valid(raise_exception=True)
        except (DRFValidationError, DjangoValidationError):
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        new_email=''

        if action == 'new_email':
            new_email = serializer.validated_data['new_email']
            new_email_repeat = serializer.validated_data['new_email_repeat']
            password = serializer.validated_data['password']
            if new_email != new_email_repeat or User.objects.filter(email=new_email).exists():
                return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.get(email=email)
            if not check_password(password, user.password):
                return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED, headers={'WWW-Authenticate': 'Bearer realm="api/new_email_request"'})

        if not user:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED, headers={'WWW-Authenticate': 'Bearer realm="api/new_email_request"'})
        if not user.is_active or user.archived:
            return Response({'error': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        
        # Generate permission code
        permission_code = get_random_string(length=24)
        permission_hashed_code = make_password(permission_code)
        expiration_time = timezone.now() + timezone.timedelta(hours=1)
        if action == 'new_password':
            PermissionCode.objects.create(user=user, action=action, permission_code=permission_hashed_code, expiration_time=expiration_time)
        elif action == 'new_email':
            PermissionCode.objects.create(user=user, action=action, new_email=new_email, permission_code=permission_hashed_code, expiration_time=expiration_time)

        subject = f'Your permission code [SmartStudy account][{action.split('_')[1]}]'
        message = f'Dear {user.name}!\n\nYour permission code to create your new {action.split('_')[1]} is:\n{permission_code}\n\nCopy this code to the SmartStudy program to be able to enter the new {action.split('_')[1]}.\nThis code will expire in one hour.\n\nBest regards!\nSmartStudy'
        send_mail(subject, message, None, [user.email])

        #self.send_permission_code_email(user.name, user.email, permission_code, action)
        return Response({'message': 'Permission code sent to your email'})
      
    def send_permission_code_email(name, email, permission_code, action):
        subject = f'Your permission code [SmartStudy account][{action.split('_')[1]}]'
        message = f'Dear {name}!\n\nYour permission code to create your new {action.split('_')[1]} is:\n{permission_code}\n\nCopy this code to the SmartStudy program to be able to enter the new {action.split('_')[1]}.\nThis code will expire in one hour.\n\nBest regards!\nSmartStudy'
        send_mail(subject, message, None, [email])

class ChangeCredentialsAPIView(APIView):
    def validate_permission_code(self, serializer):
        permission_code = serializer.validated_data['permission_code']
        permission_code_list = PermissionCode.objects.filter()
        print(permission_code_list)
        if type(permission_code_list)!=None:
            for i in permission_code_list:
                if check_password(permission_code, i.permission_code):
                    return i
        return None        

    def post(self, request):        
        action = request.data.get('action')
        if action == 'new_password':
            serializer = ChangePasswordSerializer(data=request.data)
        elif action == 'new_email':
            serializer = ChangeEmailSerializer(data=request.data)
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            serializer.is_valid(raise_exception=True)
        except (DRFValidationError, DjangoValidationError):
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
        
        permission_code_obj = self.validate_permission_code(serializer)
        print('valids')
        if not permission_code_obj:
            return Response({'error': 'Invalid permission code'}, status=status.HTTP_400_BAD_REQUEST)
        if permission_code_obj.expiration_time < timezone.now():
            return Response({'error': 'Permission code has expired'}, status=status.HTTP_400_BAD_REQUEST)
        if action == 'new_password':
            new_password_1 = serializer.validated_data['password']
            new_password_2 = serializer.validated_data['password_repeat']
            if new_password_1 != new_password_2:
                return Response({'error': 'Passwords do not match. Please ensure that the new password is entered correctly in both fields.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = permission_code_obj.user

        if not user.is_active or user.archived:
            return Response({'error': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            if action == 'new_password':
                hashed_password = make_password(new_password_1)
                user.password = hashed_password
                user.save(update_fields=["password"])
            elif action == 'new_email':
                user.email = permission_code_obj.new_email
                user.save(update_fields=["email"])
        except:
            return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

        unauthorized_access_code = get_random_string(length=24)
        unauthorized_access_hashed_code = make_password(unauthorized_access_code)
        expiration_time = timezone.now() + timezone.timedelta(hours=72)        
        LockAccount.objects.create(user=user, lock_code=unauthorized_access_hashed_code, expiration_time=expiration_time)      
        subject = f'New {action.split('_')[1]} [SmartStudy account]'
        message = f'Dear {user.name}!\n\nA new {action.split('_')[1]} has been set to your account.\nIf it was not you who changed your {action.split('_')[1]}, then copy this code into the SmartStudy program to lock your account and prevent unauthorized access:\n{unauthorized_access_code}\n\nIf it wa you who made the change then you do not have to do anything and this link deactivates in 72 hours.'
        send_mail(subject, message, None, [user.email])
        #self.send_new_credentials_email(user.name, user.email, unauthorized_access_code, action)
        permission_code_obj.delete()
        return Response({'message': 'User information updated successfully'})        
        
    def send_new_credentials_email(self, name, email, unauthorized_access_code, action):
        subject = f'New {action.split('_')[1]} [SmartStudy account]'
        message = f'Dear {name}!\n\nA new {action.split('_')[1]} has been set to your account.\nIf it was not you who changed your {action.split('_')[1]}, then copy this code into the SmartStudy program to lock your account and prevent unauthorized access:\n{unauthorized_access_code}\n\nIf it wa you who made the change then you do not have to do anything and this link deactivates in 72 hours.'
        send_mail(subject, message, None, [email])

class LockAccountAPIView(APIView):
    def validate_lock_code(self, serializer):
        lock_code = serializer.validated_data['lock_code']
        lock_code_list = LockAccount.objects.filter()
        for i in lock_code_list:
            if check_password(lock_code, i.lock_code):
                return i
        return None 
    def post(self, request):
        serializer = LockAccountSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except (DRFValidationError, DjangoValidationError):
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
        action = serializer.validated_data['action']
        if action != 'lock_account':
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
        lock_code_obj = self.validate_lock_code(serializer)
        if not lock_code_obj:
            return Response({'error': 'Invalid permission code'}, status=status.HTTP_400_BAD_REQUEST)
        if lock_code_obj.expiration_time < timezone.now():
            return Response({'error': 'Lock code has expired'}, status=status.HTTP_400_BAD_REQUEST)
        user = lock_code_obj.user
        user.is_active = False
        user.save(update_fields=["is_active"])
        #self.send_locked_account_email(user.name, user.email)
        subject = f'Locked account [SmartStudy account]'
        message = f'Dear {user.name}!\n\nYour account has been locked at your request.\nContact our administrator to unlock the user account'
        print(user.email)
        send_mail(subject, message, None, [user.email])
        lock_code_obj.delete()
        return Response({'message': 'User information updated successfully'}) 
    
    def send_locked_account_email(self, name, email):
        subject = f'Locked account [SmartStudy account]'
        message = f'Dear {name}!\n\nYour account has been locked at your request.\nContact our administrator to unlock the user account'
        send_mail(subject, message, None, [email])