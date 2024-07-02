from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from user_management.models import CustomUsers
from rest_framework.exceptions import ValidationError
import uuid
from user_management.serializers import CustomUsersSerializer

def custom_token_verification(request):
    """Function to verify token and return user_id"""
    
    auth_header = request.headers.get('Authorization')
    # print("auth_header", auth_header)
    if not auth_header or not auth_header.startswith('Bearer '):
        raise AuthenticationFailed('Invalid authorization header')
    
    token = auth_header.split()[1]
    
    try:
        authentication_data = JWTAuthentication().authenticate(request)
        user_id_str = authentication_data[1].get('user_id', None)
        if user_id_str:
            user_id = uuid.UUID(user_id_str)
        else:
            raise AuthenticationFailed('User ID not found in token data')
        user_instance = CustomUsers.objects.get(id=user_id)
        user_data = CustomUsersSerializer(user_instance).data
        return user_data
    except CustomUsers.DoesNotExist:
        raise ValidationError({
                'error': 'User email does not exist.'
            }, status=401)
    except Exception as e:
        raise AuthenticationFailed('Invalid token')
