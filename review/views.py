from django.shortcuts import render
from homepage.models import Book

# Create your views here.
def show_review(request, id):
    books = Book.objects.get(pk=id)
    # books = Book.objects.all()
    context = {
        'books' : books,
    }
    return render(request, 'book_review.html', context)


def write_review(request):
    return render(request, 'write_review.html')
