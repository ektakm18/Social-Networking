from django.utils import timezone
import email
from networking.serializer import FriendRequestSerializer, FriendRequestViewSerializer
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
# from rest_framework import status
import secrets 
import string
from user_management.models import CustomUsers 
from networking.models import FriendRequest
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
# from user_management.serializer import LoginSignupSerializer
from rest_framework.permissions import IsAuthenticated
from user_management.utils import custom_token_verification
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

class FriendRequestsViewset(GenericViewSet):
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['POST'])
    def send_request(self, request):
        current_user = custom_token_verification(request)
        # print("currrent", current_user['id'])
        
        to_request = (request.data.get('to_request', None)).strip()
        if not to_request:
            return Response({
                'error': 'User email is required to send friend request'}, status=400)
        if to_request == current_user['email']:
            return Response({
                'error': 'User email cannot be same as logged in user'}, status=400)

        try: 
            to_request_obj = CustomUsers.objects.get(email=to_request.lower())
            # print(to_request_obj.id)
        except CustomUsers.DoesNotExist:
            raise ValidationError({
                'error': 'User email does not exist'
            })
        
        # Check for requests sent in the last minute
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        recent_requests_count = FriendRequest.objects.filter(
            sender=current_user['id'],
            created_at__gte=one_minute_ago
        ).count()

        if recent_requests_count >= 3:
            return Response({'error': 'You can only send 3 friend requests per minute'}, status=429)
        
        # Fetch all relevant friend requests in a single query
        friend_requests = FriendRequest.objects.filter(
            Q(sender=current_user['id'], receiver=to_request_obj.id) |
            Q(sender=to_request_obj.id, receiver=current_user['id'])
        )
        
        if friend_requests.filter(status='pending').exists():
            return Response({'message': 'Friend request is already pending.'})
        elif friend_requests.filter(status='accepted').exists():
            return Response({'message': 'You both are already Friends.'})

        friend_request_data = {
            'sender': current_user['id'],
            'receiver': to_request_obj.id
        }
        serializer = FriendRequestSerializer(data=friend_request_data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Friend request sent!',
                'data': serializer.data}, status=201)
        else:
            return Response(serializer.errors, status=400) 


    @action(detail=False, methods=['get'])
    def list_pending_friend_request(self, request):
        """Lists the received friend requests which are pending"""
        current_user = custom_token_verification(request)
        
        friend_request = FriendRequest.objects.filter(receiver=current_user['id'], status='pending').order_by('created_at')
        serializer = FriendRequestViewSerializer(friend_request, many=True)
        # print("friendss", serializer.data)
        
        return Response(serializer.data, status=200)
    
    @action(detail=False, methods=['get'])
    def list_friends(self, request):
        """Lists the received friend requests which are pending"""
        current_user = custom_token_verification(request)
        
        # friend_request = FriendRequest.objects.filter(receiver=current_user['id'], status='accepted').order_by('created_at')
        friend_requests = FriendRequest.objects.filter(
                                Q(sender=current_user['id'], status='accepted') | Q(receiver=current_user['id'], status='accepted')
                            ).order_by('created_at')
        serializer = FriendRequestViewSerializer(friend_requests, many=True)
        # print("friendss", serializer.data)
        
        return Response(serializer.data, status=200)
    
    @action(detail=False, methods=['put'])
    def respond_friend_request(self, request):
        """Respond to a pending friend request accept/reject"""
        current_user = custom_token_verification(request)
        
        from_request = ((request.data.get('from_request', None)).strip()).lower()
        status = (request.data.get('status', None)).strip()
        
        if not from_request:
            return Response({'error': 'User email is required to respond to the friend request'}, status=400)
        if not status:
            return Response({'error': 'Friend request status is required'}, status=400)
        elif status not in ['accept', 'reject']:
            return Response({'error': 'Friend request status can only be accept/reject'}, status=400)
            
        if from_request == current_user['email']:
            return Response({
                'error': 'User email cannot be same as logged in user'}, status=400)
        try: 
            from_request_obj = CustomUsers.objects.get(email=from_request)
        except CustomUsers.DoesNotExist:
            raise ValidationError({
                'error': 'User email does not exist'
            })
        
        try:
            friend_request = FriendRequest.objects.get(sender=from_request_obj.id, receiver=current_user['id'], status='pending')
        except FriendRequest.DoesNotExist:
            return Response({'error': 'Pending friend request not found'}, status=400)
        
        if status == 'accept':
            friend_request.status = 'accepted'
        elif status == 'reject':
            friend_request.status = 'rejected'
            
        friend_request.updated_at = timezone.now()
        friend_request.save()
            
        return Response({
            'message': 'Friend request successfully {}'.format(status),
            'data': FriendRequestViewSerializer(friend_request).data
            }, status=200)
        