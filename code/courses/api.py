from ninja import NinjaAPI, Schema
from ninja.errors import HttpError
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.tokens import RefreshToken
from ninja.pagination import paginate, PageNumberPagination
from pydantic import field_validator
import re
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from .models import CourseMember, CourseContent, Comment, Course
from .throttling import throttle, throttle_strict, throttle_moderate
from .auth_api import auth_router
from typing import List, Optional

apiv1 = NinjaAPI()
auth = JWTAuth()

# Include auth router
apiv1.add_router('/auth', auth_router)

# Custom Pagination
class CustomPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


@apiv1.get('/hello')
def helloApi(request):
    return "test yh ..."


@apiv1.get('calc/{nil1}/{opr}/{nil2}')
def calculator(request, nil1: int, opr: str, nil2: int):
    hasil = nil1 + nil2
    if opr == '-':
        hasil = nil1 - nil2
    elif opr == 'x':
        hasil = nil1 * nil2
    return {'nilai1': nil1, 'nilai2': nil2, 'operator': opr, 'hasil': hasil}


@apiv1.post('hello/')
def helloPost(request):
    if 'nama' in request.POST:
        return f"Selamat menikmati ya {request.POST['nama']}"
    return "Selamat tinggal dan sampai berjumpa lagi!"


@apiv1.put('users/{id}')
def userUpdate(request, id: int):
    return f"User dengan id {id} Memiliki nama asli Herdiono kemudian diganti menjadi {request.body}"


@apiv1.delete('users/{id}')
def userDelete(request, id: int):
    return f"Hapus user dengan id: {id}"


class Kalkulator(Schema):
    nil1: int
    nil2: int
    opr: str
    hasil: int = 0
    
    def calcHasil(self):
        hasil = self.nil1 + self.nil2
        if self.opr == '-':
            hasil = self.nil1 - self.nil2
        elif self.opr == 'x':
            hasil = self.nil1 * self.nil2
        return hasil


@apiv1.post('calc')
def postCalc(request, skim: Kalkulator):
    skim.hasil = skim.calcHasil()
    return skim


class Register(Schema):
    username: str
    password: str
    email: str
    first_name: str
    last_name: str
    
    @field_validator("username")
    def validate_username(cls, value):
        if len(value) < 5:
            raise ValueError("Username harus lebih dari 5 karakter")
        return value
    
    @field_validator('password')
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password harus lebih dari 8 karakter")
        pattern = r'^(?=.*[A-Za-z])(?=.*\d).+$'
        if not re.match(pattern, value):
            raise ValueError("Password harus mengandung huruf dan angka")
        return value


class UserOut(Schema):
    id: int
    username: str
    first_name: str
    last_name: str
    email: str


@apiv1.post('register/', response=UserOut)
@throttle_strict
def register(request, data: Register):
    """Endpoint untuk registrasi pengguna dengan validasi inputan:
    - username: minimal terdiri dari 5 karakter
    - password: minimal terdiri dari 8 karakter dan harus mengandung huruf dan angka
    """
    # Check if username already exists
    if User.objects.filter(username=data.username).exists():
        raise HttpError(400, "Username sudah digunakan")
    
    if User.objects.filter(email=data.email).exists():
        raise HttpError(400, "Email sudah terdaftar")
    
    newUser = User.objects.create_user(
        username=data.username,
        password=data.password,
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name
    )
    return newUser


# Authentication Endpoints
class LoginSchema(Schema):
    username: str
    password: str


class TokenOut(Schema):
    access: str
    refresh: str
    user: UserOut
    message: str


@apiv1.post('/login', response=TokenOut)
@throttle_moderate
def login(request, credentials: LoginSchema):
    """Login endpoint - returns JWT tokens"""
    user = authenticate(username=credentials.username, password=credentials.password)
    
    if user is None:
        raise HttpError(401, "Username atau password salah")
    
    if not user.is_active:
        raise HttpError(401, "Akun tidak aktif")
    
    # Create JWT tokens
    refresh = RefreshToken.for_user(user)
    
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        },
        'message': 'Login berhasil'
    }


