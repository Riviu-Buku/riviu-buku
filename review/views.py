from django.shortcuts import render
from homepage.models import Book
from review.models import Review, ReviewCheck
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound, JsonResponse, Http404
from django.core import serializers
from django.shortcuts import redirect
from django.contrib import messages  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from review.forms import ReviewForm
from django.urls import reverse
import json
from myprofile.models import ProfileUser
from django.contrib.auth.models import User

# Create your views here.

def show_review(request, id):
    try:
        books = Book.objects.get(pk=id)
    except Book.DoesNotExist:
        # Handle the 404 error by returning a custom JSON response
        response_data = {'error': 'Book not found'}
        return JsonResponse(response_data, status=404)
    
    user = request.user
    context = {
        'books' : books,
        'login_info' : user,
    }
    return render(request, 'book_review.html', context)

@login_required
def write_review(request,id):
    form = ReviewForm(request.POST or None)
    try:
        books = Book.objects.get(pk=id)
    except Book.DoesNotExist:
        # Handle the 404 error by returning a custom JSON response
        response_data = {'error': 'Book not found'}
        return JsonResponse(response_data, status=404)

    if form.is_valid() and request.method == "POST":
        review = form.save(commit=False)
        review.user = request.user
        review.name = request.user
        review.save()
        books.review.add(review)
        stars= review.stars
        books.numRatings += 1
        books.rating = (books.rating * (books.numRatings - 1) + stars) / books.numRatings
        books.rating = round(books.rating, 1)
        books.save()
        
        messages.success(request, 'Your review has been added!')
        return HttpResponseRedirect(reverse('review:show_review', args=[id]))
    
    context = {'form':form}
    return render(request, 'write_review.html', context)

def get_review_json(request, id):
    books = get_object_or_404(Book, pk=id)  # This line will raise a 404 if the book doesn't exist
    reviews = books.review.all()
    return HttpResponse(serializers.serialize('json', reviews))

@login_required
def get_review_by_user_json(request, id):
    books = get_object_or_404(Book, pk=id)  # This line will raise a 404 if the book doesn't exist
    reviews = books.review.filter(user=request.user)
    return HttpResponse(serializers.serialize('json', reviews))

@login_required
def get_liked_by_user(request, id):
    try:
        # Use get_object_or_404 to retrieve the book or return a custom JSON response
        book = get_object_or_404(Book, liked_by_users=request.user, id=id)
        # Serialize the book to JSON and return it in the response
        data = serializers.serialize('json', [book])
        return HttpResponse(data, content_type='application/json')
    except Http404:
        # Handle the 404 error by returning a custom JSON response
        response_data = {'error': 'Book not found'}
        return JsonResponse(response_data, status=404)

# def get_checkedreview_by_user_json(request, review):
#     checkedreviews = ReviewCheck.filter(user=request.user)
#     checkedreviews = checkedreviews.get(review = review)
#     return HttpResponse(serializers.serialize('json', checkedreviews))

@csrf_exempt
@login_required
def add_review_ajax(request, id):
    books = Book.objects.get(pk=id)
    if request.method == 'POST':
        description = request.POST.get("description")
        stars = float(request.POST.get("stars"))  # Convert stars to an integer
        user = request.user

        new_review = Review(description=description, user=user, name=user, stars=stars)
        new_review.save()
        books.review.add(new_review)
        books.numRatings += 1
        books.rating = (books.rating * (books.numRatings - 1) + stars) / books.numRatings
        books.rating = round(books.rating, 1)
        books.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

@csrf_exempt
@login_required
def add_book_like(request, id):

    books = Book.objects.get(pk=id)
    if request.method == 'POST':
        user = request.user
        books.liked_by_users.add(user)
        books.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

@csrf_exempt
@login_required
def add_book_unlike(request, id):
    books = Book.objects.get(pk=id)
    if request.method == 'POST':
        user = request.user
        books.liked_by_users.remove(user)
        books.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

