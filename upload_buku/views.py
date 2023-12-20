from django.shortcuts import render
from upload_buku.forms import *
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from homepage.views import *
from django.contrib.auth.decorators import login_required
import cloudinary
import base64
import json
from django.contrib.auth.models import User
# Create your views here.


@login_required
def upload_buku(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.numLikes = 0
            book.numRatings = 0
            book.rating = 0

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
@csrf_exempt
def create_book_flutter(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)
        print(data["coverImg"])
        if(data["coverImg"] != "https://res.cloudinary.com/dcf91ipuo/image/upload/v1702620170/defaultCoverImg_pvks08.jpg"):
            format, imgstr = data["coverImg"].split(';base64,')
            ext = format.split('/')[-1]
            decoded_image = base64.b64decode(imgstr)
            result = cloudinary.uploader.upload(decoded_image)
            data["coverImg"] = result['url']

        new_product = Book.objects.create(
            user = User.objects.get(username= data["user"]),
            title = data["title"],
            description = data["description"],
            coverImg = data["coverImg"],
            numLikes = 0,
            numRatings = 0,
            rating = 0,
        )

        new_product.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

