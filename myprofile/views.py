from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from myprofile.models import ProfileUser
from homepage.models import Book
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from myprofile.forms import *

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
    # Get the book instance
    book = get_object_or_404(Book, id=book_id)

    # Check if the user has liked the book
    if book.liked_by_users.filter(id=request.user.id).exists():
        # User has liked the book, so unlike it
        book.liked_by_users.remove(request.user)
        liked = False
    else:
        liked = True

    return JsonResponse({'liked': liked})