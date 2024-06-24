from django.urls import path, include
from user_management.views import LoginSignupViewset
from rest_framework.routers import DefaultRouter
from networking import views

router = DefaultRouter()
router.register("", views.FriendRequestsViewset, basename="")

urlpatterns = [
    path("", include(router.urls)),
]
