
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.shortcuts import redirect

def template_pass(folder, file):
    return f"base/{folder}/{file}.html"




def superuser_required(view_func):
    """
    Restrict a view to superusers only.
    Redirects to login if not authenticated,
    or to landing page with a message if not a superuser.
    """
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Redirect to login page
            return redirect("login")

        if not request.user.is_superuser:
            messages.error(request, "You do not have permission to access this page.")
            return redirect("login")

        return view_func(request, *args, **kwargs)

    return _wrapped_view