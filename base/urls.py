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
    path('post-item/', findit_views.post_item, name='post_item'),
    path('about-us/', findit_views.about_us, name='about_us'),
    path('contact/', findit_views.contact, name='contact'),
    path('account/', findit_views.account_profile, name='account'),
    
    # management views
    path('management/admin-dashboard/', management_views.admin_dashboard, name='admin_dashboard'),
]
