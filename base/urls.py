from django.urls import path


from base.views import findit_views,base_views, management_views

urlpatterns = [
    
    # base views
    path('login/', base_views.login, name='login'),
    path('register/', base_views.register, name='register'),
    path('logout/', base_views.logout_view, name='logout'),
    
    # findit views
    path('', findit_views.landing, name='landing'),
    path('lost-found/', findit_views.lost_found, name='lost_found'),
    path('item-detail/<int:item_id>/', findit_views.item_detail, name='item_detail'),
    path('claim-item/<int:item_id>/', findit_views.claim_item, name='claim_item'),
    path('claims/<int:claim_id>/update/', findit_views.update_claim, name="update_claim"),
    path('profile/<str:username>/', findit_views.profile_view, name='profile_view'),
    path('post-item/', findit_views.post_item, name='post_item'),
    path('about-us/', findit_views.about_us, name='about_us'),
    path('contact/', findit_views.contact, name='contact'),
    path('account/', findit_views.account_profile, name='account'),
    
    # management views
    path('management/admin-dashboard/', management_views.admin_dashboard, name='admin_dashboard'),
    path('management/categories/', management_views.categories_management, name='categories_management'),
    path('management/items-posted/', management_views.items_posted, name='items_posted'),
    path('management/claims/', management_views.claim_management, name='claim_management'),
    path('management/user-management/', management_views.user_management, name='user_management'),
    path('management/items-posted/<int:item_id>/', management_views.item_detail, name='item_detail_management'),
]
