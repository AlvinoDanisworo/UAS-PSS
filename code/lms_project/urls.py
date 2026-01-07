"""
URL configuration for lms_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from courses.api import apiv1
from courses.health import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health_check'),  # Health check endpoint
    path('', include('courses.urls')),  # Include courses URLs
    path('api/v1/', apiv1.urls),  # Include API URLs
]
