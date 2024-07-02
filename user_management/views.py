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
from user_management.serializers import CustomUserSerializer, LoginEmailValidationSerializer

class LoginSignupViewset(GenericViewSet):
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def sign_up(self, request, *args, **kwargs):
        """User sign up for social networking"""
        
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        first_name = request.data.get('first_name', None)
        last_name = request.data.get('last_name', "")
        
        if not email or not first_name:
            raise ValidationError({
                'error': 'email & first_name is required for SignUp'})    
        
        if last_name:
            last_name = last_name.strip()
            
        if password:
            password = password.strip()
            
        if last_name:
            raise ValidationError({'error': 'Last name cannot exceed 50 characters.'})
        
        email = email.strip()
        first_name = first_name.strip()
        
        serializer = CustomUserSerializer(data={
                    'email': email,
                    'first_name': first_name,
                    })
        serializer.is_valid(raise_exception=True)
        
        # Retrieve validated data
        validated_data = serializer.validated_data
        email = validated_data['email']
        first_name = validated_data['first_name']
        # last_name = validated_data.get('last_name', "")
    
        if not password:
            alphabet = string.ascii_letters + string.digits 
            password = ''.join(secrets.choice(alphabet) for i in range(10)) 
            
        try:     
            user = CustomUsers(email=email.lower(), first_name=first_name, last_name=last_name)
            user.set_password(password)
            user.save()
            return Response({
                'message': 'You are succesfully signed up.',
                'email': email,
                'password': password}, status=201)

        except IntegrityError:
            return Response({'error': 'A user with this email already exists.'}, status=400)
        except Exception as e:
            return Response({
                'error': str(e)}, status=500)
            
    @action(detail=False, methods=['post'])
    def login(self, request, *args, **kwargs):
        """Login with email and password"""
        
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        
        if not email or not password:
            raise ValidationError({'error': 'email & password are required!'})

        email = email.strip()
        password =  password.strip()
        
        serializer = LoginEmailValidationSerializer(data={
                    'email': email,
                    })
        serializer.is_valid(raise_exception=True)
        
        # Retrieve validated data
        validated_data = serializer.validated_data
        email = validated_data['email']
        
        try:
            user_obj = CustomUsers.objects.get(email=email.lower())
        except CustomUsers.DoesNotExist:
            raise ValidationError({
                'error': 'Invalid email or password.'
            })
            
        if user_obj.check_password(password):
            refresh = RefreshToken.for_user(user_obj)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            return Response({
                'message': 'Login successful!',
                'access_token': access_token,
                'refresh_token': refresh_token}, status=200)
        return Response({'error': 'User password does not match.'}, status=401)
    
