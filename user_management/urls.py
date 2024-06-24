from django.urls import path, include
from user_management.views import LoginSignupViewset
from rest_framework.routers import DefaultRouter
from user_management import views

router = DefaultRouter()
router.register("", views.LoginSignupViewset, basename="")

urlpatterns = [
    path("", include(router.urls)),
]
