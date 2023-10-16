from django.urls import path
from login_register.views import *

app_name = 'login_register'

urlpatterns = [
    path('signup/', register_user, name='registrasi_user'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
]