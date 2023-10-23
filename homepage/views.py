from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from homepage.models import Book

def show_homepage(request):
    return render(request, 'homepage.html')

# Create your views here.
def get_books (request):
    data = Book.objects.all()
    return HttpResponse(serializers. serialize("json", data), content_type="application/json")