# PENJELASAN INTEGRATION DATA & DJANGO NINJA
## Sistem Manajemen Pembelajaran

---

## Daftar Isi
1. [Pendahuluan](#pendahuluan)
2. [Apa itu Django Ninja](#apa-itu-django-ninja)
3. [Integration Data dalam Project](#integration-data-dalam-project)
4. [Implementasi Django Ninja](#implementasi-django-ninja)
5. [Data Flow Architecture](#data-flow-architecture)
6. [Contoh Implementasi](#contoh-implementasi)
7. [Best Practices](#best-practices)

---

## Pendahuluan

Project ini mengimplementasikan **sistem manajemen pembelajaran** yang mengintegrasikan berbagai data dan layanan melalui **RESTful API** menggunakan **Django Ninja**. Document ini menjelaskan bagaimana data diintegrasikan antar komponen sistem dan peran Django Ninja dalam memfasilitasi komunikasi tersebut.

### Tujuan Integration Data

1. **Interoperability**: Memungkinkan berbagai client (web, mobile, third-party) mengakses data yang sama
2. **Separation of Concerns**: Memisahkan business logic dari presentation layer
3. **Scalability**: Memudahkan scaling horizontal dengan stateless API
4. **Reusability**: API endpoints dapat digunakan oleh multiple consumers

---

## Apa itu Django Ninja?

### Definisi

**Django Ninja** adalah modern web framework untuk building APIs dengan Django, terinspirasi oleh FastAPI. Framework ini menggabungkan kekuatan Django dengan type hints Python dan automatic validation menggunakan Pydantic.

### Karakteristik Utama

#### 1. **Type Safety dengan Python Type Hints**
```python
@apiv1.get("/courses/{course_id}", response=CourseSchema)
def get_course(request, course_id: int):
    # course_id automatically validated as integer
    pass
```

#### 2. **Automatic Request Validation**
Django Ninja menggunakan **Pydantic** untuk validasi otomatis:
```python
class RegisterSchema(Schema):
    username: str = Field(..., min_length=3, max_length=150)
    email: str
    password: str = Field(..., min_length=8)
    
    @field_validator('email')
    def validate_email(cls, v):
        if not re.match(email_regex, v):
            raise ValueError('Email tidak valid')
        return v
```

#### 3. **Auto-Generated Documentation**
- OpenAPI (Swagger) documentation
- Interactive API testing interface
- Accessible at `/api/v1/docs`

#### 4. **High Performance**
- Minimal overhead dibanding Django REST Framework
- Asynchronous support (optional)
- Efficient serialization

#### 5. **Developer-Friendly**
- Intuitive decorator-based routing
- Similar to FastAPI syntax
- Built-in pagination support

### Django Ninja vs Django REST Framework

| Aspek | Django Ninja | Django REST Framework |
|-------|--------------|----------------------|
| **Syntax** | Decorator-based, simple | Class-based, verbose |
| **Type Hints** | ✅ Native support | ❌ Limited |
| **Validation** | Pydantic automatic | Manual serializers |
| **Performance** | ⚡ Fast | Standard |
| **Learning Curve** | 📈 Easy | Steep |
| **Documentation** | Auto-generated OpenAPI | Manual setup |

### Komponen Django Ninja

#### 1. **NinjaAPI Instance**
```python
from ninja import NinjaAPI

apiv1 = NinjaAPI()
```

#### 2. **Schema (Pydantic Models)**
```python
from ninja import Schema

class UserSchema(Schema):
    id: int
    username: str
    email: str
```

#### 3. **Routing Decorators**
```python
@apiv1.get("/endpoint")     # GET request
@apiv1.post("/endpoint")    # POST request
@apiv1.put("/endpoint")     # PUT request
@apiv1.delete("/endpoint")  # DELETE request
```

#### 4. **Authentication**
```python
from ninja_jwt.authentication import JWTAuth

auth = JWTAuth()

@apiv1.get("/protected", auth=auth)
def protected_endpoint(request):
    return {"user": request.auth.username}
```

---

## Integration Data dalam Project

### Arsitektur Integration

Project ini mengimplementasikan **multi-layer architecture** dengan integration points berikut:

```
┌─────────────────────────────────────────────────────┐
│                  Client Layer                        │
│  (Web Browser, Mobile App, Third-party Services)    │
└─────────────────┬───────────────────────────────────┘
                  │ HTTP/HTTPS
                  │ JSON Request/Response
┌─────────────────▼───────────────────────────────────┐
│              API Gateway Layer                       │
│           (Django Ninja - /api/v1/)                  │
│  ┌─────────────────────────────────────────────┐    │
│  │  Authentication (JWT)                       │    │
│  │  Rate Limiting (Throttling)                 │    │
│  │  Input Validation (Pydantic)                │    │
│  │  Response Serialization                     │    │
│  └─────────────────────────────────────────────┘    │
└─────────────────┬───────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────┐
│            Business Logic Layer                      │
│              (Django Views & Services)               │
│  ┌─────────────────────────────────────────────┐    │
│  │  Course Management Logic                    │    │
│  │  Enrollment Processing                      │    │
│  │  Material Management                        │    │
│  │  User Authentication Logic                  │    │
│  └─────────────────────────────────────────────┘    │
└─────────────────┬───────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────┐
│           Data Access Layer (ORM)                    │
│              (Django Models)                         │
│  ┌─────────────────────────────────────────────┐    │
│  │  Course Model                               │    │
│  │  Material Model                             │    │
│  │  Enrollment Model                           │    │
│  │  User Model                                 │    │
│  │  CourseMember Model                         │    │
│  │  CourseContent Model                        │    │
│  └─────────────────────────────────────────────┘    │
└─────────────────┬───────────────────────────────────┘
                  │ SQL Queries
┌─────────────────▼───────────────────────────────────┐
│            Database Layer                            │
│              (PostgreSQL)                            │
│  ┌─────────────────────────────────────────────┐    │
│  │  courses_course                             │    │
│  │  courses_material                           │    │
│  │  courses_enrollment                         │    │
│  │  auth_user                                  │    │
│  │  courses_coursemember                       │    │
│  └─────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

### Data Integration Points

#### 1. **Client-API Integration**

**Format Data**: JSON  
**Protocol**: HTTP/HTTPS  
**Authentication**: JWT Bearer Token

**Request Format**:
```http
POST /api/v1/courses HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
    "code": "CS101",
    "name": "Introduction to Programming",
    "description": "Learn programming basics",
    "price": 1000000,
    "credits": 3
}
```

**Response Format**:
```json
{
    "id": 1,
    "name": "Introduction to Programming",
    "description": "Learn programming basics",
    "price": 1000000,
    "teacher": 2
}
```

#### 2. **API-Database Integration**

Data mengalir dari API ke database melalui **Django ORM**:

```python
# API Endpoint receives data
@apiv1.post("/courses", auth=auth)
def create_course(request, data: CourseCreateSchema):
    # Data validation by Pydantic (automatic)
    
    # Business logic validation
    if Course.objects.filter(code=data.code).exists():
        raise HttpError(400, "Kode course sudah digunakan")
    
    # ORM Integration - Save to database
    course = Course.objects.create(
        code=data.code,
        name=data.name,
        description=data.description,
        price=data.price,
        credits=data.credits,
        teacher=request.auth  # Current authenticated user
    )
    
    # Return serialized response
    return course
```

#### 3. **Cross-Model Data Integration**

Project mengintegrasikan data dari multiple models:

**Example: Course Detail dengan Related Data**
```python
@apiv1.get("/courses/{course_id}/details")
def get_course_details(request, course_id: int):
    # Get course
    course = Course.objects.get(id=course_id)
    
    # Integrate materials (One-to-Many)
    materials = course.materials.all()
    
    # Integrate enrollments (One-to-Many)
    enrollments = course.enrollments.select_related('student').all()
    
    # Integrate course members (Many-to-Many)
    members = course.members.select_related('user_id').all()
    
    return {
        "course": {
            "id": course.id,
            "name": course.name,
            "description": course.description
        },
        "materials": [
            {"id": m.id, "title": m.title} for m in materials
        ],
        "students": [
            {"id": e.student.id, "name": e.student.username} 
            for e in enrollments
        ],
        "members": [
            {"id": m.user_id.id, "role": m.roles} 
            for m in members
        ]
    }
```

#### 4. **Authentication Integration**

JWT token diintegrasikan dengan setiap request:

**Flow**:
1. User login → Generate JWT token
2. Client store token
3. Client send token in Authorization header
4. API validate token
5. API attach user object to request
6. Business logic access user via `request.auth`

```python
# Login generates token
@apiv1.post('/login')
def login(request, credentials: LoginSchema):
    user = authenticate(username=credentials.username, password=credentials.password)
    
    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)
    
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': {...}
    }

# Protected endpoint validates token
@apiv1.get('/me', auth=auth)
def get_current_user(request):
    # request.auth contains user object from JWT
    return request.auth
```

---

## Implementasi Django Ninja

### Struktur File Project

```
code/
├── lms_project/
│   └── urls.py              # Root URL configuration
└── courses/
    ├── api.py               # Main API endpoints
    ├── auth_api.py          # Authentication endpoints
    ├── auth_schemas.py      # Pydantic schemas for auth
    ├── throttling.py        # Rate limiting implementation
    └── models.py            # Django models
```

### 1. Setup Django Ninja

**File: `lms_project/urls.py`**
```python
from django.urls import path
from courses.api import apiv1

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', apiv1.urls),  # Mount Ninja API
]
```

**File: `courses/api.py`**
```python
from ninja import NinjaAPI
from ninja_jwt.authentication import JWTAuth

# Initialize API
apiv1 = NinjaAPI()
auth = JWTAuth()

# Include sub-routers
from .auth_api import auth_router
apiv1.add_router('/auth', auth_router)
```

### 2. Schema Definition dengan Pydantic

**Input Schema**:
```python
from ninja import Schema
from pydantic import field_validator, Field
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
        if not any(char.isdigit() for char in v):
            raise ValueError('Password harus mengandung angka')
        if not any(char.isupper() for char in v):
            raise ValueError('Password harus mengandung huruf besar')
        return v
```

**Output Schema**:
```python
class UserSchema(Schema):
    id: int
    username: str
    first_name: str
    last_name: str
    email: str

class TokenResponseSchema(Schema):
    access: str
    refresh: str
    user: dict
```

### 3. Endpoint Implementation

**Public Endpoint (No Auth)**:
```python
@apiv1.get("/courses", response=List[CourseSchema])
@paginate(CustomPagination)
@throttle(max_requests=30, time_window=60)
def list_courses(request, search: Optional[str] = None):
    """List all courses - public endpoint"""
    courses = Course.objects.all()
    
    if search:
        courses = courses.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )
    
    return courses
```

**Protected Endpoint (Requires Auth)**:
```python
@apiv1.post("/courses", auth=auth, response=CourseSchema)
def create_course(request, data: CourseCreateSchema):
    """Create course - requires authentication"""
    # request.auth contains authenticated user
    if not request.auth.is_staff:
        raise HttpError(403, "Only staff can create courses")
    
    course = Course.objects.create(
        code=data.code,
        name=data.name,
        teacher=request.auth
    )
    
    return course
```

### 4. Authentication Implementation

**File: `courses/auth_api.py`**
```python
from ninja import Router
from ninja_jwt.tokens import RefreshToken
from ninja_jwt.authentication import JWTAuth

auth_router = Router(tags=['Authentication'])
jwt_auth = JWTAuth()

@auth_router.post('/register', response={201: TokenResponseSchema})
@throttle_strict
def register(request, payload: RegisterSchema):
    # Validate password confirmation
    if payload.password != payload.password_confirm:
        raise HttpError(400, "Password tidak cocok")
    
    # Create user
    user = User.objects.create_user(
        username=payload.username,
        email=payload.email,
        password=payload.password
    )
    
    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)
    
    return 201, {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }

@auth_router.post('/login', response={200: TokenResponseSchema})
def login(request, payload: LoginSchema):
    user = authenticate(
        username=payload.username, 
        password=payload.password
    )
    
    if user is None:
        raise HttpError(401, "Username atau password salah")
    
    refresh = RefreshToken.for_user(user)
    
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': {...}
    }
