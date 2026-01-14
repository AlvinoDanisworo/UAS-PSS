# PANDUAN SETUP PROJECT DARI AWAL
# Learning Management System dengan Django & Django Ninja

---

## 📋 Daftar Isi
1. [Persiapan Environment](#persiapan-environment)
2. [Instalasi Software](#instalasi-software)
3. [Inisialisasi Project](#inisialisasi-project)
4. [Urutan Pembuatan File](#urutan-pembuatan-file)
5. [Konfigurasi Database](#konfigurasi-database)
6. [Testing Project](#testing-project)
7. [Deployment Preparation](#deployment-preparation)

---

## ⚙️ Persiapan Environment

### 1. Requirement Software

Sebelum memulai, pastikan software berikut sudah terinstall:

| Software | Versi Minimum | Purpose |
|----------|---------------|---------|
| **Python** | 3.10+ | Backend programming language |
| **pip** | Latest | Package manager |
| **PostgreSQL** | 14+ | Database server |
| **Git** | 2.30+ | Version control |
| **Docker** | 20.10+ | Containerization (optional) |
| **Docker Compose** | 2.0+ | Multi-container orchestration |
| **Code Editor** | - | VS Code / PyCharm |

### 2. Cek Instalasi

Buka terminal dan cek versi software:

```bash
# Check Python
python --version
# Output: Python 3.14.0 (atau versi lain >= 3.10)

# Check pip
pip --version
# Output: pip 24.0 atau lebih baru

# Check PostgreSQL
psql --version
# Output: psql (PostgreSQL) 14.x

# Check Git
git --version
# Output: git version 2.x.x

# Check Docker (optional)
docker --version
docker-compose --version
```

---

## 📥 Instalasi Software

### Windows

#### 1. Install Python
```bash
# Download dari python.org
# Atau gunakan winget:
winget install Python.Python.3.14

# Pastikan "Add Python to PATH" dicentang saat install
```

#### 2. Install PostgreSQL
```bash
# Download dari postgresql.org
# Atau gunakan installer:
# https://www.postgresql.org/download/windows/

# Catat password yang Anda buat untuk user postgres
```

#### 3. Install Git
```bash
winget install Git.Git
```

#### 4. Install Docker Desktop (Optional)
```bash
# Download dari docker.com
# https://www.docker.com/products/docker-desktop/
```

### Linux (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Install Python
sudo apt install python3.10 python3-pip python3-venv

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Install Git
sudo apt install git

# Install Docker
sudo apt install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
```

### macOS

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.14

# Install PostgreSQL
brew install postgresql@14
brew services start postgresql@14

# Install Git
brew install git

# Install Docker Desktop
brew install --cask docker
```

---

## 🚀 Inisialisasi Project

### Step 1: Buat Folder Project

```bash
# Buat folder utama project
mkdir lms-project
cd lms-project

# Buat subfolder untuk code
mkdir code
cd code
```

### Step 2: Setup Virtual Environment

```bash
# Buat virtual environment
python -m venv venv

# Aktivasi virtual environment

# Windows (PowerShell):
venv\Scripts\Activate.ps1

# Windows (CMD):
venv\Scripts\activate.bat

# Linux/macOS:
source venv/bin/activate

# Setelah aktivasi, prompt akan berubah menjadi:
# (venv) PS C:\path\to\lms-project\code>
```

### Step 3: Install Django dan Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install Django
pip install django==5.2.7

# Install dependencies satu per satu untuk memastikan
pip install psycopg2-binary
pip install pillow
pip install django-ninja
pip install django-ninja-jwt
pip install python-dotenv
pip install gunicorn
pip install whitenoise
pip install dj-database-url
```

### Step 4: Generate requirements.txt

```bash
# Save installed packages
pip freeze > requirements.txt
```

### Step 5: Inisialisasi Git

```bash
# Initialize git repository
git init

# Buat .gitignore (akan dibuat di step selanjutnya)
```

---

## 📝 Urutan Pembuatan File

Berikut adalah **urutan lengkap** file yang harus dibuat beserta isinya:

### FASE 1: Setup Dasar Project

#### File 1: `.gitignore`
**Lokasi**: `lms-project/.gitignore`

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Django
*.log
db.sqlite3
db.sqlite3-journal
/staticfiles/
/media/

# Environment variables
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Docker
*.pid
```

#### File 2: `.env`
**Lokasi**: `lms-project/.env`

```env
# Django Settings
SECRET_KEY=django-insecure-development-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings (Development)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=lms_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME_HOURS=24
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
```

#### File 3: `requirements.txt`
**Lokasi**: `lms-project/requirements.txt`

```txt
django==5.2.7
psycopg2-binary
pillow
django-ninja
django-ninja-jwt
python-dotenv
gunicorn
whitenoise
dj-database-url
```

#### File 4: Create Django Project

```bash
# Dari folder lms-project/code
django-admin startproject lms_project .

# Ini akan membuat:
# lms_project/
#   __init__.py
#   settings.py
#   urls.py
#   wsgi.py
#   asgi.py
# manage.py
```

#### File 5: Create Django App

```bash
# Masih di folder lms-project/code
python manage.py startapp courses

# Ini akan membuat folder courses/ dengan:
# courses/
#   __init__.py
#   admin.py
#   apps.py
#   models.py
#   tests.py
#   views.py
#   migrations/
```

---

### FASE 2: Konfigurasi Django

#### File 6: `lms_project/settings.py`
**Lokasi**: `lms-project/code/lms_project/settings.py`

**Action**: Edit file yang sudah ada, tambahkan/ubah bagian berikut:

```python
from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(BASE_DIR.parent / '.env')

# Secret Key
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-key')

# Debug Mode
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Allowed Hosts
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

# Installed Apps - TAMBAHKAN courses, ninja_extra, ninja_jwt
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ninja_extra',
    'ninja_jwt',
    'courses',  # Our main app
]

# Middleware - TAMBAHKAN WhiteNoise
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Add templates directory
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Database
import dj_database_url

if os.getenv('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=600,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
            'NAME': os.getenv('DB_NAME', 'lms_db'),
            'USER': os.getenv('DB_USER', 'postgres'),
            'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }

# Static Files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

---

### FASE 3: Database Models

#### File 7: `courses/models.py`
**Lokasi**: `lms-project/code/courses/models.py`

```python
from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    """Model untuk menyimpan data mata kuliah"""
    code = models.CharField(max_length=10, unique=True, help_text="Kode mata kuliah")
    name = models.CharField(max_length=200, help_text="Nama mata kuliah")
    description = models.TextField(blank=True, help_text="Deskripsi mata kuliah")
    credits = models.IntegerField(default=3, help_text="Jumlah SKS")
    price = models.IntegerField(default=0, help_text="Harga course")
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='courses_taught')
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='courses_instructed')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['code']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Material(models.Model):
    """Model untuk menyimpan materi pembelajaran"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200, help_text="Judul materi")
    content = models.TextField(help_text="Isi materi")
    order = models.IntegerField(default=0, help_text="Urutan materi")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Material'
        verbose_name_plural = 'Materials'
    
    def __str__(self):
        return f"{self.course.code} - {self.title}"


class Enrollment(models.Model):
    """Model untuk menyimpan data pendaftaran mahasiswa"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    grade = models.CharField(max_length=2, blank=True, null=True, help_text="Nilai (A, B, C, D, E)")
    
    class Meta:
        unique_together = ['student', 'course']
        ordering = ['-enrolled_at']
        verbose_name = 'Enrollment'
        verbose_name_plural = 'Enrollments'
    
    def __str__(self):
        return f"{self.student.username} - {self.course.code}"


class CourseMember(models.Model):
    """Model untuk menyimpan member dari course"""
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_memberships')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='members')
    roles = models.CharField(max_length=50, help_text="Role member")
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user_id', 'course']
        ordering = ['-joined_at']
    
    def __str__(self):
        return f"{self.user_id.username} - {self.course.name}"


class CourseContent(models.Model):
    """Model untuk menyimpan konten pembelajaran"""
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='contents')
    name = models.CharField(max_length=200, help_text="Nama konten")
    description = models.TextField(help_text="Deskripsi konten")
    video_url = models.URLField(blank=True, help_text="URL video")
    file_attachment = models.CharField(max_length=500, blank=True, help_text="File path")
    order = models.IntegerField(default=0, help_text="Urutan konten")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.course_id.code} - {self.name}"


class Comment(models.Model):
    """Model untuk komentar"""
    content_id = models.ForeignKey(CourseContent, on_delete=models.CASCADE, related_name='comments')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment_text = models.TextField(help_text="Isi komentar")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.user_id.username}"
```

#### File 8: `courses/admin.py`
**Lokasi**: `lms-project/code/courses/admin.py`

```python
from django.contrib import admin
from .models import Course, Material, Enrollment, CourseMember, CourseContent, Comment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'credits', 'price', 'teacher', 'created_at']
    list_filter = ['credits', 'created_at']
    search_fields = ['code', 'name', 'description']
    ordering = ['code']

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'created_at']
    list_filter = ['course', 'created_at']
    search_fields = ['title', 'content']
    ordering = ['course', 'order']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'grade', 'enrolled_at']
    list_filter = ['course', 'grade', 'enrolled_at']
    search_fields = ['student__username', 'course__name']
    ordering = ['-enrolled_at']

