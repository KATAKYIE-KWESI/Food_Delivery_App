from django.shortcuts import render

def homepage(request):
    return render(request, 'homepage.html')


def menu(request):
    return render(request, 'menu.html')

def contact(request):
    return render(request, 'contact.html')

def mobile(request):
    return render(request, 'mobile.html')