```

### 5. Pagination Implementation

```python
from ninja.pagination import paginate, PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

@apiv1.get("/users", auth=auth, response=List[UserSchema])
@paginate(CustomPagination)
def list_users(request, search: Optional[str] = None):
    users = User.objects.all()
    
    if search:
        users = users.filter(username__icontains=search)
    
    return users
```

**Response Format**:
```json
{
    "items": [
        {"id": 1, "username": "john", "email": "john@example.com"},
        {"id": 2, "username": "jane", "email": "jane@example.com"}
    ],
    "count": 100,
    "next": "/api/v1/users?page=2",
    "previous": null
}
```

### 6. Rate Limiting (Throttling)

**File: `courses/throttling.py`**
```python
from collections import defaultdict
import time

request_tracker = defaultdict(list)

def throttle(max_requests: int = 10, time_window: int = 60):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            client_ip = request.META.get('REMOTE_ADDR')
            current_time = time.time()
            
            # Clean old requests
            request_tracker[client_ip] = [
                req_time for req_time in request_tracker[client_ip]
                if current_time - req_time < time_window
            ]
            
            # Check limit
            if len(request_tracker[client_ip]) >= max_requests:
                raise HttpError(429, "Rate limit exceeded")
            
            request_tracker[client_ip].append(current_time)
            return func(request, *args, **kwargs)
        
        return wrapper
    return decorator