@admin.register(CourseMember)
class CourseMemberAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'course', 'roles', 'joined_at']
    list_filter = ['roles', 'joined_at']
    search_fields = ['user_id__username', 'course__name']

@admin.register(CourseContent)
class CourseContentAdmin(admin.ModelAdmin):
    list_display = ['name', 'course_id', 'order', 'created_at']
    list_filter = ['course_id', 'created_at']
    search_fields = ['name', 'description']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'content_id', 'created_at']
    list_filter = ['created_at']
    search_fields = ['comment_text', 'user_id__username']
```

---

### FASE 4: API Implementation

#### File 9: `courses/auth_schemas.py`
**Lokasi**: `lms-project/code/courses/auth_schemas.py`

```python
from ninja import Schema
from pydantic import field_validator, Field
from typing import Optional
import re

class RegisterSchema(Schema):
    username: str = Field(..., min_length=3, max_length=150)
    email: str
    password: str = Field(..., min_length=8)
    password_confirm: str = Field(..., min_length=8)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    
    @field_validator('email')
    def validate_email(cls, v):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, v):
            raise ValueError('Email tidak valid')
        return v
    
    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password minimal 8 karakter')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password harus mengandung angka')
        if not any(char.isupper() for char in v):
            raise ValueError('Password harus mengandung huruf besar')
        return v


