from django.shortcuts import render

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