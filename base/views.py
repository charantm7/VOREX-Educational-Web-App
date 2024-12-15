from django.shortcuts import render



def home(request):
    return render(request, 'base/home.html')

def rooms(request):
    return render(request, 'base/room.html')

def login(request):
    return render(request, 'base/authentication/loginpage.html')