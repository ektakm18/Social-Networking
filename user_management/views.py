from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db import IntegrityError
import secrets 
import string
from user_management.models import CustomUsers 
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class LoginSignupViewset(GenericViewSet):
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def sign_up(self, request, *args, **kwargs):
        """User sign up for social networking"""
        
        email = (request.data.get('email', None)).strip()
        password = (request.data.get('password', None)).strip()
        first_name = (request.data.get('first_name', None)).strip()
        last_name = (request.data.get('last_name', "")).strip()
        
        if len(email) > 255:
            raise ValidationError({'error': 'Email is too long.'})
        if len(first_name) > 50:
            raise ValidationError({'error': 'First name is too long.'})
        if len(last_name) > 50:
            raise ValidationError({'error': 'Last name is too long.'})
        
        if not email:
            raise ValidationError({
                'error': 'email is required for SignUp'})    
        if not first_name:
            raise ValidationError({
                'error': 'First name is required for SignUp'
            })
        if not password:
            # print("inside pass")
            alphabet = string.ascii_letters + string.digits 
            password = ''.join(secrets.choice(alphabet) for i in range(10)) 
        # print("password", password)
        try:     
            user = CustomUsers(email=email.lower(), first_name=first_name, last_name=last_name)
            user.set_password(password)
            user.save()
            return Response({
                'message': 'Welcome! You are succesfully signed up.',
                'email': email,
                'password': password}, status=201)

        except IntegrityError:
            return Response({'error': 'A user with this email already exists.'}, status=400)
        except Exception as e:
            print("inside2")
            return Response({
                'error': str(e)}, status=500)
            
    @action(detail=False, methods=['post'])
    def login(self, request, *args, **kwargs):
        """Login with email and password"""
        
        email = (request.data.get('email', None)).strip()
        password = (request.data.get('password', None)).strip()
        
        if not email or not password:
            raise ValidationError({'error': 'email & password are required!'})
        
        # user = authenticate(request, email=email, password=password)
        try:
            user_obj = CustomUsers.objects.get(email=email.lower())
        except CustomUsers.DoesNotExist:
            raise ValidationError({
                'error': 'Invalid email or password.'
            }, status=401)
            
        if user_obj.check_password(password):
            refresh = RefreshToken.for_user(user_obj)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            return Response({
                'message': 'Login successful!',
                'access_token': access_token,
                'refresh_token': refresh_token}, status=200)
        return Response({'error': 'User password does not match.'}, status=401)
    
