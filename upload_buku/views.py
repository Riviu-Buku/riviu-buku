from django.shortcuts import render

# Create your views here.
def show_upload(request):
    return render(request, 'upload_buku.html')