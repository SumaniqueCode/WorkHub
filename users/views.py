from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from skills.models import Skill
from .models import Profile
from .forms import *
from .utils import calculate_total_experience

def register(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            messages.success(request, "Registration successful. Please login to complete your profile.")
            return redirect("/users/login")
    else:
        user_form = UserRegistrationForm()
    return render(request, "pages/users/register.html", {"user_form": user_form})


def login_user(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    errors = {}
    username = ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        check_user = User.objects.filter(username=username).exists() 
        
        if check_user:
            authenticated_user = authenticate(request, username=username, password=password)
            if authenticated_user:
                login(request, authenticated_user)
                messages.success(request, "You have successfully logged in")
                return redirect('/dashboard')
            else:
                messages.error(request, "Invalid Password!")
                errors['password'] = "Invalid Password!" 
        else:
            messages.error(request, "User does not exist")
            errors['username'] = "User does not exist."       
        if errors:
            return render(request, 'pages/users/login.html', {'errors': errors}) 
    
    return render(request, 'pages/users/login.html', {'errors': errors, 'username': username})

def logoutUser(request):
    logout(request)
    messages.success(request, "User logged out successfully!")
    return redirect('/')

@login_required(login_url='/users/login')
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    skills = Skill.objects.filter(is_active=True).values("id", "name")
    skills_ids_str = ','.join(str(s.id) for s in profile.skills.all())
    experience_duration = calculate_total_experience(profile.experiences.all())
    return render(request, "pages/users/profile.html", {"profile": profile,"experience_duration":experience_duration, "skills_ids_str": skills_ids_str, "skills": list(skills)})

@login_required(login_url='/users/login')
def profile_update(request):
    user = request.user
    profile = user.profile
    
    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if profile_form.is_valid() and user_form.is_valid():
            profile = profile_form.save(commit=False)
            user = user_form.save(commit=False)
            user.save()
            profile.user = user
            profile.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
    else:
        profile_form = ProfileForm(instance=profile)
        user_form = UserUpdateForm(instance=user)
        return render(request, "pages/users/profile_update.html", {
            "profile_form": profile_form,
            "user_form": user_form,
            "profile": profile,
        })
    
@login_required(login_url='/users/login')
def add_skill(request):
    profile = request.user.profile
    if request.method == "POST":
        skills_str = request.POST.get("skills", "")
        skill_ids = [int(x) for x in skills_str.split(",") if x.isdigit()]
        profile.skills.set(Skill.objects.filter(id__in=skill_ids))
        messages.success(request, "Skills updated successfully.")
        return redirect("profile")
    else:
        return redirect("profile")

@login_required(login_url='/users/login')
def add_experience(request):
    if request.method == "POST":
        form = ExperienceForm(request.POST)
        if form.is_valid():
            exp = form.save(commit=False)
            exp.profile = request.user.profile
            exp.save()
            messages.success(request, "Experience added successfully.")
            return redirect("profile")
    else:
        form = ExperienceForm()
    return render(request, "pages/users/profile_form.html", {"form": form, "page_title": "Add Experience", "page_subtitle": "Add your work experience details."})

@login_required(login_url='/users/login')
def add_education(request):
    if request.method == "POST":
        form = EducationForm(request.POST)
        if form.is_valid():
            edu = form.save(commit=False)
            edu.profile = request.user.profile
            edu.save()
            messages.success(request, "Education added successfully.")
            return redirect("profile")
    else:
        form = EducationForm()
    return render(request, "pages/users/profile_form.html", {"form": form, "page_title": "Add Education", "page_subtitle": "Add your educational qualifications."})

@login_required(login_url='/users/login')
def add_certification(request):
    if request.method == "POST":
        form = CertificationForm(request.POST)
        if form.is_valid():
            cert = form.save(commit=False)
            cert.profile = request.user.profile
            cert.save()
            messages.success(request, "Certification added successfully.")
            return redirect("profile")
    else:
        form = CertificationForm()
    return render(request, "pages/users/profile_form.html", {"form": form, "page_title": "Add Certification", "page_subtitle": "Add your professional certifications."})

@login_required(login_url='/users/login')
def add_social_link(request):
    if request.method == "POST":
        form = SocialLinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.profile = request.user.profile
            link.save()
            messages.success(request, "Social link added successfully.")
            return redirect("profile")
    else:
        form = SocialLinkForm()
    return render(request, "pages/users/profile_form.html", {"form": form, "page_title": "Add Social Link", "page_subtitle": "Add your social media or professional links."})


@login_required(login_url='/users/login')
def add_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.profile = request.user.profile
            project.save()
            messages.success(request, "Project added successfully.")
            return redirect("profile")
    else:
        form = ProjectForm()
    return render(request, "pages/users/profile_form.html", {"form": form, "page_title": "Add Project", "page_subtitle": "Add your personal or professional projects."})

@login_required(login_url='/users/login')
def view_resume(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    experience_duration = calculate_total_experience(profile.experiences.all())
    return render(request, "pages/users/resume.html", {"profile": profile, "experience_duration": experience_duration})