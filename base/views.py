from django.shortcuts import render



def home(request):
    return render(request, 'base/home.html')

def rooms(request):
    return render(request, 'base/room.html')

def auth_page(request):
    return render(request, 'base/authentication/auth.html')

def user_login(request):
    pass

def user_signup(request):
    pass

