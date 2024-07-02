from rest_framework import serializers
from user_management.models import CustomUsers
from django.core.validators import validate_email
from rest_framework.exceptions import ValidationError

# class CustomUsersSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField()
#     class Meta:
#         model = CustomUsers
#         fields = '__all__'
    
# class CustomUserSerializer(serializers.Serializer):
#     email = serializers.EmailField()

#     def validate_email(self, value):
#         try:
#             validate_email(value)
#         except ValidationError:
#             raise serializers.ValidationError("Invalid email format.")
#         return value
        
        
from rest_framework import serializers
from django.core.validators import validate_email

class CustomUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50, required=False)

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid email format.")
        return value

    def validate(self, data):
        if 'first_name' in data and len(data['first_name']) > 50:
            raise serializers.ValidationError("First name cannot exceed 50 characters.")
        
        if 'last_name' in data and len(data['last_name']) > 50:
            raise serializers.ValidationError("Last name cannot exceed 50 characters.")

        return data
