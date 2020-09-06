from django.urls import path
from .views import *
app_name = 'profiles'

urlpatterns = [
    path('myprofile',my_profile,name="my-profile"),
    path('my-invites',invites_received_view,name="my-invites-view"),
    path('all-profiles-list',profiles_list,name="all-profiles-list"),
    path('invites-profiles-list',invites_profiles_list,name="invites-profiles-list"),

]
