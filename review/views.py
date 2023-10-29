from django.shortcuts import render
from homepage.models import Book
from review.models import Review, ReviewCheck
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound, JsonResponse
from django.core import serializers
from django.shortcuts import redirect
from django.contrib import messages  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def show_review(request, id):
    books = Book.objects.get(pk=id)
    # reviewcheckers = ReviewCheck.objects.get(user=request.user)
    user = request.user
    # books = Book.objects.all()
    context = {
        'books' : books,
        'login_info' : user,
        # 'reviewcheckers' : reviewcheckers
    }
    return render(request, 'book_review.html', context)


def write_review(request):
    return render(request, 'write_review.html')

def get_review_json(request, id):
    books = Book.objects.get(pk=id)
    reviews = books.review.all()
    return HttpResponse(serializers.serialize('json', reviews))

def get_review_by_user_json(request, id):
    books = Book.objects.get(pk=id)
    reviews = books.review.filter(user=request.user)
    return HttpResponse(serializers.serialize('json', reviews))

# def get_checkedreview_by_user_json(request, review):
#     checkedreviews = ReviewCheck.filter(user=request.user)
#     checkedreviews = checkedreviews.get(review = review)
#     return HttpResponse(serializers.serialize('json', checkedreviews))

@csrf_exempt
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
def increase_upvote_ajax(request, item_id):
    if request.method == 'POST':
        try:
            review = Review.objects.get(pk=item_id)
            review.upvote += 1
            review.save()
            response_data = {'message': "POST"}
            status_code = 201
            return HttpResponse(b"POST", status=201)
        except Review.DoesNotExist:
            return HttpResponseNotFound()

    return HttpResponseNotFound()

@csrf_exempt
def decrease_upvote_ajax(request, item_id):
    if request.method == 'POST':
        try:
            review = Review.objects.get(pk=item_id)
            review.upvote -= 1
            review.save()
            response_data = {'message': 'POST'}
            status_code = 201
            return HttpResponse(b"POST", status=201)
        except Review.DoesNotExist:
            return HttpResponseNotFound()

    return HttpResponseNotFound()

@csrf_exempt
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

@csrf_exempt
def delete_review(request, item_id):
    if request.method == 'DELETE':
        try:
            review = Review.objects.get(pk=item_id)
            print('test')
            book = Book.objects.get(review = review)
            print('test')
            # Now, you have the review associated with the book, and you can perform your operations
            if(book.numRatings-1 == 0):
                book.rating = 0
            else:
                book.rating = (book.rating * book.numRatings - review.stars) / (book.numRatings - 1)
                
            book.numRatings -=1
            book.save()
            review.delete()
            response_data = {'message': 'DELETE'}
            status_code = 201
            return HttpResponse(b"POST", status=201)
        except Review.DoesNotExist:
            return HttpResponseNotFound()

    return HttpResponseNotFound()