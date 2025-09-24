import os
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    mobile_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} Profile"
    

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=2000)
    
    def __str__(self):
        return self.name
    
class ItemPost(models.Model):
    POST_TYPES = [
        ("lost", "Lost"),
        ("found", "Found"),
    ]

    STATUS_CHOICES = [
        ("unclaimed", "Unclaimed"),
        ("claimed", "Claimed"),
        ("resolved", "Resolved"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="items")
    location = models.CharField(max_length=200)
    date_reported = models.DateTimeField(auto_now_add=True)
    post_type = models.CharField(max_length=10, choices=POST_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="unclaimed")
    image = models.ImageField(upload_to="items/", blank=True, null=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")
    
    question_one = models.CharField(max_length=255, blank=True, null=True)
    question_two = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.post_type} - {self.status})"
    
    def get_image_url(self):
        if self.image and self.image.name:
            file_path = os.path.join(settings.MEDIA_ROOT, self.image.name)
            if os.path.exists(file_path):
                return self.image.url
        return "/static/assets/images/findit/default_image.png"


class ClaimRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("owner_accepted", "Accepted By Owner"),
        ("admin_accepted", "Accepted By Admin"),
        ("rejected", "Rejected"),
    ]

    item_post = models.ForeignKey(ItemPost, on_delete=models.CASCADE, related_name="claims")
    claimant = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="claims_made")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    security_answer_one = models.TextField(blank=True, null=True)
    security_answer_two = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Claim by {self.claimant} on {self.item_post}"


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ("claim_submitted", "Claim Submitted"),
        ("claim_accepted", "Claim Accepted"),
        ("claim_rejected", "Claim Rejected"),
    ]

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient} - {self.notification_type}"