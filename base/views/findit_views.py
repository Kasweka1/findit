from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from base.models import Category, ItemPost, Profile
from django.contrib import messages
from base.utils import template_pass


def landing(request):
    user = request.user
    profile = None

    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = None

    context = {
        "profile": profile,
        "user": user,
    }
    return render(request, template_pass("findit", "landing"), context)


def lost_found(request):
    categories = Category.objects.all()
    items = ItemPost.objects.all()

    context = {
        "categories": categories,
        "items":items,
    }
    return render(request, template_pass("findit", "lost_found"), context)


def post_item(request):
    user = request.user

    categories = Category.objects.all()
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.warning(request, "You need to log in to post an item.")
            return redirect("login")

        item_name = request.POST.get("item_name")
        category_id = request.POST.get("category")
        post_type = request.POST.get("status").lower()
        description = request.POST.get("description")
        location = request.POST.get("location")
        item_picture = request.FILES.get("item_picture")

        print(category_id)
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None

        profile = Profile.objects.get(user=request.user)

        # Save item
        item_post = ItemPost.objects.create(
            title=item_name,
            category=category,
            post_type=post_type,
            description=description,
            location=location,
            image=item_picture,
            owner=profile,
        )

        messages.success(request, "Your item has been posted successfully!")
        return redirect("lost_found")
    context = {
        "categories": categories,
    }
    return render(request, template_pass("findit", "post_item"), context)


def about_us(request):
    context = {}
    return render(request, template_pass("findit", "about_us"), context)


def contact(request):
    context = {}
    return render(request, template_pass("findit", "contact"), context)


@login_required
def account_profile(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None
    print(profile)

    context = {
        "profile": profile,
    }
    return render(request, template_pass("findit", "account_profile"), context)