```

**Usage**:
```python
@apiv1.post('register/')
@throttle_strict  # 10 requests per minute
def register(request, data: Register):
    pass

@apiv1.get('/courses')
@throttle(max_requests=30, time_window=60)  # 30 requests per minute
def list_courses(request):
    pass
```

---

## Data Flow Architecture

### Complete Request-Response Flow

```
1. CLIENT REQUEST
   ↓
   POST /api/v1/courses
   Authorization: Bearer <token>
   Body: {"code": "CS101", "name": "Programming"}

2. DJANGO MIDDLEWARE
   ↓
   - SecurityMiddleware
   - SessionMiddleware
   - CSRFMiddleware (skipped for API)
   - AuthenticationMiddleware

3. URL ROUTING
   ↓
   Django URLs → /api/v1/ → NinjaAPI → /courses

4. DJANGO NINJA PROCESSING
   ↓
   a. Authentication Check (JWTAuth)
      - Verify JWT token
      - Decode user info
      - Attach user to request.auth
   
   b. Throttling Check
      - Check request count for IP
      - Raise 429 if exceeded
   
   c. Input Validation (Pydantic)
      - Parse JSON body
      - Validate against CourseCreateSchema
      - Type checking
      - Custom validators
      - Raise 422 if invalid
   
   d. Handler Execution
      - Execute create_course function
      - Access validated data
      - Access authenticated user via request.auth