class LoginSchema(Schema):
    username: str
    password: str


class TokenResponseSchema(Schema):
    access: str
    refresh: str
    user: dict


class MessageSchema(Schema):
    message: str
    detail: Optional[str] = None
```

#### File 10: `courses/throttling.py`
**Lokasi**: `lms-project/code/courses/throttling.py`

```python
from ninja.errors import HttpError
from functools import wraps
from collections import defaultdict
import time

request_tracker = defaultdict(list)

def throttle(max_requests: int = 10, time_window: int = 60):
    """Rate limiting decorator"""
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            client_ip = request.META.get('REMOTE_ADDR', 'unknown')
            current_time = time.time()
            
            # Clean old requests
            request_tracker[client_ip] = [
                req_time for req_time in request_tracker[client_ip]
                if current_time - req_time < time_window
            ]
            
            # Check limit
            if len(request_tracker[client_ip]) >= max_requests:
                raise HttpError(429, f"Rate limit exceeded")
            
            request_tracker[client_ip].append(current_time)
            return func(request, *args, **kwargs)
        
        return wrapper
    return decorator

# Predefined throttle levels
def throttle_strict(func):
    return throttle(max_requests=10, time_window=60)(func)

def throttle_moderate(func):
    return throttle(max_requests=30, time_window=60)(func)
```

#### File 11: `courses/auth_api.py`
**Lokasi**: `lms-project/code/courses/auth_api.py`

```python
from ninja import Router
from ninja.errors import HttpError
from ninja_jwt.tokens import RefreshToken
from ninja_jwt.authentication import JWTAuth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .auth_schemas import RegisterSchema, LoginSchema, TokenResponseSchema, MessageSchema
from .throttling import throttle_strict