@csrf_exempt
@login_required
def increase_upvote_ajax(request, item_id):
    if request.method == 'GET':
        try:
            review = Review.objects.get(pk=item_id)
            review.upvote += 1
            review.save()
            response_data = {'message': "GET"}
            status_code = 201
            return HttpResponse(b"GET", status=201)
        except Review.DoesNotExist:
            return HttpResponseNotFound()

    return HttpResponseNotFound()

@csrf_exempt
@login_required
def decrease_upvote_ajax(request, item_id):
    if request.method == 'GET':
        try:
            review = Review.objects.get(pk=item_id)
            review.upvote -= 1
            review.save()
            response_data = {'message': 'GET'}
            status_code = 201
            return HttpResponse(b"GET", status=201)
        except Review.DoesNotExist:
            return HttpResponseNotFound()

    return HttpResponseNotFound()

@csrf_exempt
@login_required
def increase_downvote_ajax(request, item_id):
    if request.method == 'POST':
        try:
            review = Review.objects.get(pk=item_id)
            review.downvote += 1
            review.save()
            response_data = {'message': 'POST'}
            status_code = 201
            return HttpResponse(b"POST", status=201)
        except Review.DoesNotExist:
            return HttpResponseNotFound()

    return HttpResponseNotFound()

@csrf_exempt
def decrease_downvote_ajax(request, item_id):
    if request.method == 'POST':
        try:
            review = Review.objects.get(pk=item_id)
            review.downvote -= 1
            review.save()
            response_data = {'message': 'POST'}
            status_code = 201
            return HttpResponse(b"POST", status=201)
        except Review.DoesNotExist:
            return HttpResponseNotFound()

    return HttpResponseNotFound()

# @csrf_exempt
# @login_required
# def delete_review(request, item_id):
#     if request.method == 'DELETE':
#         try:
#             review = Review.objects.get(pk=item_id)
#             book = Book.objects.get(review = review)
#             # Now, you have the review associated with the book, and you can perform your operations
#             if(book.numRatings-1 == 0):
#                 book.rating = 0
#             else:
#                 book.rating = (book.rating * book.numRatings - review.stars) / (book.numRatings - 1)
#                 book.rating = round(book.rating, 1)
                
#             book.numRatings -=1
#             book.save()
#             review.delete()
#             response_data = {'message': 'DELETE'}
#             status_code = 201
#             return HttpResponse(b"POST", status=201)
#         except Review.DoesNotExist:
#             return HttpResponseNotFound()

#     return HttpResponseNotFound()


@csrf_exempt
@login_required
def delete_review(request, item_id):
    if request.method == 'DELETE':
        try:
            review = Review.objects.get(pk=item_id)
            book = get_object_or_404(Book, review=review)  # Use get_object_or_404 to get the book
            # Now, you have the review associated with the book, and you can perform your operations
            if book.numRatings - 1 == 0:
                book.rating = 0
            else:
                book.rating = (book.rating * book.numRatings - review.stars) / (book.numRatings - 1)
                book.rating = round(book.rating, 1)

            book.numRatings -= 1
            book.save()
            review.delete()
            response_data = {'message': 'DELETE'}
            status_code = 201
            return HttpResponse(b"POST", status=201)
        except Review.DoesNotExist:
            return HttpResponseNotFound()

    return HttpResponseNotFound()

@csrf_exempt
def create_review_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        books = Book.objects.get(pk= int(data["bookId"]))
        auth_user = User.objects.get(username= data["user"])
        stars = int(data["stars"])
        description = data["description"]

        new_review = Review(description=description, user=auth_user, name=auth_user, stars=stars)
        new_review.save()
        books.review.add(new_review)
        books.numRatings += 1
        books.rating = (books.rating * (books.numRatings - 1) + stars) / books.numRatings
        books.rating = round(books.rating, 1)
        books.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
@csrf_exempt
@login_required
def add_like_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        books = Book.objects.get(pk= int(data["bookId"]))
        user = User.objects.get(username= data["user"])
        books.liked_by_users.add(user)
        books.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
@login_required
def add_unlike_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        books = Book.objects.get(pk= int(data["bookId"]))
        user = User.objects.get(username= data["user"])
        books.liked_by_users.remove(user)
        books.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
