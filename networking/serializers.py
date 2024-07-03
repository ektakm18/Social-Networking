from networking.models import FriendRequest
from rest_framework import serializers
from user_management.models import CustomUsers
        
class FriendRequestViewSerializer(serializers.ModelSerializer):
    sender_email = serializers.EmailField(source='sender.email', read_only=True)
    
    class Meta:
        model = FriendRequest
        fields = ['sender_email', 'status', 'created_at']

class FriendViewSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = ['email', 'status', 'created_at']

    def get_email(self, obj):
        current_user = self.context['request'].user
        if obj.sender == current_user:
            return obj.receiver.email
        return obj.sender.email
        
class FriendRequestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FriendRequest
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUsers
        fields = ['email', 'first_name', 'last_name']