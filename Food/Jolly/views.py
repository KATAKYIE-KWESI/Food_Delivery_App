import datetime
from itertools import groupby
from operator import itemgetter
from django.views.decorators.http import require_POST
from .models import CartItem
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required


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



def cart(request):
    #Display cart page
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart_items = CartItem.objects.filter(session_key=session_key)

    total = sum(item.get_total_price() for item in cart_items)

    context = {
        'cart_items': cart_items,
        'cart_total': total,
        'cart_count': sum(item.quantity for item in cart_items)
    }
    return render(request, 'cart.html', context)


@require_POST
def add_to_cart(request):
    #Add item to cart via AJAX
    try:
        data = json.loads(request.body)
        food_name = data.get('name')
        food_price = data.get('price')
        food_image = data.get('image')
        quantity = data.get('quantity', 1)

        if request.user.is_authenticated:
            cart_item, created = CartItem.objects.get_or_create(
                user=request.user,
                food_name=food_name,
                defaults={
                    'food_price': food_price,
                    'food_image': food_image,
                    'quantity': quantity
                }
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key

            cart_item, created = CartItem.objects.get_or_create(
                session_key=session_key,
                food_name=food_name,
                defaults={
                    'food_price': food_price,
                    'food_image': food_image,
                    'quantity': quantity
                }
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()

        # Get updated cart count
        if request.user.is_authenticated:
            cart_count = sum(item.quantity for item in CartItem.objects.filter(user=request.user))
        else:
            cart_count = sum(item.quantity for item in CartItem.objects.filter(session_key=session_key))

        return JsonResponse({
            'success': True,
            'cart_count': cart_count,
            'message': f'{food_name} added to cart!'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_POST
def update_cart_item(request):
    """Update cart item quantity"""
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = data.get('quantity')

        cart_item = CartItem.objects.get(id=item_id)

        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_POST
def remove_from_cart(request):
    """Remove item from cart"""
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')

        cart_item = CartItem.objects.get(id=item_id)
        cart_item.delete()

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def get_cart_count(request):
    """Get cart count for navbar"""
    if request.user.is_authenticated:
        count = sum(item.quantity for item in CartItem.objects.filter(user=request.user))
    else:
        session_key = request.session.session_key
        if session_key:
            count = sum(item.quantity for item in CartItem.objects.filter(session_key=session_key))
        else:
            count = 0
    return JsonResponse({'cart_count': count})



# ============= AUTHENTICATION VIEWS =============

@require_POST
def signup_view(request):
    """Handle user signup via AJAX"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # Validate input
        if not username or not email or not password:
            return JsonResponse({
                'success': False,
                'error': 'All fields are required'
            })

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'success': False,
                'error': 'Username already exists'
            })

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'success': False,
                'error': 'Email already registered'
            })

        # Create new user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Automatically log the user in after signup
        login(request, user)

        # Transfer cart items from session to user account (if any)
        session_key = request.session.session_key
        if session_key:
            from .models import CartItem  # Import your CartItem model
            CartItem.objects.filter(session_key=session_key).update(
                user=user,
                session_key=None
            )

        return JsonResponse({
            'success': True,
            'message': 'Account created successfully! Welcome to JollyFoods!'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@require_POST
def login_view(request):
    """Handle user login via AJAX"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        # Validate input
        if not username or not password:
            return JsonResponse({
                'success': False,
                'error': 'Username and password are required'
            })

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login successful
            login(request, user)

            # Transfer cart items from session to user account (if any)
            session_key = request.session.session_key
            if session_key:
                from .models import CartItem
                CartItem.objects.filter(session_key=session_key).update(
                    user=user,
                    session_key=None
                )

            return JsonResponse({
                'success': True,
                'message': f'Welcome back, {user.username}!'
            })
        else:
            # Login failed
            return JsonResponse({
                'success': False,
                'error': 'Invalid username or password'
            })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


def logout_view(request):

    logout(request)
    return redirect('homepage')  # Redirect to homepage after logout

def terms(request):
    return render(request, 'terms.html')


# ============= PAYMENT VIEWS (Paystack Integration) =============

DELIVERY_FEE = 2.00
TAX_RATE = 0.10  # 10% Tax


def calculate_order_total(request):
    """Calculates the dynamic total amount from the user's cart."""

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        session_key = request.session.session_key
        cart_items = CartItem.objects.filter(session_key=session_key)

    # 1. Calculate Subtotal
    subtotal = sum(item.get_total_price() for item in cart_items)

    # 2. Calculate Tax
    tax_amount = subtotal * TAX_RATE

    # 3. Calculate Grand Total
    grand_total = subtotal + tax_amount + DELIVERY_FEE

    # 4. Paystack requires amount in cents/kobo (integer)
    amount_in_cents = int(grand_total * 100)

    return grand_total, amount_in_cents


@login_required
def payment_view(request):
    # 1. Calculate the actual dynamic total amount
    amount_in_dollars, amount_in_cents = calculate_order_total(request)

    # Check if cart is empty before proceeding
    if amount_in_cents == 0:
        return redirect('cart')  # Redirect to cart if nothing to pay for

    # 2. Collect necessary data for Paystack
    context = {
        # Keys for Paystack
        'PAYSTACK_PUBLIC_KEY': settings.PAYSTACK_PUBLIC_KEY,
        'AMOUNT_IN_CENTS': amount_in_cents,
        'CUSTOMER_EMAIL': request.user.email,
        # Correctly using datetime.datetime.now()
        'REFERENCE': f"JF-{request.user.id}-{amount_in_cents}-{datetime.datetime.now().timestamp()}",

        # Keys for Display in template (optional, but good for dynamic buttons)
        'AMOUNT_IN_DOLLARS': f"{amount_in_dollars:.2f}",
    }

    return render(request, 'payment.html', context)