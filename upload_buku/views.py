from django.shortcuts import render
from upload_buku.forms import *
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from homepage.views import *
from django.contrib.auth.decorators import login_required
import cloudinary

# Create your views here.


@login_required
def upload_buku(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user

            # Check if 'image' exists in request.FILES
            if 'image' in request.FILES:
                image = request.FILES['image']
                
                # Upload image to Cloudinary
                result = cloudinary.uploader.upload(image)
                
                book.coverImg = result['url']
           

            book.save()
            return HttpResponseRedirect(reverse('homepage:show_homepage'))

    else:
        form = BookForm()

    context = {'form': form}
    return render(request, "upload_buku.html", context)
