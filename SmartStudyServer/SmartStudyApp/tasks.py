from celery import shared_task
from SmartStudyApp.models import CustomToken, PermissionCode, LockAccount
from django.utils import timezone

@shared_task
def delete_expired_tokens():
    expired_tokens = CustomToken.objects.filter(used=True)
    expired_tokens.delete()

@shared_task
def delete_expired_permission_codes():
    expired_permission_codes = PermissionCode.objects.filter(expiration_time__lt=timezone.now())
    expired_permission_codes.delete()

@shared_task
def delete_expired_lock_codes():
    expired_lock_codes = LockAccount.objects.filter(expiration_time__lt=timezone.now())
    expired_lock_codes.delete()