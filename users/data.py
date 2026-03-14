import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
django.setup()

from django.contrib.auth.models import User
from users.models import Profile
from skills.models import Skill

# Sample users data
users_data = [
    {
        'first_name': 'Andrew',
        'last_name': 'Smith',
        'role': 'JobSeeker',
        'position': 'Frontend Developer',
        'summary': 'Experienced Frontend Developer specializing in React and modern web technologies. Passionate about creating responsive UIs.',
        'address': 'Kathmandu, Bagmati, Nepal',
        'phone': '9841234567',
        'nationality': 'Nepali',
        'gender': 'Male',
        'skills': ['React', 'JavaScript', 'HTML', 'CSS', 'Tailwind CSS'],
        'preferred_job_type': 'Full Time',
        'preferred_work_mode': 'Hybrid',
    },
    {
        'first_name': 'Sarah',
        'last_name': 'Johnson',
        'role': 'JobSeeker',
        'position': 'Backend Developer',
        'summary': 'Backend Developer proficient in Python/Django and database design. Focus on scalable APIs and secure authentication.',
        'address': 'Lalitpur, Bagmati, Nepal',
        'phone': '9812345678',
        'nationality': 'Nepali',
        'gender': 'Female',
        'skills': ['Python', 'Django', 'PostgreSQL', 'REST API', 'Docker'],
        'preferred_job_type': 'Full Time',
        'preferred_work_mode': 'Remote',
    },
    {
        'first_name': 'Michael',
        'last_name': 'Chen',
        'role': 'JobSeeker',
        'position': 'Full Stack Developer',
        'summary': 'Versatile Full Stack Developer with expertise in MERN stack and DevOps practices.',
        'address': 'Pokhara, Gandaki, Nepal',
        'phone': '9823456789',
        'nationality': 'Nepali',
        'gender': 'Male',
        'skills': ['React', 'Node.js', 'MongoDB', 'Express.js', 'AWS'],
        'preferred_job_type': 'Full Time',
        'preferred_work_mode': 'Hybrid',
    },
    {
        'first_name': 'Lisa',
        'last_name': 'Brown',
        'role': 'JobSeeker',
        'position': 'Data Scientist',
        'summary': 'Data Scientist skilled in ML models, statistical analysis and data visualization.',
        'address': 'Biratnagar, Koshi, Nepal',
        'phone': '9834567890',
        'nationality': 'Nepali',
        'gender': 'Female',
        'skills': ['Python', 'Machine Learning', 'Pandas', 'Scikit-learn', 'Tableau'],
        'preferred_job_type': 'Full Time',
        'preferred_work_mode': 'Remote',
    },
    {
        'first_name': 'David',
        'last_name': 'Wilson',
        'role': 'Recruiter',
        'position': 'Technical Recruiter',
        'summary': 'Recruiter specializing in IT talent acquisition for tech companies.',
        'address': 'Kathmandu, Nepal',
        'phone': '9845678901',
        'nationality': 'Nepali',
        'gender': 'Male',
        'skills': ['Recruitment', 'Talent Acquisition', 'Interviewing', 'CRM'],
        'preferred_job_type': 'Full Time',
        'preferred_work_mode': 'On-site',
    },
    {
        'first_name': 'Emma',
        'last_name': 'Davis',
        'role': 'Recruiter',
        'position': 'HR Manager',
        'summary': 'HR professional with experience in talent management and employee relations.',
        'address': 'Lalitpur, Nepal',
        'phone': '9856789012',
        'nationality': 'Nepali',
        'gender': 'Female',
        'skills': ['Human Resource Management', 'Employee Relations', 'Performance Management'],
        'preferred_job_type': 'Full Time',
        'preferred_work_mode': 'Hybrid',
    },
    {
        'first_name': 'Raj',
        'last_name': 'Sharma',
        'role': 'JobSeeker',
        'position': 'DevOps Engineer',
        'summary': 'DevOps Engineer expert in CI/CD pipelines, cloud infrastructure and containerization.',
        'address': 'Butwal, Lumbini, Nepal',
        'phone': '9867890123',
        'nationality': 'Nepali',
        'gender': 'Male',
        'skills': ['Docker', 'Kubernetes', 'AWS', 'Jenkins', 'Terraform'],
        'preferred_job_type': 'Full Time',
        'preferred_work_mode': 'Remote',
    },
    {
        'first_name': 'Priya',
        'last_name': 'Thapa',
        'role': 'JobSeeker',
        'position': 'UI/UX Designer',
        'summary': 'Creative UI/UX Designer focused on user-centered design and prototyping.',
        'address': 'Kathmandu, Nepal',
        'phone': '9878901234',
        'nationality': 'Nepali',
        'gender': 'Female',
        'skills': ['Figma', 'Adobe XD', 'UI/UX Design', 'User Research'],
        'preferred_job_type': 'Part Time',
        'preferred_work_mode': 'Remote',
    },
    {
        'first_name': 'admin',
        'last_name': 'admin',
        'role': 'Admin',
        'position': 'System Administrator',
        'summary': 'Platform administrator with full access.',
        'address': 'Kathmandu, Nepal',
        'phone': '9889012345',
        'nationality': 'Nepali',
        'gender': 'Male',
        'skills': [],
        'preferred_job_type': '',
        'preferred_work_mode': '',
    },
]

# Create users and profiles
created_users = 0
created_profiles = 0

for data in users_data:
    username = data['first_name'].lower()
    email = f"{username}@gmail.com"
    
    # Create or get user
    user, user_created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': email,
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'is_active': True,
        }
    )
    
    if user_created:
        user.set_password('Test@1234')
        user.save()
        created_users += 1
    
    # Create profile
    profile, profile_created = Profile.objects.get_or_create(
        user=user,
        defaults={
            'position': data['position'],
            'summary': data['summary'],
            'address': data['address'],
            'phone': data['phone'],
            'nationality': data['nationality'],
            'gender': data['gender'],
            'role': data['role'],
            'profile_image': None,
            'search_vector': None,
            'preferred_job_type': data['preferred_job_type'],
            'preferred_work_mode': data['preferred_work_mode'],
        }
    )
    
    if profile_created:
        created_profiles += 1
    
    # Add skills
    for skill_name in data['skills']:
        skill, _ = Skill.objects.get_or_create(name=skill_name)
        profile.skills.add(skill)

print(f"Created/Updated {created_users} users, {created_profiles} profiles.")
