from django.shortcuts import render
from upload_buku.forms import *
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from homepage.views import *

# Create your views here.



def upload_buku(request):
    form = BookForm(request.POST, request.FILES)
    if form.is_valid() and request.method == "POST":
        book = form.save(commit=False)
        book.save()
        
        return HttpResponseRedirect(reverse('homepage:show_homepage'))

    context = {'form': form}
    return render(request, "upload_buku.html", context)
