from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_GET

from login_register.urls import *
from homepage.models import Book
from .forms import AlbumForm
from album.models import Album


# Create your views here.
def show_albums(request):
    # Get all albums
    albums = Album.objects.all()

    # Render the template with the albums
    return render(request, 'albums.html', {'albums': albums})

def show_album(request, slug):
    # Get the album with the given slug
    album = get_object_or_404(Album, slug=slug)

    # Render the album details page
    return render(request, 'album.html', {'album': album})

from django.utils.text import slugify
from django.db.utils import IntegrityError

def create_album(request):
    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get('name')
        description = request.POST.get('description')
        book_ids = request.POST.getlist('books')  # This should be a list of book IDs

        if not name:
            # Handle the case where no name is provided
            # For example, you could return an error message
            return render(request, 'create_album.html', {'error': 'Name is required'})

        # Create a new album object
        album = Album(name=name, description=description, user=request.user)


        # Generate a unique slug
        slug = slugify(name)
        unique_slug = slug
        num = 1
        while Album.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        album.slug = unique_slug

        album.save()

        # Add the selected books to the album
        books = Book.objects.filter(id__in=book_ids)
        album.books.set(books)

        return redirect('album:show_album', slug=album.slug)

    else:
        return render(request, 'create_album.html')


def add_book_to_album(request):
    album_id = request.GET.get('album_id')
    book_id = request.GET.get('book_id')
    album = get_object_or_404(Album, id=album_id)
    book = get_object_or_404(Book, id=book_id)
    added = False
    if book not in album.books.all():
        album.books.add(book)
        added = True
    return JsonResponse({'added': added, 'title': book.title})

@require_GET
def search_books(request):
    query = request.GET.get('query', '')
    books = Book.objects.filter(title__icontains=query)
    books_list = list(books.values())
    return JsonResponse(books_list, safe=False)

def get_book_json(request):
    book_item = Book.objects.all
    return HttpResponse(serializers.serialize('json', book_item))

def view_lists(request):
    lists = Album.objects.all()
    return render(request, 'lists.html', {'lists': lists})

def view_list(request, slug):
    list = get_object_or_404(Album, slug=slug)
    return render(request, 'list.html', {'list': list})