class RefreshTokenSchema(Schema):
    refresh: str


class AccessTokenOut(Schema):
    access: str


@apiv1.post('/refresh', response=AccessTokenOut)
def refresh_token(request, data: RefreshTokenSchema):
    """Refresh access token"""
    try:
        refresh = RefreshToken(data.refresh)
        return {'access': str(refresh.access_token)}
    except Exception as e:
        raise HttpError(401, "Invalid or expired refresh token")


@apiv1.post('/logout', auth=auth)
def logout(request, data: RefreshTokenSchema):
    """Logout endpoint - blacklist refresh token"""
    try:
        token = RefreshToken(data.refresh)
        token.blacklist()
        return {'message': 'Logout berhasil'}
    except Exception:
        return {'message': 'Logout berhasil'}


@apiv1.get('/me', auth=auth, response=UserOut)
def get_current_user(request):
    """Get current authenticated user"""
    return request.auth


class UserSchema(Schema):
    id: int
    username: str
    first_name: str
    last_name: str
    email: str


@apiv1.get("/users", auth=auth, response=List[UserSchema])
@paginate(CustomPagination)
@throttle(max_requests=20, time_window=60)
def list_users(request, search: Optional[str] = None, is_staff: Optional[bool] = None):
    """List all users with pagination and filtering - requires authentication
    
    Query Parameters:
    - search: Search in username, first_name, last_name, email
    - is_staff: Filter by staff status (true/false)
    """
    users = User.objects.all()
    
    # Filtering by search
    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )
    
    # Filtering by staff status
    if is_staff is not None:
        users = users.filter(is_staff=is_staff)
    
    return users


@apiv1.get("/users/{user_id}", auth=auth, response=UserSchema)
def get_user(request, user_id: int):
    """Get specific user - requires authentication"""
    try:
        user = User.objects.get(id=user_id)
        return user
    except User.DoesNotExist:
        raise HttpError(404, "User tidak ditemukan")


class CourseSchema(Schema):
    id: int
    name: str
    description: str
    price: int
    teacher: int


@apiv1.get("/courses", response=List[CourseSchema])
@paginate(CustomPagination)
@throttle(max_requests=30, time_window=60)
def list_courses(request, search: Optional[str] = None, min_price: Optional[int] = None, max_price: Optional[int] = None, teacher_id: Optional[int] = None):
    """List all courses with pagination and filtering - public endpoint
    
    Query Parameters:
    - search: Search in course name or description
    - min_price: Minimum price filter
    - max_price: Maximum price filter
    - teacher_id: Filter by teacher ID
    """
    courses = Course.objects.all()
    
    # Filtering by search
    if search:
        courses = courses.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(code__icontains=search)
        )
    
    # Filtering by price range
    if min_price is not None:
        courses = courses.filter(price__gte=min_price)
    if max_price is not None:
        courses = courses.filter(price__lte=max_price)
    
    # Filtering by teacher
    if teacher_id is not None:
        courses = courses.filter(teacher_id=teacher_id)
    
    return [
        {
            "id": c.id,
            "name": c.name,
            "description": c.description,
            "price": c.price,
            "teacher": c.teacher.id if c.teacher else None
        }
        for c in courses
    ]


@apiv1.get("/courses/{course_id}", response=CourseSchema)
def get_course(request, course_id: int):
    """Get specific course - public endpoint"""
    try:
        c = Course.objects.get(id=course_id)
        return {
            "id": c.id,
            "name": c.name,
            "description": c.description,
            "price": c.price,
            "teacher": c.teacher.id if c.teacher else None
        }
    except Course.DoesNotExist:
        raise HttpError(404, "Course tidak ditemukan")


class CourseCreateSchema(Schema):
    code: str
    name: str
    description: str
    price: int
    credits: int = 3


