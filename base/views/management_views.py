from django.shortcuts import redirect, render

from base.models import Category, ClaimRequest, ItemPost, Profile
from base.utils import template_pass


def admin_dashboard(request):
    items = ItemPost.objects.all()
    categories = Category.objects.all()
    claims = ClaimRequest.objects.all()
    profiles = Profile.objects.all()
    
    context = {
        "items": items,
        "categories": categories,
        "claims": claims,
        "profiles": profiles,
    }
    return render(request,  template_pass("management", "admin_dashboard"), context)


def categories_management(request):
    categories = Category.objects.all()
    
    if request.method == "POST":
        category_name = request.POST.get("category_name") 
        description = request.POST.get("description")

        if category_name:
            Category.objects.create(
                name=category_name,
                description=description
            )
        return redirect("categories_management") 

    context = {
        "categories": categories,
    }
    return render(request, template_pass("management", "categories"), context)