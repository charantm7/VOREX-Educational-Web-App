from django.shortcuts import render



def home(request):
    return render(request, 'base/home.html')

def rooms(request):
    return render(request, 'rooms.html')