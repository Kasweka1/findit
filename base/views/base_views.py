from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.db.models import Q
import re
from base.models import Profile
from base.utils import template_pass


def login(request):
    if request.method == "POST":
        username_or_email = request.POST.get("username").strip()
        password = request.POST.get("password").strip()

        try:
            user_obj = User.objects.get(
                Q(username=username_or_email) | Q(email=username_or_email)
            )
            username = user_obj.username
        except User.DoesNotExist:
            username = username_or_email

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            

            if user.is_superuser:
                return redirect("admin_dashboard")  
           
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
        email = request.POST.get("email", "").strip()
        mobile_no = request.POST.get("mobile_no")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        errors = []
        context = {}

        # Password match check
        if password != confirm_password:
            errors.append("Passwords do not match.")

        if len(username) != 10 or not username.isdigit():
            errors.append("Incorrect Username. It should be a comuter number (e.g., 2021000001)")

                
        pattern = r"^[^@]+@([a-zA-Z0-9-]+\.)*unza\.zm$"

        if not re.fullmatch(pattern, email, flags=re.IGNORECASE):
            errors.append("Email must be a valid UNZA email (e.g., user@unza.zm, user@cs.unza.zm)")

        # Username exists
        if User.objects.filter(username=username).exists():
            errors.append("Username already taken.")

        # Email exists
        if User.objects.filter(email=email).exists():
            errors.append("Email is already registered.")


        if errors:
            context["errors"] = errors
            # Keep entered values except password
            context.update(
                {
                    "first_name": first_name,
                    "last_name": last_name,
                    "username": username,
                    "email": email,
                    "mobile_no": mobile_no,
                }
            )
            return render(request, template_pass("base", "register"), context)

        # Create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password, 
            first_name=first_name,
            last_name=last_name,
        )

        profile = Profile.objects.create(
            user=user,
            mobile_number=mobile_no,
        )
        profile.save()

        messages.success(
            request, "Your account has been created successfully! Please log in."
        )
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
