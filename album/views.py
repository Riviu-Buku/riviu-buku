from django.shortcuts import render

# Create your views here.
def show_album(request):
    return render(request, 'album.html')