5. BUSINESS LOGIC
   ↓
   - Check permissions (is_staff)
   - Validate business rules (unique code)
   - Prepare data for database

6. DATABASE INTERACTION (ORM)
   ↓
   - Course.objects.create(...)
   - Django ORM generates SQL
   - Execute INSERT query
   - PostgreSQL stores data
   - Return Course instance

7. RESPONSE SERIALIZATION
   ↓
   - Django Ninja serializes Course
   - According to CourseSchema
   - Convert to JSON

8. HTTP RESPONSE
   ↓
   Status: 201 Created
   Body: {
       "id": 1,
       "name": "Programming",
       "price": 1000000,
       "teacher": 2
   }

9. CLIENT RECEIVES RESPONSE
   ↓
   - Parse JSON
   - Update UI
   - Store data if needed
```

### Data Integration Patterns

#### Pattern 1: Simple CRUD

```python
# CREATE
@apiv1.post("/courses")
def create(request, data: CourseSchema):
    return Course.objects.create(**data.dict())

# READ
@apiv1.get("/courses/{id}")
def read(request, id: int):
    return Course.objects.get(id=id)

# UPDATE
@apiv1.put("/courses/{id}")
def update(request, id: int, data: CourseSchema):
    course = Course.objects.get(id=id)
    for key, value in data.dict().items():
        setattr(course, key, value)
    course.save()
    return course

