from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from homepage.models import Book

def show_homepage(request):
    books = Book.objects.all()
    context = {
        'books' : books,
    }

    return render(request, "homepage.html", context)

# Create your views here.
def get_books (request):
    data = Book.objects.all()
    return HttpResponse(serializers. serialize("json", data), content_type="application/json")



def get_books_by_id(request, id):
    book = Book.objects.filter(pk=id)  # Use filter to get a queryset with a single object
    if book.exists():  # Check if the book with the given ID exists
        return HttpResponse(serializers.serialize("json", book), content_type="application/json")
    else:
        return HttpResponse("Book not found", status=404)