@apiv1.post("/courses", auth=auth, response=CourseSchema)
def create_course(request, data: CourseCreateSchema):
    """Create new course - requires authentication (teacher only)"""
    # Only allow staff/teacher to create courses
    if not request.auth.is_staff:
        raise HttpError(403, "Hanya staff/teacher yang dapat membuat course")
    
    if Course.objects.filter(code=data.code).exists():
        raise HttpError(400, "Kode course sudah digunakan")
    
    course = Course.objects.create(
        code=data.code,
        name=data.name,
        description=data.description,
        price=data.price,
        credits=data.credits,
        teacher=request.auth,
        instructor=request.auth
    )
    
    return {
        "id": course.id,
        "name": course.name,
        "description": course.description,
        "price": course.price,
        "teacher": course.teacher.id
    }


class CourseMemberSchema(Schema):
    id: int
    user_id: int
    roles: str


@apiv1.get("/members", auth=auth, response=List[CourseMemberSchema])
@paginate(CustomPagination)
@throttle(max_requests=20, time_window=60)
def list_members(request, roles: Optional[str] = None, user_id: Optional[int] = None):
    """List all course members with pagination and filtering - requires authentication
    
    Query Parameters:
    - roles: Filter by role (teacher/student)
    - user_id: Filter by user ID
    """
    members = CourseMember.objects.all()
    
    # Filtering by role
    if roles:
        members = members.filter(roles__icontains=roles)
    
    # Filtering by user
    if user_id is not None:
        members = members.filter(user_id_id=user_id)
    
    return [
        {
            "id": m.id,
            "user_id": m.user_id.id,
            "roles": m.roles,
        }
        for m in members
    ]


class CourseContentSchema(Schema):
    id: int
    course_id: int
    name: str
    description: str
    video_url: str
    file_attachment: str


@apiv1.get("/contents", response=List[CourseContentSchema])
@paginate(CustomPagination)
@throttle(max_requests=30, time_window=60)
def list_contents(request, course_id: Optional[int] = None, search: Optional[str] = None):
    """List all course contents with pagination and filtering
    
    Query Parameters:
    - course_id: Filter by course ID
    - search: Search in content name or description
    """
    contents = CourseContent.objects.all()
    
    # Filtering by course
    if course_id is not None:
        contents = contents.filter(course_id_id=course_id)
    
    # Filtering by search
    if search:
        contents = contents.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )
    
    return [
        {
            "id": c.id,
            "course_id": c.course_id.id,
            "name": c.name,
            "description": c.description,
            "video_url": c.video_url,
            "file_attachment": c.file_attachment
        }
        for c in contents
    ]


class CommentSchema(Schema):
    id: int
    content_id: int
    member_id: int
    comment: str


@apiv1.get("/comments", response=List[CommentSchema])
@paginate(CustomPagination)
@throttle(max_requests=30, time_window=60)
def list_comments(request, content_id: Optional[int] = None, member_id: Optional[int] = None):
    """List all comments with pagination and filtering
    
    Query Parameters:
    - content_id: Filter by content ID
    - member_id: Filter by member ID
    """
    comments = Comment.objects.all()
    
    # Filtering by content
    if content_id is not None:
        comments = comments.filter(content_id_id=content_id)
    
    # Filtering by member
    if member_id is not None:
        comments = comments.filter(member_id_id=member_id)
    
    return [
        {
            "id": c.id,
            "content_id": c.content_id.id,
            "member_id": c.member_id.id,
            "comment": c.comment,
        }
        for c in comments
    ]


class CommentCreateSchema(Schema):
    content_id: int
    comment: str


@apiv1.post("/comments", auth=auth, response=CommentSchema)
def create_comment(request, data: CommentCreateSchema):
    """Create comment on course content - requires authentication"""
    try:
        content = CourseContent.objects.get(id=data.content_id)
    except CourseContent.DoesNotExist:
        raise HttpError(404, "Content tidak ditemukan")
    
    # Check if user is a member of the course
    try:
        member = CourseMember.objects.get(user_id=request.auth, course=content.course_id)
    except CourseMember.DoesNotExist:
        raise HttpError(403, "Anda bukan member dari course ini")
    
    comment = Comment.objects.create(
        content_id=content,
        member_id=member,
        comment=data.comment
    )
    
    return {
        "id": comment.id,
        "content_id": comment.content_id.id,
        "member_id": comment.member_id.id,
        "comment": comment.comment
    }