# DELETE
@apiv1.delete("/courses/{id}")
def delete(request, id: int):
    Course.objects.get(id=id).delete()
    return {"success": True}
```

#### Pattern 2: Nested Data Integration

```python
@apiv1.get("/courses/{id}/full")
def get_course_full(request, id: int):
    course = Course.objects.select_related('teacher').get(id=id)
    
    return {
        "course": CourseSchema.from_orm(course),
        "materials": [
            MaterialSchema.from_orm(m) 
            for m in course.materials.all()
        ],
        "enrollments": [
            EnrollmentSchema.from_orm(e) 
            for e in course.enrollments.select_related('student').all()
        ]
    }
```

#### Pattern 3: Aggregated Data

```python
from django.db.models import Count, Avg

@apiv1.get("/courses/statistics")
def course_statistics(request):
    stats = Course.objects.aggregate(
        total_courses=Count('id'),
        avg_price=Avg('price'),
        total_enrollments=Count('enrollments')
    )
    return stats
```

#### Pattern 4: Filtered Integration

```python
@apiv1.get("/my-courses", auth=auth)
def my_courses(request):
    # Integration with authentication
    user = request.auth
    
    # Get courses where user is enrolled
    enrollments = Enrollment.objects.filter(
        student=user
    ).select_related('course')
    
    return [{
        "course": CourseSchema.from_orm(e.course),
        "enrolled_at": e.enrolled_at,
        "grade": e.grade
    } for e in enrollments]
```

---

## Contoh Implementasi

### Case Study 1: User Registration Flow

**Client Side (JavaScript)**:
```javascript
async function register(userData) {
    const response = await fetch('http://api.example.com/api/v1/auth/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: userData.username,
            email: userData.email,
            password: userData.password,
            password_confirm: userData.password_confirm,
            first_name: userData.first_name,
            last_name: userData.last_name
        })
    });
    
    if (response.ok) {
        const data = await response.json();
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);
        return data;
    } else {
        const error = await response.json();
        throw new Error(error.detail);
    }
}
```

**Server Side (Django Ninja)**:
```python
@auth_router.post('/register', response={201: TokenResponseSchema, 400: MessageSchema})
@throttle_strict
def register(request, payload: RegisterSchema):
    # Automatic validation by Pydantic
    # If invalid, returns 422 with error details
    
    # Business logic validation
    if payload.password != payload.password_confirm:
        raise HttpError(400, "Password tidak cocok")
    
    if User.objects.filter(username=payload.username).exists():
        raise HttpError(400, "Username sudah digunakan")
    
    # Create user
    user = User.objects.create_user(
        username=payload.username,
        email=payload.email,
        password=payload.password,
        first_name=payload.first_name or '',
        last_name=payload.last_name or ''
    )
    
    # Generate JWT tokens
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
```

### Case Study 2: Creating Course with Materials

**Client Side**:
```javascript
async function createCourseWithMaterials(courseData) {
    // Get token from storage
    const token = localStorage.getItem('access_token');
    
    // Step 1: Create course
    const courseResponse = await fetch('http://api.example.com/api/v1/courses', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            code: courseData.code,
            name: courseData.name,
            description: courseData.description,
            price: courseData.price,
            credits: courseData.credits
        })
    });
    
    const course = await courseResponse.json();
    
    // Step 2: Create materials for the course
    for (const material of courseData.materials) {
        await fetch('http://api.example.com/api/v1/materials', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                course_id: course.id,
                title: material.title,
                content: material.content,
                order: material.order
            })
        });
    }
    
    return course;
}
```

**Server Side**:
```python
# Course creation endpoint
@apiv1.post("/courses", auth=auth, response=CourseSchema)
def create_course(request, data: CourseCreateSchema):
    if not request.auth.is_staff:
        raise HttpError(403, "Only staff can create courses")
    
    if Course.objects.filter(code=data.code).exists():
        raise HttpError(400, "Course code already exists")
    
    course = Course.objects.create(
        code=data.code,
        name=data.name,
        description=data.description,
        price=data.price,
        credits=data.credits,
        teacher=request.auth
    )
    
    return {
        "id": course.id,
        "name": course.name,
        "description": course.description,
        "price": course.price,
        "teacher": course.teacher.id
    }

