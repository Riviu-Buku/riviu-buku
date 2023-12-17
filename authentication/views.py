from django.shortcuts import render
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
    print("hello")
    print(password)
    print(username)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            # Status login sukses.
            # return JsonResponse({
            #     "username": user.username,
            #     "status": True,
            #     "message": "Login sukses!",
            #     "id" : user.id
            #     # Tambahkan data lainnya jika ingin mengirim data ke Flutter.
            # }, status=200)
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
    print(user.to_dict())
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
    username = request.user.username

    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout gagal."
        }, status=401)