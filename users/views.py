# accounts/views.py (registration)
from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib import messages
from .forms import UserRegistrationForm, ProfileForm
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(request, "Registration successful")
            return redirect("/auth/log-in")

        else:
            print(user_form.errors)
            print(profile_form.errors)

    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()

    return render(request, "pages/users/register.html", {
        "user_form": user_form,
        "profile_form": profile_form,
    })


@login_required
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, "pages/users/profile.html", {"profile": profile})


@login_required
def profile_update(request):
    user = request.user
    profile = user.profile
    if request.method == "POST":
        user_form = UserRegistrationForm(
            request.POST, instance=user
        ) 
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
    else:
        user_form = UserRegistrationForm(instance=user)
        profile_form = ProfileForm(instance=profile)
    return render(
        request,
        "pages/users/profile_update.html",
        {"user_form": user_form, "profile_form": profile_form},
    )
