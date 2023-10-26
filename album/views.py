from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from login_register.urls import *
from homepage.models import Book
from .forms import AlbumForm
from album.models import Album


# Create your views here.
def show_album(request):
    return render(request, 'albums.html')

def create_album(request, slug=None):
    if slug:
        album = get_object_or_404(Album, slug=slug)
        form = AlbumForm(request.POST or None, instance=album)
    else:
        form = AlbumForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            album = form.save(commit=False)
            if request.user.is_authenticated:
                album.user = request.user  # assign the logged in user
                album.save()
                return redirect('view_album', slug=album.slug)
            else:
                # handle unauthenticated user
                return redirect('login_register:login_user')  # or however you want to handle it

    books = Book.objects.all()
    return render(request, 'create_album.html', {'form': form, 'books': books})

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



def view_lists(request):
    lists = Album.objects.all()
    return render(request, 'lists.html', {'lists': lists})

def view_list(request, slug):
    list = get_object_or_404(Album, slug=slug)
    return render(request, 'list.html', {'list': list})