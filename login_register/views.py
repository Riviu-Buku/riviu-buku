from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages       
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from homepage.views import show_homepage
from django.views.decorators.csrf import csrf_exempt
from myprofile.models import ProfileUser

# session and cookies
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse

from myprofile.forms import ProfileForm

# Create your views here.
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("homepage:show_homepage")) 
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)

def complete_profile(request, user):
    form = ProfileForm()

    if form.is_valid() and request.method == "POST":
        profile = form.save(commit=False)
        profile.user = user
        profile.save()
        messages.success(request, 'Your profile detail has been successfully added!')
        return 

def register_user(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            userProfile = ProfileUser(user=user, name= user.username, avatar="", email="", bio="", address="", handphone="")
            userProfile.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('login_register:login_user')
    context = {'form':form}
    return render(request, 'register.html', context)


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('homepage:show_homepage'))
    response.delete_cookie('last_login')
    return response