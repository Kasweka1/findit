from django.urls import path


from base.views import findit_views,base_views

urlpatterns = [
    
    # base views
    path('login/', base_views.login, name='login'),
    path('register/', base_views.register, name='register'),
    path('logout/', base_views.logout_view, name='logout'),
    
    # findit views
    path('', findit_views.landing, name='landing'),
    path('lost-found/', findit_views.lost_found, name='lost_found'),
    path('post-item/', findit_views.post_item, name='post_item'),
    path('about-us/', findit_views.about_us, name='about_us'),
    path('contact/', findit_views.contact, name='contact'),
    path('account/', findit_views.account_profile, name='account'),
]