# Material creation endpoint
@apiv1.post("/materials", auth=auth, response=MaterialSchema)
def create_material(request, data: MaterialCreateSchema):
    # Verify course exists
    try:
        course = Course.objects.get(id=data.course_id)
    except Course.DoesNotExist:
        raise HttpError(404, "Course not found")
    
    # Check permission (only course teacher can add materials)
    if course.teacher != request.auth:
        raise HttpError(403, "Only course teacher can add materials")
    
    material = Material.objects.create(
        course=course,
        title=data.title,
        content=data.content,
        order=data.order
    )
    
    return material
```

### Case Study 3: Student Enrollment

**Complete Flow**:

```python
@apiv1.post("/enrollments", auth=auth)
def create_enrollment(request, data: EnrollmentCreateSchema):
    # 1. Validate student (must be authenticated)
    student = request.auth
    
    # 2. Validate course exists
    try:
        course = Course.objects.get(id=data.course_id)
    except Course.DoesNotExist:
        raise HttpError(404, "Course not found")
    
    # 3. Check if already enrolled
    if Enrollment.objects.filter(student=student, course=course).exists():
        raise HttpError(400, "Already enrolled in this course")
    
    # 4. Business logic: Check prerequisites (example)
    if course.requires_prerequisite:
        completed_courses = Enrollment.objects.filter(
            student=student,
            grade__in=['A', 'B', 'C']
        ).values_list('course_id', flat=True)
        
        if course.prerequisite_id not in completed_courses:
            raise HttpError(400, "Prerequisite not met")
    
    # 5. Create enrollment
    enrollment = Enrollment.objects.create(
        student=student,
        course=course
    )
    
    # 6. Create course member record
    CourseMember.objects.create(
        user_id=student,
        course=course,
        roles='student'
    )
    
    # 7. Return response
    return {
        "id": enrollment.id,
        "student": {
            "id": student.id,
            "username": student.username
        },
        "course": {
            "id": course.id,
            "name": course.name
        },
        "enrolled_at": enrollment.enrolled_at
    }
```

---

## Best Practices

### 1. Schema Design

**✅ DO**:
```python
# Use descriptive schema names
class CourseCreateSchema(Schema):
    code: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., max_length=200)
    description: str
    price: int = Field(..., ge=0)  # Greater than or equal to 0

# Separate input and output schemas
class CourseOut(Schema):
    id: int
    code: str
    name: str
    teacher_name: str = None
```

**❌ DON'T**:
```python
# Don't use generic names
class Data(Schema):
    field1: str
    field2: int

# Don't mix input/output in one schema
class Course(Schema):
    id: int  # Output only
    password: str  # Input only - security risk!
```

### 2. Error Handling

**✅ DO**:
```python
@apiv1.post("/courses")
def create_course(request, data: CourseCreateSchema):
    try:
        course = Course.objects.create(**data.dict())
        return course
    except IntegrityError:
        raise HttpError(400, "Course code must be unique")
    except Exception as e:
        # Log the error
        logger.error(f"Error creating course: {str(e)}")
        raise HttpError(500, "Internal server error")
```

**❌ DON'T**:
```python
@apiv1.post("/courses")
def create_course(request, data: CourseCreateSchema):
    # Don't let exceptions propagate unhandled
    course = Course.objects.create(**data.dict())
    return course
```

### 3. Authentication

**✅ DO**:
```python
# Always use auth for sensitive operations
@apiv1.post("/courses", auth=auth)
def create_course(request, data: CourseCreateSchema):
    # Check permissions
    if not request.auth.is_staff:
        raise HttpError(403, "Permission denied")
    
    course = Course.objects.create(
        teacher=request.auth,
        **data.dict()
    )
    return course
