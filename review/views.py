from django.shortcuts import render

# Create your views here.
def show_review(request):
    return render(request, 'book_review.html')

def write_review(request):
    return render(request, 'write_review.html')