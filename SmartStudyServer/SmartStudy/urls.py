"""
URL configuration for SmartStudy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from SmartStudyApp.views import LoginAPIView, SmartStudyAPIView, NewCredentialsRequestAPIView, ChangeCredentialsAPIView, LockAccountAPIView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', LoginAPIView.as_view(), name='api_login'),    
    path('api/smartstudy/', SmartStudyAPIView.as_view(), name='api_smartstudy'),
    path('api/new_credentials_request/', NewCredentialsRequestAPIView.as_view(), name='api_new_credentials'),
    path('api/change_credentials/', ChangeCredentialsAPIView.as_view(), name='api_change_credentials'),
    path('api/lock_account/', LockAccountAPIView.as_view(), name='lock_account'),
]
