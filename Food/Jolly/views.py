from itertools import groupby
from operator import itemgetter

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

    food_list = [
        {"id": 1, "name": "Greek salad", "image": "food_1.png", "price": 12, "category": "Salad",
         "description": "Fresh Greek salad with feta cheese.", "rating": 5},
        {"id": 2, "name": "Veg salad", "image": "food_2.png", "price": 18, "category": "Salad",
         "description": "Crispy vegetables with light dressing.", "rating": 4},
        {"id": 3, "name": "Clover Salad", "image": "food_3.png", "price": 16, "category": "Salad",
         "description": "Healthy clover sprouts salad.", "rating": 4},
        {"id": 4, "name": "Chicken Salad", "image": "food_4.png", "price": 24, "category": "Salad",
         "description": "Grilled chicken with greens.", "rating": 5},
        {"id": 5, "name": "Lasagna Rolls", "image": "food_5.png", "price": 14, "category": "Rolls",
         "description": "Cheesy lasagna rolled to perfection.", "rating": 5},
        {"id": 6, "name": "Peri Peri Rolls", "image": "food_6.png", "price": 12, "category": "Rolls",
         "description": "Spicy peri peri rolls for a kick.", "rating": 4},
        {"id": 7, "name": "Chicken Rolls", "image": "food_7.png", "price": 20, "category": "Rolls",
         "description": "Juicy chicken wrapped in soft rolls.", "rating": 5},
        {"id": 8, "name": "Veg Rolls", "image": "food_8.png", "price": 15, "category": "Rolls",
         "description": "Delicious rolls packed with veggies.", "rating": 4},
        {"id": 9, "name": "Ripple Ice Cream", "image": "food_9.png", "price": 14, "category": "Deserts",
         "description": "Chocolate ripple ice cream delight.", "rating": 5},
        {"id": 10, "name": "Fruit Ice Cream", "image": "food_10.png", "price": 22, "category": "Deserts",
         "description": "Refreshing ice cream with mixed fruits.", "rating": 4},
        {"id": 11, "name": "Jar Ice Cream", "image": "food_11.png", "price": 10, "category": "Deserts",
         "description": "Ice cream served in cute jars.", "rating": 3},
        {"id": 12, "name": "Vanilla Ice Cream", "image": "food_12.png", "price": 12, "category": "Deserts",
         "description": "Classic vanilla flavor.", "rating": 5},
        {"id": 13, "name": "Chicken Sandwich", "image": "food_13.png", "price": 12, "category": "Sandwich",
         "description": "Grilled chicken sandwich.", "rating": 4},
        {"id": 14, "name": "Vegan Sandwich", "image": "food_14.png", "price": 18, "category": "Sandwich",
         "description": "Healthy vegan delight.", "rating": 5},
        {"id": 15, "name": "Grilled Sandwich", "image": "food_15.png", "price": 16, "category": "Sandwich",
         "description": "Toasted grilled sandwich.", "rating": 4},
        {"id": 16, "name": "Bread Sandwich", "image": "food_16.png", "price": 24, "category": "Sandwich",
         "description": "Filling bread sandwich.", "rating": 5},
        {"id": 17, "name": "Cup Cake", "image": "food_17.png", "price": 14, "category": "Cake",
         "description": "Mini cupcake treat.", "rating": 4},
        {"id": 18, "name": "Vegan Cake", "image": "food_18.png", "price": 12, "category": "Cake",
         "description": "Delicious plant-based cake.", "rating": 5},
        {"id": 19, "name": "Butterscotch Cake", "image": "food_19.png", "price": 20, "category": "Cake",
         "description": "Rich butterscotch flavor.", "rating": 5},
        {"id": 20, "name": "Sliced Cake", "image": "food_20.png", "price": 15, "category": "Cake",
         "description": "Perfect cake slices.", "rating": 4},
        {"id": 21, "name": "Garlic Mushroom", "image": "food_21.png", "price": 14, "category": "Pure Veg",
         "description": "Sautéed garlic mushrooms.", "rating": 5},
        {"id": 22, "name": "Fried Cauliflower", "image": "food_22.png", "price": 22, "category": "Pure Veg",
         "description": "Crispy fried cauliflower.", "rating": 4},
        {"id": 23, "name": "Mix Veg Pulao", "image": "food_23.png", "price": 10, "category": "Pure Veg",
         "description": "Mixed vegetable rice.", "rating": 5},
        {"id": 24, "name": "Rice Zucchini", "image": "food_24.png", "price": 12, "category": "Pure Veg",
         "description": "Zucchini with rice.", "rating": 4},
        {"id": 25, "name": "Cheese Pasta", "image": "food_25.png", "price": 12, "category": "Pasta",
         "description": "Creamy cheesy pasta.", "rating": 5},
        {"id": 26, "name": "Tomato Pasta", "image": "food_26.png", "price": 18, "category": "Pasta",
         "description": "Tangy tomato pasta.", "rating": 4},
        {"id": 27, "name": "Creamy Pasta", "image": "food_27.png", "price": 16, "category": "Pasta",
         "description": "Rich creamy pasta.", "rating": 5},
        {"id": 28, "name": "Chicken Pasta", "image": "food_28.png", "price": 24, "category": "Pasta",
         "description": "Chicken with pasta.", "rating": 4},
        {"id": 29, "name": "Butter Noodles", "image": "food_29.png", "price": 14, "category": "Noodles",
         "description": "Buttery noodles.", "rating": 5},
        {"id": 30, "name": "Veg Noodles", "image": "food_30.png", "price": 12, "category": "Noodles",
         "description": "Vegetable noodles.", "rating": 3},
        {"id": 31, "name": "Somen Noodles", "image": "food_31.png", "price": 20, "category": "Noodles",
         "description": "Somen style noodles.", "rating": 5},
        {"id": 32, "name": "Cooked Noodles", "image": "food_32.png", "price": 15, "category": "Noodles",
         "description": "Cooked noodles with sauce.", "rating": 4},
    ]

    food_list_sorted = sorted(food_list, key=itemgetter('category'))

    # Group by category
    grouped_foods = []
    for category, items in groupby(food_list_sorted, key=itemgetter('category')):
        grouped_foods.append({
            'category': category,
            'items': list(items)
        })
    return render(request, "homepage.html", {
        "menu_list": menu_list,
        "food_list": food_list,
         "grouped_foods": grouped_foods,
    })


def menu(request):
    return render(request, 'menu.html')

def contact(request):
    return render(request, 'contact.html')

def mobile(request):
    return render(request, 'mobile.html')



def payment(request):
    return render(request, 'payment.html')