from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.db.models import Q

from base.models import Profile
from base.utils import template_pass


def login(request):
    if request.method == "POST":
        username_or_email = request.POST.get("username").strip()
        password = request.POST.get("password").strip()

        try:
            user_obj = User.objects.get(Q(username=username_or_email) | Q(email=username_or_email))
            username = user_obj.username
        except User.DoesNotExist:
            username = username_or_email 

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect("landing") 
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            
    context = {}
    return render(request, template_pass("base", "login"), context)


def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        mobile_no = request.POST.get("mobile_no")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        errors = []

        # Password match check
        if password != confirm_password:
            errors.error("Passwords do not match.")

        # Username exists
        if User.objects.filter(username=username).exists():
            errors.error("Username already taken.")

        # Email exists
        if User.objects.filter(email=email).exists():
            errors.error("Email is already registered.")

        if errors:
            context["errors"] = errors
            # Keep entered values except password
            context.update({
                "first_name": first_name,
                "last_name": last_name,
                "username": username,
                "email": email,
                "mobile_no": mobile_no,
            })
            return render(request, "base/register.html", context)
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.save()
        
        profile = Profile.objects.create(
            user=user,
            mobile_number=mobile_no,
        )
        profile.save()
        
        messages.success(request, "Your account has been created successfully! Please log in.")
        return redirect("login")
    
    context = {}
    return render(request, template_pass("base", "register"), context)



def logout_view(request):
    logout(request)
    storage = messages.get_messages(request)
    for _ in storage:
        pass
    
    messages.info(request, "You have been logged out successfully.")
    return redirect("login")
