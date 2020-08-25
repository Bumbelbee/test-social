from django.shortcuts import render
from .models import Profile
# Create your views here.

def my_profile(request):
    profile = Profile.objects.get(user = request.user)

    return render(request,'profiles/myprofile.html',{'profile':profile})