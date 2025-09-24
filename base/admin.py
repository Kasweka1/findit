from django.contrib import admin

# Register your models here.
from .models import Profile, Category, ItemPost, ClaimRequest

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(ClaimRequest)
admin.site.register(ItemPost)