auth_router = Router(tags=['Authentication'])
jwt_auth = JWTAuth()

@auth_router.post('/register', response={201: TokenResponseSchema, 400: MessageSchema})
@throttle_strict
def register(request, payload: RegisterSchema):
    """Register new user"""
    if payload.password != payload.password_confirm:
        raise HttpError(400, "Password tidak cocok")
    
    if User.objects.filter(username=payload.username).exists():
        raise HttpError(400, "Username sudah digunakan")
    
    if User.objects.filter(email=payload.email).exists():
        raise HttpError(400, "Email sudah terdaftar")
    
    user = User.objects.create_user(
        username=payload.username,
        email=payload.email,
        password=payload.password,
        first_name=payload.first_name or '',
        last_name=payload.last_name or ''
    )
    
    refresh = RefreshToken.for_user(user)
    
    return 201, {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
    }

@auth_router.post('/login', response={200: TokenResponseSchema, 401: MessageSchema})
@throttle_strict
def login(request, payload: LoginSchema):
    """Login user"""
    user = authenticate(username=payload.username, password=payload.password)
    
    if user is None:
        raise HttpError(401, "Username atau password salah")
    
    if not user.is_active:
        raise HttpError(401, "Akun tidak aktif")
    
    refresh = RefreshToken.for_user(user)
    
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_staff': user.is_staff
        }
    }
```

#### File 12: `courses/health.py`
**Lokasi**: `lms-project/code/courses/health.py`

```python
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    """Health check endpoint for deployment"""
    try:
        # Check database connection
        connection.ensure_connection()
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e)
        }, status=503)
```

#### File 13: `courses/api.py`
**Lokasi**: `lms-project/code/courses/api.py`

```python
from ninja import NinjaAPI, Schema
from ninja.errors import HttpError
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.tokens import RefreshToken
from ninja.pagination import paginate, PageNumberPagination
from typing import List, Optional
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Course
from .throttling import throttle
from .auth_api import auth_router

apiv1 = NinjaAPI()
auth = JWTAuth()

# Include auth router
apiv1.add_router('/auth', auth_router)

# Custom Pagination
class CustomPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

# Schemas
class CourseSchema(Schema):
    id: int
    code: str
    name: str
    description: str
    credits: int
    price: int

class CourseCreateSchema(Schema):
    code: str
    name: str
    description: str
    credits: int = 3
    price: int = 0

# Endpoints
@apiv1.get('/health')
def health(request):
    return {"status": "ok"}

@apiv1.get("/courses", response=List[CourseSchema])
@paginate(CustomPagination)
@throttle(max_requests=30, time_window=60)
def list_courses(request, search: Optional[str] = None):
    """List all courses"""
    courses = Course.objects.all()
    
    if search:
        courses = courses.filter(
            Q(code__icontains=search) |
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )
    
    return courses

@apiv1.get("/courses/{course_id}", response=CourseSchema)
def get_course(request, course_id: int):
    """Get specific course"""
    try:
        return Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        raise HttpError(404, "Course tidak ditemukan")

@apiv1.post("/courses", auth=auth, response=CourseSchema)
def create_course(request, data: CourseCreateSchema):
    """Create course - requires authentication"""
    if not request.auth.is_staff:
        raise HttpError(403, "Hanya staff yang dapat membuat course")
    
    if Course.objects.filter(code=data.code).exists():
        raise HttpError(400, "Kode course sudah digunakan")
    
    course = Course.objects.create(
        code=data.code,
        name=data.name,
        description=data.description,
        credits=data.credits,
        price=data.price,
        teacher=request.auth
    )
    
    return course
```

---

### FASE 5: URL Configuration

#### File 14: `lms_project/urls.py`
**Lokasi**: `lms-project/code/lms_project/urls.py`

```python
from django.contrib import admin
from django.urls import path, include
from courses.api import apiv1
from courses.health import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health_check'),
    path('api/v1/', apiv1.urls),
]
```

#### File 15: `courses/urls.py`
**Lokasi**: `lms-project/code/courses/urls.py`

```python
from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    # Add your web views here later
    # path('', views.home, name='home'),
]
```

---

### FASE 6: Static Files & Templates

#### File 16: `static/css/custom.css`
**Lokasi**: `lms-project/code/static/css/custom.css`

```css
/* Custom CSS for LMS */
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
}

