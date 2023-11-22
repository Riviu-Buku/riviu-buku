from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.core import serializers
from homepage.models import Book, FavoriteBook
from django.views.decorators.csrf import csrf_exempt
import json

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
    
@csrf_exempt
def add_book_ajax(request):
    if request.method == 'POST':
        title = request.POST.get("title")
        author = request.POST.get("author")

        new_book = Book(title=title, author=author)
        new_book.save()

        return HttpResponse(b"CREATED", status=201)
    return HttpResponseNotFound()

def show_xml(request):
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Book.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Book.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
def create_product_flutter(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)

        new_product = Book.objects.create(
            user = request.user,
            name = data["name"],
            price = int(data["price"]),
            description = data["description"]
        )

        new_product.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)