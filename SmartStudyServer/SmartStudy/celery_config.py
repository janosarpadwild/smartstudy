import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SmartStudy.settings')

# Create a Celery instance.
app = Celery('SmartStudy')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Use Redis as the broker.
app.conf.broker_url = 'redis://localhost:6379/0'

# Use Redis as the result backend.
app.conf.result_backend = 'redis://localhost:6379/0'

# Set broker_connection_retry_on_startup to True to retain the existing behavior for retrying connections on startup.
app.conf.broker_connection_retry_on_startup = True

# Autodiscover tasks in all applications listed in INSTALLED_APPS.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'delete-expired-tokens': {
        'task': 'SmartStudyApp.tasks.delete_expired_tokens',
        'schedule': 900  # Run every 15 minutes -> 24 * 3600,  # Run every 24 hours
    },
    'delete-expired-permission-codes': {
        'task': 'SmartStudyApp.tasks.delete_expired_permission_codes',
        'schedule': 900  # Run every 15 minutes -> 24 * 3600,  # Run every 24 hours
    },
    'delete-expired-lock-codes': {
        'task': 'SmartStudyApp.tasks.delete_expired_lock_codes',
        'schedule': 900  # Run every 15 minutes -> 72 * 3600,  # Run every 72 hours
    }
}
