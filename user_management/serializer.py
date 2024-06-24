from rest_framework import serializers
from user_management.models import CustomUsers

class CustomUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUsers
        fields = '__all__'
    