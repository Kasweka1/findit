from django.shortcuts import redirect, render

from base.models import Category, ClaimRequest, ItemPost, Profile
from base.utils import template_pass, superuser_required



@superuser_required
def admin_dashboard(request): 
    user = request.user
    items = ItemPost.objects.all()
    categories = Category.objects.all()
    claims = ClaimRequest.objects.all()
    profiles = Profile.objects.all()
    
    context = {
        "items": items,
        "categories": categories,
        "claims": claims,
        "profiles": profiles,
         "user":user,
    }
    return render(request,  template_pass("management", "admin_dashboard"), context)



@superuser_required
def categories_management(request):

    user = request.user
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
        "user":user,
    }
    return render(request, template_pass("management", "categories"), context)


def items_posted(request):
    user = request.user

    items = ItemPost.objects.all()
    
    context = {
        "items": items,
         "user":user,
    }
    return render(request, template_pass("management", "items_posted"), context)




@superuser_required
def item_detail(request, item_id):
    user = request.user
    item = ItemPost.objects.get(id=item_id)
    
    context = {
        "item": item,
         "user":user,
    }
    return render(request, template_pass("management", "item_detail"), context)


@superuser_required
def claim_management(request):
    user = request.user

    claims = ClaimRequest.objects.all()
    
    context = {
        "claims": claims,
         "user":user,
    }
    return render(request, template_pass("management", "claims_management"), context)


def user_management(request):
    user = request.user
    profiles = Profile.objects.all()
    
    context = {
        "profiles": profiles,
        "user":user,
    }
    return render(request, template_pass("management", "user_management"), context)