from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_GET
from django.utils.text import slugify
from django.db.utils import IntegrityError
from login_register.urls import *
from homepage.models import Book
from .forms import AlbumForm
from album.models import Album
from django.shortcuts import render, get_object_or_404, redirect
from .models import Album
from .forms import AlbumForm
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def show_albums(request):
    # Get all albums
    albums = Album.objects.all()

    # Render the template with the albums
    return render(request, 'albums.html', {'albums': albums})

def delete_album(request, slug):
    album = get_object_or_404(Album, slug=slug)
    album.delete()
    return redirect('album:show_albums')

def show_album(request, slug):
    # Get the album with the given slug
    album = get_object_or_404(Album, slug=slug)

    # Render the album details page
    return render(request, 'album.html', {'album': album})

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

        album.save()

        return redirect('album:show_album', slug=album.slug)

    else:
        return render(request, 'create_album.html')
@login_required()
def edit_album(request, slug):
    # Get the album that you want to edit
    album = get_object_or_404(Album, slug=slug)
    books = Book.objects.all()
    book_ids = list(album.books.values_list('id', flat=True))

    if request.method == 'POST':
        # Get the updated data from the form
        name = request.POST.get('name')
        description = request.POST.get('description')
        book_ids = request.POST.getlist('books')  # This should be a list of book IDs

        if not name:
            return render(request, 'edit_album.html', {'error': 'Name is required', 'album': album})
        elif not description:
            return render(request, 'edit_album.html', {'error': 'Description is required', 'album': album})

        # Update the album object
        album.name = name
        album.description = description

        # Update the selected books in the album
        books = Book.objects.filter(id__in=book_ids)
        album.books.set(books)

        album.save()

        return redirect('album:show_album', slug=album.slug)

    else:
        return render(request, 'edit_album.html', {'album': album, 'books': books, 'book_ids': book_ids})

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

def remove_book_from_album(request, slug):
    if request.method == 'POST':
        # Get the album and book
        album = get_object_or_404(Album, slug=slug)
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Book, id=book_id)

        # Remove the book from the album
        album.books.remove(book)

        # Return a JSON response
        return JsonResponse({'success': True})

    else:
        return JsonResponse({'success': False})

@require_GET
def search_books(request):
    query = request.GET.get('query', '')
    books = Book.objects.filter(title__icontains=query)
    books_list = list(books.values())
    return JsonResponse(books_list, safe=False)

@require_GET
def search_albums(request):
    query = request.GET.get('query', '')
    albums = Album.objects.filter(name__icontains=query)
    album_list = list(albums.values())
    return JsonResponse(album_list, safe=False)

def get_book_json(request):
    book_item = Book.objects.all
    return HttpResponse(serializers.serialize('json', book_item))

def get_album_json(request):
    album_item = Album.objects.all()
    return HttpResponse(serializers.serialize("json", album_item), content_type="application/json")

def view_lists(request):
    lists = Album.objects.all()
    return render(request, 'lists.html', {'lists': lists})

def view_list(request, slug):
    list = get_object_or_404(Album, slug=slug)
    return render(request, 'list.html', {'list': list})

from django.http import JsonResponse
from django.core.serializers import serialize

# ... (existing imports)

@csrf_exempt
def create_album_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        description = data.get('description')
        book_ids = data.get('books')  # This should be a list of book IDs
        auth_user = User.objects.get(username=data["user"])

        if not name:
            return JsonResponse({'error': 'Name is required'}, status=400)

        # Create a new album object
        album = Album(name=name, description=description, user=auth_user)

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

        album.save()

        # Return the JSON representation of the created album
        serialized_album = serialize('json', [album])
        return JsonResponse({'message': 'Album created successfully', 'album': serialized_album}, status=201)

    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def edit_album_flutter(request, slug):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        description = data.get('description')
        book_ids = data.get('books')  # This should be a list of book IDs
        pk = data.get('pk')

        if not name:
            return JsonResponse({'error': 'Name is required'}, status=400)
        elif not description:
            return JsonResponse({'error': 'Description is required'}, status=400)

        album = Album.objects.get(pk=pk)

        # Update the album object
        album.name = name
        album.description = description

        # Update the selected books in the album
        books = Book.objects.filter(id__in=book_ids)
        album.books.set(books)

        album.save()

        return JsonResponse({'message': 'Album updated successfully', 'slug': album.slug}, status=200)

    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def delete_album_flutter(request, slug):
    if request.method == 'DELETE':
        album = get_object_or_404(Album, slug=slug)
        album.delete()
        return JsonResponse({'message': 'Album deleted successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)