from django.shortcuts import render
from .models import Profile,Relationship
from .forms import ProfileModelForm
# Create your views here.

def my_profile(request):
    profile = Profile.objects.get(user = request.user)
    form = ProfileModelForm(request.POST or None,request.FILES or None,instance=profile)
    confirm = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True
    context = {
        'profile': profile,
        'form' : form,
        'confirm': confirm
    }
    return render(request,'profiles/myprofile.html',context)


def invites_received_view(request):
    profile = Profile.objects.get(user = request.user)
    qs = Relationship.objects.invantions_received(profile)

    context = {
        'qs':qs,
    }

    return render(request,'profiles/my_invites.html',context)

def profiles_list(request):
    user = request.user
    qs = Profile.objects.get_all_profiles(user)

    context = {
        'qs':qs,
    }

    return render(request,'profiles/profiles_list.html',context)

def invites_profiles_list(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invites(user)

    context = {
        'qs':qs,
    }

    return render(request,'profiles/invites_profiles_list.html',context)