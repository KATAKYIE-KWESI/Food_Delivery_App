from django.shortcuts import render


def homepage(request):
    menu_list = [
        {"menu_name": "Salad", "menu_image": "menu_1.png"},
        {"menu_name": "Rolls", "menu_image": "menu_2.png"},
        {"menu_name": "Deserts", "menu_image": "menu_3.png"},
        {"menu_name": "Sandwich", "menu_image": "menu_4.png"},
        {"menu_name": "Cake", "menu_image": "menu_5.png"},
        {"menu_name": "Pure Veg", "menu_image": "menu_6.png"},
        {"menu_name": "Pasta", "menu_image": "menu_7.png"},
        {"menu_name": "Noodles", "menu_image": "menu_8.png"}
    ]

    return render(request, "homepage.html", {"menu_list": menu_list})

def menu(request):
    return render(request, 'menu.html')

def contact(request):
    return render(request, 'contact.html')

def mobile(request):
    return render(request, 'mobile.html')