body {
    font-family: 'Inter', sans-serif;
}

.gradient-bg {
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
}
```

#### File 17: Buat Folder Templates
```bash
# Dari lms-project/code
mkdir -p courses/templates/courses
```

---

### FASE 7: Docker Configuration

#### File 18: `dockerfile`
**Lokasi**: `lms-project/dockerfile`

```dockerfile
FROM python:3.14-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY code/ ./code/

# Set work directory to code
WORKDIR /app/code

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "lms_project.wsgi:application"]
```

#### File 19: `docker-compose.yml`
**Lokasi**: `lms-project/docker-compose.yml`

```yaml
version: '3.8'

services:
  db:
    image: postgres:14
    environment:
      POSTGRES_DB: lms_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ./code:/app/code
    ports:
      - "8000:8000"
    environment:
      - DEBUG=True
      - DB_HOST=db
      - DB_NAME=lms_db
      - DB_USER=postgres
      - DB_PASSWORD=postgres
    depends_on:
      - db

volumes:
  postgres_data:
```

---

### FASE 8: Deployment Scripts

#### File 20: `migrate.sh`
**Lokasi**: `lms-project/migrate.sh`

```bash
#!/bin/bash
cd code
python manage.py migrate --noinput
```

#### File 21: `start.sh`
**Lokasi**: `lms-project/start.sh`

```bash
#!/bin/bash
cd code
python manage.py collectstatic --noinput
gunicorn --bind 0.0.0.0:8000 --workers 3 lms_project.wsgi:application
```

#### File 22: `Procfile` (untuk Railway/Heroku)
**Lokasi**: `lms-project/Procfile`

```
web: cd code && gunicorn lms_project.wsgi:application --bind 0.0.0.0:$PORT
```

#### File 23: `railway.json`
**Lokasi**: `lms-project/railway.json`

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "dockerfile"
  },
  "deploy": {
    "startCommand": "sh start.sh",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

---

### FASE 9: Documentation

#### File 24: `README.md`
**Lokasi**: `lms-project/README.md`

```markdown
# Learning Management System

## Quick Start

### Local Development

1. Clone repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\Activate.ps1` (Windows) or `source venv/bin/activate` (Linux/Mac)
4. Install dependencies: `pip install -r requirements.txt`
5. Create database
6. Run migrations: `python manage.py migrate`
7. Create superuser: `python manage.py createsuperuser`
8. Run server: `python manage.py runserver`

### With Docker

```bash
docker-compose up --build
```

## API Documentation

Visit: http://localhost:8000/api/v1/docs
```

---

## 🗄️ Konfigurasi Database

### PostgreSQL Setup

#### Windows

```powershell
# Buka PowerShell sebagai Administrator

# Akses PostgreSQL
psql -U postgres

# Buat database
CREATE DATABASE lms_db;

# Buat user (optional, atau gunakan postgres)
CREATE USER lms_user WITH PASSWORD 'lms_password';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE lms_db TO lms_user;

# Exit
\q
```

#### Linux/Mac

```bash
# Switch to postgres user
sudo -u postgres psql

# Buat database
CREATE DATABASE lms_db;

# Buat user
CREATE USER lms_user WITH PASSWORD 'lms_password';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE lms_db TO lms_user;

# Exit
\q
```

---

## ✅ Testing Project

### Step 1: Run Migrations

```bash
# Pastikan virtual environment aktif
# Pastikan berada di folder lms-project/code

# Buat migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Output yang diharapkan:
# Operations to perform:
#   Apply all migrations: admin, auth, contenttypes, courses, sessions
# Running migrations:
#   Applying contenttypes.0001_initial... OK
#   Applying auth.0001_initial... OK
#   Applying courses.0001_initial... OK
#   ...
```

### Step 2: Create Superuser

```bash
python manage.py createsuperuser

# Input:
# Username: admin
# Email: admin@example.com
# Password: (input password minimal 8 karakter)
# Password (again): (konfirmasi password)
```

