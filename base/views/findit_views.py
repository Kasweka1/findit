from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from base.models import Category, ClaimRequest, ItemPost, Profile
from django.contrib import messages
from base.utils import template_pass
from django.utils.timezone import now
from datetime import timedelta


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
    user = request.user
    categories = Category.objects.all()
    items = ItemPost.objects.all()

    for item in items:
        item.is_blurred = item.post_type == "found" and item.owner.user != user

    context = {
        "categories": categories,
        "items": items,
    }
    return render(request, template_pass("findit", "lost_found"), context)


def item_detail(request, item_id):
    # Check if user is logged in first
    if not request.user.is_authenticated:
        messages.info(request, "You need to log in to view this item.")
        return redirect("login")

    user = request.user
    profile = Profile.objects.get(user=user)

    # Get the item or 404
    item = get_object_or_404(ItemPost, id=item_id)
    item.is_blurred = item.post_type == "found" and item.owner.user != user

    claim_count = ClaimRequest.objects.filter(item_post=item).count()

    # Initialize variables for template
    user_claim = None
    all_claims = None
    can_claim = False

    if item.owner.user == user:
        # Owner sees all claims
        all_claims = ClaimRequest.objects.filter(item_post=item)
    else:
        # Non-owner sees only their own claim for this item (if any)
        user_claim = ClaimRequest.objects.filter(
            item_post=item, claimant=profile
        ).first()

        if item.status != "resolved":
            if not user_claim:
                # No claim yet → can claim
                can_claim = True
            else:
                # Claim exists → check status
                if user_claim.status == "rejected":
                    can_claim = True

    context = {
        "item": item,
        "user_claim": user_claim,
        "all_claims": all_claims,
        "can_claim": can_claim,
        "claim_count": claim_count,
    }
    return render(request, template_pass("findit", "item"), context)


@login_required
def claim_item(request, item_id):
    user = request.user
    profile = Profile.objects.get(user=user)
    item = get_object_or_404(ItemPost, id=item_id)

    # Prevent user from claiming their own item
    if item.owner.user == request.user:
        messages.warning(request, "You cannot claim your own item.")
        return redirect("item_detail", item_id=item.id)

    # Check if item is "Found" (only found items can be claimed)
    if item.post_type.lower() != "found":
        messages.warning(request, "Only found items can be claimed.")
        return redirect("item_detail", item_id=item.id)

    # Check if user already claimed this item
    if ClaimRequest.objects.filter(item_post=item, claimant=profile).exists():
        messages.warning(request, "You have already submitted a claim for this item.")
        return redirect("item_detail", item_id=item.id)

    if request.method == "POST":
        security_answer_1 = request.POST.get("security_answer_1")
        security_answer_2 = request.POST.get("security_answer_2")

        ClaimRequest.objects.create(
            item_post=item,
            claimant=profile,
            status="pending",
            security_answer_one=security_answer_1,
            security_answer_two=security_answer_2,
        )

        messages.success(
            request, "Your claim has been submitted. The finder will review it."
        )
        return redirect("item_detail", item_id=item.id)

    return redirect("item_detail", item_id=item.id)


@login_required
def update_claim(request, claim_id):
    claim = get_object_or_404(ClaimRequest, id=claim_id)
    item = claim.item_post

    # Only owner of the item can accept/reject
    if request.user != claim.item_post.owner.user:
        messages.error(request, "You are not allowed to manage this claim.")
        return redirect("item_detail", item_id=claim.item_post.id)

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "accept":
            claim.status = "accepted"
            item.status = "resolved"
            item.save()
            messages.success(request, "Claim has been accepted.")
        elif action == "reject":
            claim.status = "rejected"
            item.status = "unclaimed"
            item.save()
            messages.warning(request, "Claim has been rejected.")
        claim.save()

    return redirect("item_detail", item_id=claim.item_post.id)


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
        security_question_1 = request.POST.get("section_question_1")
        security_question_2 = request.POST.get("section_question_2")

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
            question_one=security_question_1,
            question_two=security_question_2,
        )
        item_post.save()

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

    posted_items = []
    claimed_items = []

    if profile:
        # Items the user has posted
        posted_items = ItemPost.objects.filter(owner=profile)

        # Items the user has claimed
        claimed_items = ClaimRequest.objects.filter(claimant=profile)

    context = {
        "profile": profile,
        "posted_items": posted_items,
        "claimed_items": claimed_items,
    }
    return render(request, template_pass("findit", "account_profile"), context)


def profile_view(request, username):
    try:
        profile = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect("lost_found")

    # Items posted by this user
    posted_items = ItemPost.objects.filter(owner=profile)
    
    claims_on_items = ClaimRequest.objects.filter(item_post__in=posted_items).exclude(claimant=profile)
    accepted_items = ClaimRequest.objects.filter(
        item_post__in=posted_items,
        status="accepted",  
    )

    print(claims_on_items)

    context = {
        "profile": profile,
        "posted_items": posted_items,
        "claims_on_items":claims_on_items,
        "accepted_items":accepted_items,
    }
    return render(request, template_pass("findit", "profile_view"), context)