```

**❌ DON'T**:
```python
# Don't skip authentication for write operations
@apiv1.post("/courses")  # No auth!
def create_course(request, data: CourseCreateSchema):
    course = Course.objects.create(**data.dict())
    return course
```

### 4. Query Optimization

**✅ DO**:
```python
@apiv1.get("/courses/{id}")
def get_course(request, id: int):
    # Use select_related for foreign keys
    course = Course.objects.select_related('teacher').get(id=id)
    
    # Use prefetch_related for reverse foreign keys
    materials = course.materials.all()
    
    return {
        "course": course,
        "teacher": course.teacher.username,
        "materials": materials
    }
```

**❌ DON'T**:
```python
@apiv1.get("/courses/{id}")
def get_course(request, id: int):
    # N+1 query problem
    course = Course.objects.get(id=id)
    
    # Each material access triggers a query
    materials = [m.title for m in course.materials.all()]
    
    return {"course": course, "materials": materials}
```

### 5. Pagination

**✅ DO**:
```python
# Always paginate list endpoints
@apiv1.get("/courses", response=List[CourseSchema])
@paginate(CustomPagination)
def list_courses(request):
    return Course.objects.all()
```

**❌ DON'T**:
```python
# Don't return all records without pagination
@apiv1.get("/courses")
def list_courses(request):
    # Could return thousands of records!
    return Course.objects.all()
```

### 6. Rate Limiting

**✅ DO**:
```python
# Apply throttling based on sensitivity
@apiv1.post("/auth/register")
@throttle_strict  # 10 requests/min
def register(request, data: RegisterSchema):
    pass

@apiv1.get("/courses")
@throttle(max_requests=30, time_window=60)
def list_courses(request):
    pass
```

### 7. Documentation

**✅ DO**:
```python
@apiv1.post("/courses", auth=auth, response=CourseSchema)
def create_course(request, data: CourseCreateSchema):
    """
    Create a new course.
    
    **Requirements:**
    - User must be authenticated
    - User must have staff permission
    - Course code must be unique
    
    **Returns:**
    - 201: Course created successfully
    - 400: Invalid data or duplicate code
    - 403: Permission denied
    """
    pass
```

### 8. Validation

**✅ DO**:
```python
class RegisterSchema(Schema):
    username: str = Field(..., min_length=3, max_length=150)
    email: str
    password: str = Field(..., min_length=8)
    
    @field_validator('email')
    def validate_email(cls, v):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', v):
            raise ValueError('Email tidak valid')
        return v
    
    @field_validator('password')
    def validate_password_strength(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password harus mengandung huruf besar')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password harus mengandung angka')
        return v
```

---

## Kesimpulan

### Keunggulan Integration dengan Django Ninja

1. **Type Safety**: Python type hints memastikan type correctness
2. **Automatic Validation**: Pydantic handles validation automatically
3. **Clear Separation**: API logic terpisah dari web views
4. **Auto Documentation**: OpenAPI docs generated automatically
5. **High Performance**: Minimal overhead dibanding alternatives
6. **Developer Experience**: Simple, intuitive API

### Integration Architecture Benefits

1. **Modularity**: Setiap component independent
2. **Scalability**: Easy to scale horizontally
3. **Flexibility**: Multiple clients dapat consume API yang sama
4. **Maintainability**: Clear structure, easy to maintain
5. **Security**: Centralized authentication & authorization

### Rekomendasi

Untuk pengembangan selanjutnya:

1. Tambahkan API versioning (`/api/v2/`)
2. Implement caching layer (Redis)
3. Add comprehensive logging
4. Setup monitoring & alerts
5. Implement API rate limiting per user
6. Add webhook support untuk event notifications
7. Consider GraphQL untuk complex queries

---

**Dokumentasi ini menjelaskan integration data dalam project LMS menggunakan Django Ninja sebagai API framework modern yang powerful, type-safe, dan developer-friendly.**
