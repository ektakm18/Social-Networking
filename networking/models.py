from ast import Delete
from django.db import models
import uuid 
from user_management.models import CustomUsers
from social_networking.models import BaseModelCustom

class FriendRequest(BaseModelCustom):
    status_choices = (
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected")
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(CustomUsers, related_name='sent_request', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUsers, related_name='received_request', on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=status_choices, default="pending")
    
    class Meta:
        unique_together = ('sender', 'receiver')