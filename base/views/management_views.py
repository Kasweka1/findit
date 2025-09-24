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


def items_posted(request):
    items = ItemPost.objects.all()
    
    context = {
        "items": items,
    }
    return render(request, template_pass("management", "items_posted"), context)


def item_detail(request, item_id):
    item = ItemPost.objects.get(id=item_id)
    
    context = {
        "item": item,
    }
    return render(request, template_pass("management", "item_detail"), context)


def claim_management(request):
    claims = ClaimRequest.objects.all()
    
    context = {
        "claims": claims,
    }
    return render(request, template_pass("management", "claims_management"), context)


def user_management(request):
    profiles = Profile.objects.all()
    
    context = {
        "profiles": profiles,
    }
    return render(request, template_pass("management", "user_management"), context)