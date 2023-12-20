from django.shortcuts import render

def show_landingpage(request):
    return render(request, 'landingpage.html')