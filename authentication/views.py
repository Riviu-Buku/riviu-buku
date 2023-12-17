from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from myprofile.models import ProfileUser
from django.contrib.auth.models import User

@csrf_exempt
def login_custom(request):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)
    else:
        return JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali username atau kata sandi."
        }, status=401)
        
    auth_user = User.objects.get(username= data['username'])
    if auth_user is None:
        return JsonResponse({
                "status": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)
    user = ProfileUser.objects.get(user=auth_user)
    if user is None:
        return JsonResponse({
                "status": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)
    return JsonResponse({'user':user.to_dict()})


@csrf_exempt
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            # Status login sukses.
            return JsonResponse({
                "username": user.username,
                "status": True,
                "message": "Login sukses!",
                "id" : user.id
                # Tambahkan data lainnya jika ingin mengirim data ke Flutter.
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali email atau kata sandi."
        }, status=401)
    
@csrf_exempt
def logout(request):
    data = json.loads(request.body)
    user = data['user']
    try:
        auth_logout(request, user)
        return JsonResponse({
            "username": user.username,
            "status": True,
            "message": "Logout berhasil!",
            'user': user
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout gagal."
        }, status=401)
    
@csrf_exempt
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        form = UserCreationForm(data)
        print(form.is_valid())  # Call the method to get the result
        if form.is_valid():
            print(1)  # This will be printed if the form is valid
            user = form.save()
            userProfile = ProfileUser(user=user, name=user.username, avatar="", email="", bio="", address="", handphone="")
            userProfile.save()
            return JsonResponse({
                "status": True,
                "message": "User registered successfully.",
                'user':userProfile.to_dict()
            }, status=201)
        else:
            # Print validation errors for debugging
            errors_json = form.errors.as_json()
            print(errors_json)
            errors_dict = json.loads(errors_json)
            # Get the list of error messages for "username" field
            username_errors = errors_dict.get("username", [])
            # Use the first error message, or a default message if the list is empty
            error_message = username_errors[0] if username_errors else "Registration failed. Check your username or password."
            return JsonResponse({
                "status": False,
                "message": error_message['message']
            }, status=401)

    return JsonResponse({
        "status": False,
        "message": "Invalid request method."
    }, status=405)