### Step 3: Run Development Server

```bash
python manage.py runserver

# Output:
# Starting development server at http://127.0.0.1:8000/
# Quit the server with CTRL-BREAK.
```

### Step 4: Test Endpoints

Buka browser dan test:

1. **Admin Panel**: http://localhost:8000/admin
   - Login dengan superuser
   
2. **Health Check**: http://localhost:8000/health/
   - Should return: `{"status": "healthy", "database": "connected"}`
   
3. **API Docs**: http://localhost:8000/api/v1/docs
   - Interactive API documentation

4. **API Test**: http://localhost:8000/api/v1/health
   - Should return: `{"status": "ok"}`

### Step 5: Test API dengan Postman/curl

```bash
# Test register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "Test1234",
    "password_confirm": "Test1234",
    "first_name": "Test",
    "last_name": "User"
  }'

# Test login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "Test1234"
  }'

# Test list courses (public)
curl http://localhost:8000/api/v1/courses
```

---

## 🚀 Deployment Preparation

### For Railway

1. **Push to GitHub**
```bash
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/username/lms-project.git
git push -u origin main
```

2. **Railway Setup**
   - Login ke Railway.app
   - New Project → Deploy from GitHub
   - Select repository
   - Add PostgreSQL service
   - Set environment variables

3. **Environment Variables di Railway**
```
SECRET_KEY=generate-new-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app.railway.app
DATABASE_URL=(auto-filled by Railway)
```

---

## 📊 Checklist Completion

Gunakan checklist ini untuk memastikan semua step sudah dilakukan:

### Phase 1: Environment Setup
- [ ] Python 3.10+ installed
- [ ] pip installed
- [ ] PostgreSQL installed
- [ ] Git installed
- [ ] Virtual environment created
- [ ] Dependencies installed

### Phase 2: Project Initialization
- [ ] Django project created
- [ ] Django app created
- [ ] .gitignore created
- [ ] .env created
- [ ] requirements.txt created

### Phase 3: Configuration
- [ ] settings.py configured
- [ ] Models created (Course, Material, Enrollment, etc)
- [ ] Admin registered
- [ ] URLs configured

### Phase 4: API Implementation
- [ ] auth_schemas.py created
- [ ] auth_api.py created
- [ ] api.py created
- [ ] throttling.py created
- [ ] health.py created

### Phase 5: Database
- [ ] PostgreSQL database created
- [ ] Migrations created
- [ ] Migrations applied
- [ ] Superuser created

### Phase 6: Testing
- [ ] Development server runs
- [ ] Admin panel accessible
- [ ] API endpoints working
- [ ] Authentication working

### Phase 7: Docker (Optional)
- [ ] dockerfile created
- [ ] docker-compose.yml created
- [ ] Docker containers running

### Phase 8: Documentation
- [ ] README.md created
- [ ] API documentation accessible
- [ ] Code commented

---

## 🎯 Summary

### Urutan File yang Harus Dibuat:

1. `.gitignore` - Ignore files for git
2. `.env` - Environment variables
3. `requirements.txt` - Python dependencies
4. Django Project (via command)
5. Django App (via command)
6. `lms_project/settings.py` - Configure Django
7. `courses/models.py` - Database models
8. `courses/admin.py` - Admin configuration
9. `courses/auth_schemas.py` - Pydantic schemas
10. `courses/throttling.py` - Rate limiting
11. `courses/auth_api.py` - Authentication API
12. `courses/health.py` - Health check
13. `courses/api.py` - Main API
14. `lms_project/urls.py` - Root URLs
15. `courses/urls.py` - App URLs
16. `static/css/custom.css` - Custom styling
17. `dockerfile` - Docker image
18. `docker-compose.yml` - Docker orchestration
19. `migrate.sh` - Migration script
20. `start.sh` - Start script
21. `Procfile` - Deployment config
22. `railway.json` - Railway config
23. `README.md` - Documentation

### Total: 23 file utama + folder structure

---

**Selamat! Anda sekarang memiliki panduan lengkap untuk setup project LMS dari nol.**
