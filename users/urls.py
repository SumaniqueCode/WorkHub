# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.profile_update, name="profile-update"),
]
