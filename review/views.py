from django.shortcuts import render
from homepage.models import Book
from review.models import Review
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound, JsonResponse
from django.core import serializers
from django.shortcuts import redirect
from django.contrib import messages  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def show_review(request, id):
    books = Book.objects.get(pk=id)
    user = request.user
    # books = Book.objects.all()
    context = {
        'books' : books,
        'login_info' : user,
    }
    return render(request, 'book_review.html', context)


def write_review(request):
    return render(request, 'write_review.html')

def get_review_json(request, id):
    books = Book.objects.get(pk=id)
    reviews = books.review.all()
    return HttpResponse(serializers.serialize('json', reviews))

def get_review_by_user_json(request, id):
    books = Book.objects.get(pk=id)
    reviews = books.review.filter(user=request.user)
    return HttpResponse(serializers.serialize('json', reviews))

@csrf_exempt
def add_review_ajax(request, id):
    books = Book.objects.get(pk=id)
    if request.method == 'POST':
        description = request.POST.get("description")
        user = request.user

        new_review = Review(description=description, user=user)
        new_review.save()
        books.review.add(new_review)

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()