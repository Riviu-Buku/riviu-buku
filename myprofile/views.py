from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from myprofile.models import ProfileUser
from homepage.models import Book
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.urls import reverse
from myprofile.forms import *
from django.views.decorators.http import require_POST
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core import serializers

@login_required
def show_profile(request):
    user = request.user
    user_has_profile = ProfileUser.objects.filter(user=user).exists()

    liked_books = Book.objects.filter(liked_by_users=user)  # Fetch liked books

    context = {
        'username': request.user.username,
        'user_has_profile': user_has_profile,
    }

    if user_has_profile:
        profile_user = get_object_or_404(ProfileUser, user=user)
        context['profile_user'] = profile_user

    # Pass liked_books to the context
    context['liked_books'] = liked_books

    return render(request, 'myprofile.html', context)

@login_required
def complete_profile(request):
    form = ProfileForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        profile = form.save(commit=False)
        profile.user = request.user
        profile.save()
        messages.success(request, 'Your profile detail has been successfully added!')
        return HttpResponseRedirect(reverse('myprofile:show_profile'))
    
    context = {'form':form}
    return render(request, 'complete_profile.html', context)


@login_required
def update_profile(request):
    user = request.user
    try:
        profile = ProfileUser.objects.get(user=user)
    except ProfileUser.DoesNotExist:
        profile = None

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile) 

        if form.is_valid():
            updated_profile = form.save(commit=False)
            updated_profile.user = user
            updated_profile.save()
            messages.success(request, 'Your profile details have been successfully updated!')
            return HttpResponseRedirect(reverse('myprofile:show_profile'))

    else:
        form = ProfileForm(instance=profile)

    context = {'form': form}
    return render(request, 'update_profile.html', context)

@login_required
def toggle_unlike_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if book.liked_by_users.filter(id=request.user.id).exists():
        book.liked_by_users.remove(request.user)
        liked = False
    else:
        liked = True

    return JsonResponse({'liked': liked})

@login_required
@require_POST
def update_bio(request):
    user = request.user
    new_bio = request.POST.get('bio', '')

    try:
        user.profileuser.bio = new_bio
        user.profileuser.save()

        # You can also return the updated bio in the response
        return JsonResponse({'success': True, 'new_bio': new_bio})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
def get_profile_user(request, id):
    if request.method == 'GET':

        auth_user = User.objects.get(pk=id)
        profile_user = ProfileUser.objects.get(user=auth_user)

        profile_dict = {
            "name": profile_user.name,
            "avatar": profile_user.avatar,
            "bio": profile_user.bio,
            "email": profile_user.email,
            "handphone": profile_user.handphone,
            "address": profile_user.address,
        }

        return JsonResponse(profile_dict, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
@csrf_exempt
def get_profile_other_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        auth_user = User.objects.get(username=data["user"])
        profile_user = ProfileUser.objects.get(user=auth_user)

        profile_dict = {
            "name": profile_user.name,
            "avatar": profile_user.avatar,
            "bio": profile_user.bio,
            "email": profile_user.email,
            "handphone": profile_user.handphone,
            "address": profile_user.address,
        }

        return JsonResponse(profile_dict, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
def complete_profile_flutter(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)

        auth_user = User.objects.get(pk=id)
        profile_user = ProfileUser.objects.get(user=auth_user)

        profile_user.name = data["name"]
        profile_user.avatar = data["avatar"]
        profile_user.bio = data["bio"]
        profile_user.email = data["email"]
        profile_user.handphone = data["handphone"]
        profile_user.address = data["address"]

        profile_user.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
@csrf_exempt
def get_books_liked_by_user_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            user = User.objects.get(username=data["user"])
            liked_books = Book.objects.filter(liked_by_users=user)
            serialized_books = serializers.serialize('json', liked_books)
            return JsonResponse({"status": "success", "liked_books": serialized_books}, status=200)
        except Http404:
            response_data = {'status': 'User not found', "liked_books": []}
            return JsonResponse(response_data, status=200)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)