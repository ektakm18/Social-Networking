from networking.models import FriendRequest
from rest_framework import serializers
from user_management.models import CustomUsers
        
class FriendRequestViewSerializer(serializers.ModelSerializer):
    sender_email = serializers.EmailField(source='sender.email', read_only=True)
    
    class Meta:
        model = FriendRequest
        fields = ['sender_email', 'status', 'created_at']
        
class FriendRequestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FriendRequest
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUsers
        fields = ['id', 'email', 'name']