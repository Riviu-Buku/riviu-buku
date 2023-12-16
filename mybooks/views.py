from django.http import HttpResponse
from django.shortcuts import render
from homepage.models import Book
from django.core import serializers
from login_register.urls import *
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def show_main(request):
    products = Book.objects.filter(user=request.user)
    context = {
        'products' : products,
    }

    return render(request, "main.html", context)

@login_required
def get_books (request):
    data = products = Book.objects.filter(user=request.user)
    return HttpResponse(serializers. serialize("json", data), content_type="application/json")