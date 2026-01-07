from ninja import Router
from ninja.errors import HttpError
from ninja_jwt.tokens import RefreshToken
from ninja_jwt.authentication import JWTAuth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from .auth_schemas import RegisterSchema, LoginSchema, TokenResponseSchema, MessageSchema
from .throttling import throttle_strict

auth_router = Router(tags=['Authentication'])
jwt_auth = JWTAuth()


@auth_router.post('/register', response={201: TokenResponseSchema, 400: MessageSchema})
@throttle_strict
def register(request, payload: RegisterSchema):
    """
    Register new user and return JWT tokens
    """
    # Validate password confirmation
    if payload.password != payload.password_confirm:
        raise HttpError(400, "Password dan konfirmasi password tidak cocok")
    
    # Check if username exists
    if User.objects.filter(username=payload.username).exists():
        raise HttpError(400, "Username sudah digunakan")
    
    # Check if email exists
    if User.objects.filter(email=payload.email).exists():
        raise HttpError(400, "Email sudah terdaftar")
    
    try:
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
    except IntegrityError as e:
        raise HttpError(400, f"Error creating user: {str(e)}")


@auth_router.post('/login', response={200: TokenResponseSchema, 401: MessageSchema})
@throttle_strict
def login(request, payload: LoginSchema):
    """
    Login user and return JWT tokens
    """
    # Authenticate user
    user = authenticate(username=payload.username, password=payload.password)
    
    if user is None:
        raise HttpError(401, "Username atau password salah")
    
    if not user.is_active:
        raise HttpError(401, "Akun tidak aktif")
    
    # Generate JWT tokens
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


@auth_router.post('/refresh', response={200: dict, 400: MessageSchema})
def refresh_token(request, refresh_token: str):
    """
    Refresh access token using refresh token
    """
    try:
        refresh = RefreshToken(refresh_token)
        return {
            'access': str(refresh.access_token)
        }
    except Exception as e:
        raise HttpError(400, f"Invalid refresh token: {str(e)}")


@auth_router.post('/logout', response={200: MessageSchema})
def logout(request):
    """
    Logout endpoint (client should delete tokens)
    """
    return {
        'message': 'Logout berhasil',
        'detail': 'Silakan hapus token dari client'
    }


@auth_router.get('/verify', auth=jwt_auth, response={200: dict, 401: MessageSchema})
def verify_token(request):
    """
    Verify JWT token and return user info
    """
    user = request.auth
    return {
        'valid': True,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_staff': user.is_staff
        }
    }
