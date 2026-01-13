import re
import json
from decimal import Decimal
from itertools import groupby
from operator import itemgetter
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import CartItem, Profile, SecurityLog, Driver
from .utils.telegram import send_telegram_alert, send_telegram_location
from .models import Delivery

#Calculates total price of items in the cart
def calculate_cart_totals(cart_items):
    subtotal = sum(item.food_price * item.quantity for item in cart_items)
    delivery_fee = Decimal('5.00')
    grand_total = subtotal + delivery_fee

    return {
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'grand_total': grand_total,
    }

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
        {"id": 1, "name": "Greek salad", "image": "food_1.png", "price": 12, "category": "Salad", "description": "Fresh Greek salad with feta cheese.", "rating": 5},
        {"id": 2, "name": "Veg salad", "image": "food_2.png", "price": 18, "category": "Salad", "description": "Crispy vegetables with light dressing.", "rating": 4},
        {"id": 3, "name": "Clover Salad", "image": "food_3.png", "price": 16, "category": "Salad", "description": "Healthy clover sprouts salad.", "rating": 4},
        {"id": 4, "name": "Chicken Salad", "image": "food_4.png", "price": 24, "category": "Salad", "description": "Grilled chicken with greens.", "rating": 5},
        {"id": 5, "name": "Lasagna Rolls", "image": "food_5.png", "price": 14, "category": "Rolls", "description": "Cheesy lasagna rolled to perfection.", "rating": 5},
        {"id": 6, "name": "Peri Peri Rolls", "image": "food_6.png", "price": 12, "category": "Rolls", "description": "Spicy peri peri rolls for a kick.", "rating": 4},
        {"id": 7, "name": "Chicken Rolls", "image": "food_7.png", "price": 20, "category": "Rolls", "description": "Juicy chicken wrapped in soft rolls.", "rating": 5},
        {"id": 8, "name": "Veg Rolls", "image": "food_8.png", "price": 15, "category": "Rolls", "description": "Delicious rolls packed with veggies.", "rating": 4},
        {"id": 9, "name": "Ripple Ice Cream", "image": "food_9.png", "price": 14, "category": "Deserts", "description": "Chocolate ripple ice cream delight.", "rating": 5},
        {"id": 10, "name": "Fruit Ice Cream", "image": "food_10.png", "price": 22, "category": "Deserts", "description": "Refreshing ice cream with mixed fruits.", "rating": 4},
        {"id": 11, "name": "Jar Ice Cream", "image": "food_11.png", "price": 10, "category": "Deserts", "description": "Ice cream served in cute jars.", "rating": 3},
        {"id": 12, "name": "Vanilla Ice Cream", "image": "food_12.png", "price": 12, "category": "Deserts", "description": "Classic vanilla flavor.", "rating": 5},
        {"id": 13, "name": "Chicken Sandwich", "image": "food_13.png", "price": 12, "category": "Sandwich", "description": "Grilled chicken sandwich.", "rating": 4},
        {"id": 14, "name": "Vegan Sandwich", "image": "food_14.png", "price": 18, "category": "Sandwich", "description": "Healthy vegan delight.", "rating": 5},
        {"id": 15, "name": "Grilled Sandwich", "image": "food_15.png", "price": 16, "category": "Sandwich", "description": "Toasted grilled sandwich.", "rating": 4},
        {"id": 16, "name": "Bread Sandwich", "image": "food_16.png", "price": 24, "category": "Sandwich", "description": "Filling bread sandwich.", "rating": 5},
        {"id": 17, "name": "Cup Cake", "image": "food_17.png", "price": 14, "category": "Cake", "description": "Mini cupcake treat.", "rating": 4},
        {"id": 18, "name": "Vegan Cake", "image": "food_18.png", "price": 12, "category": "Cake", "description": "Delicious plant-based cake.", "rating": 5},
        {"id": 19, "name": "Butterscotch Cake", "image": "food_19.png", "price": 20, "category": "Cake", "description": "Rich butterscotch flavor.", "rating": 5},
        {"id": 20, "name": "Sliced Cake", "image": "food_20.png", "price": 15, "category": "Cake", "description": "Perfect cake slices.", "rating": 4},
        {"id": 21, "name": "Garlic Mushroom", "image": "food_21.png", "price": 14, "category": "Pure Veg", "description": "Sautéed garlic mushrooms.", "rating": 5},
        {"id": 22, "name": "Fried Cauliflower", "image": "food_22.png", "price": 22, "category": "Pure Veg", "description": "Crispy fried cauliflower.", "rating": 4},
        {"id": 23, "name": "Mix Veg Pulao", "image": "food_23.png", "price": 10, "category": "Pure Veg", "description": "Mixed vegetable rice.", "rating": 5},
        {"id": 24, "name": "Rice Zucchini", "image": "food_24.png", "price": 12, "category": "Pure Veg", "description": "Zucchini with rice.", "rating": 4},
        {"id": 25, "name": "Cheese Pasta", "image": "food_25.png", "price": 12, "category": "Pasta", "description": "Creamy cheesy pasta.", "rating": 5},
        {"id": 26, "name": "Tomato Pasta", "image": "food_26.png", "price": 18, "category": "Pasta", "description": "Tangy tomato pasta.", "rating": 4},
        {"id": 27, "name": "Creamy Pasta", "image": "food_27.png", "price": 16, "category": "Pasta", "description": "Rich creamy pasta.", "rating": 5},
        {"id": 28, "name": "Chicken Pasta", "image": "food_28.png", "price": 24, "category": "Pasta", "description": "Chicken with pasta.", "rating": 4},
        {"id": 29, "name": "Butter Noodles", "image": "food_29.png", "price": 14, "category": "Noodles", "description": "Buttery noodles.", "rating": 5},
        {"id": 30, "name": "Veg Noodles", "image": "food_30.png", "price": 12, "category": "Noodles", "description": "Vegetable noodles.", "rating": 3},
        {"id": 31, "name": "Somen Noodles", "image": "food_31.png", "price": 20, "category": "Noodles", "description": "Somen style noodles.", "rating": 5},
        {"id": 32, "name": "Cooked Noodles", "image": "food_32.png", "price": 15, "category": "Noodles", "description": "Cooked noodles with sauce.", "rating": 4},
    ]

    food_list_sorted = sorted(food_list, key=itemgetter('category'))

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



def cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart_items = CartItem.objects.filter(session_key=session_key)

    totals = calculate_cart_totals(cart_items)

    context = {
        'cart_items': cart_items,
        'cart_count': sum(item.quantity for item in cart_items),
        'cart_total': totals['subtotal'],
        'grand_total': totals['grand_total'], # Use this in your HTML
        'paid': request.session.pop('paid', False),
        'delivery_token': request.session.get('delivery_token'),  # Show 6-digit code
    }
    return render(request, 'cart.html', context)

@require_POST
def add_to_cart(request):
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
                defaults={'food_price': food_price, 'food_image': food_image, 'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
        # Change this inside add_to_cart:
            cart_item, created = CartItem.objects.get_or_create(
                user=request.user if request.user.is_authenticated else None,
                session_key=None if request.user.is_authenticated else session_key,
                food_name=food_name,
                defaults={'food_price': food_price, 'food_image': food_image, 'quantity': quantity}
            )

            if not created:
                if quantity == 0:
                    cart_item.delete()
                else:
                    cart_item.quantity = quantity  # Set it exactly to what the JS says
                    cart_item.save()

        if request.user.is_authenticated:
            cart_count = sum(item.quantity for item in CartItem.objects.filter(user=request.user))
        else:
            cart_count = sum(item.quantity for item in CartItem.objects.filter(session_key=session_key))

        return JsonResponse({'success': True, 'cart_count': cart_count, 'message': f'{food_name} added to cart!'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)



@require_POST
def update_cart_item(request):
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
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        cart_item = CartItem.objects.get(id=item_id)
        cart_item.delete()
        return JsonResponse({'success': True ,'message': 'Dish removed from cart!'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

def get_cart_count(request):
    if request.user.is_authenticated:
        count = sum(item.quantity for item in CartItem.objects.filter(user=request.user))
    else:
        session_key = request.session.session_key
        count = sum(item.quantity for item in CartItem.objects.filter(session_key=session_key)) if session_key else 0
    return JsonResponse({'cart_count': count})



@require_POST
def signup_view(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password :
            return JsonResponse({'success': False, 'error': 'All fields are required'})

        if len(password) < 6:
            return JsonResponse({'success': False, 'error': 'Password must be at least 6 characters'})

        pattern = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&]).+$'
        if not re.match(pattern, password):
             return JsonResponse({
                    'success': False,
                    'error': 'Password must contain at least a character, a number and a symbol'
             })

        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'error': 'Username already exists'})
        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'error': 'Email already registered'})

        user = User.objects.create_user(username=username, email=email, password=password)
        profile, _ = Profile.objects.get_or_create(user=user)

        profile.save()

        login(request, user)

        session_key = request.session.session_key
        if session_key:
            CartItem.objects.filter(session_key=session_key).update(user=user, session_key=None)




        return JsonResponse({'success': True, 'message': 'Account created successfully! .'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_POST
def login_view(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse({'success': False, 'error': 'Username and password are required'})

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            session_key = request.session.session_key
            if session_key:
                CartItem.objects.filter(session_key=session_key).update(user=user, session_key=None)

            return JsonResponse({'success': True, 'message': f'Welcome back, {user.username}!'})
        else:
            # Security Log for Failed Login
            SecurityLog.objects.create(
                event_type='LOGIN_FAIL',
                ip_address=request.META.get('REMOTE_ADDR'),
                path=request.path,
                details=f"Failed login attempt for username: {username}",
                severity=2
            )
            return JsonResponse({'success': False, 'error': 'Invalid username or password'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

def logout_view(request):
    logout(request)
    return redirect('homepage')

def terms(request):
    return render(request, 'terms.html')

from django.http import JsonResponse
from django.conf import settings
from groq import Groq
import traceback

# Initialize Groq client once
client = Groq(api_key=settings.GROQ_API_KEY)

def ai_chatbot(request):
    user_message = request.GET.get("message", "").strip().lower()

    # If no message, return greeting
    if not user_message:
        return JsonResponse({"reply": "Akwaaba! 👋 I'm JollyBot! How can I help? 😊"})

    # Check for order-related keywords
    order_words = ['order', 'buy', 'checkout', 'pay', 'delivery', 'deliver', 'purchase']
    if any(word in user_message for word in order_words):
        return JsonResponse({
            "reply": "Perfect! 🛒 To place your order:\n1. Browse our Menu\n2. Add items to Cart\n3. Go to Checkout\n\nClick the Menu button above to get started! 😊"
        })

    # AI rules
    rules = """
You're JollyBot, friendly AI for JollyFoods! 🍽️
Be warm, use emojis 😊 Chat about anything.

MENU (ONLY THESE):
- Garden Salad: GHS 12
- Caesar Salad: GHS 14  
- Jollof Rice: GHS 15
- Pasta: GHS 15
- Grilled Chicken: GHS 18
- Fried Rice: GHS 13
- Soda: GHS 2
- Juice: GHS 5

🚫 NO DISCOUNTS
🚫 If NOT on menu, say we don't have it

When customers ask about ordering, tell them to browse the menu and add to cart.
"""

    try:
        # Use a valid Groq model
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": rules},
                {"role": "user", "content": user_message}
            ]
        )

        # Extract reply
        reply = response.choices[0].message.content
        return JsonResponse({"reply": reply})

    except Exception as e:
        # Print full traceback for debugging
        print("❌ Groq API ERROR:")
        traceback.print_exc()

        # Handle specific common issues
        error_message = str(e)
        if "Connection" in error_message or "timeout" in error_message:
            user_reply = "Hmm 😅 I'm having trouble connecting to the AI service. Please try again in a moment."
        else:
            user_reply = "Oops! Something went wrong. Try again? 😅"

        return JsonResponse({"reply": user_reply}, status=500)


# Geolocation view
def update_cart_location(request):
    if request.method == "POST" and request.user.is_authenticated:
        data = json.loads(request.body)
        lat = data.get('lat')
        lon = data.get('lon')

        # Save for all cart items (or just first one)
        CartItem.objects.filter(user=request.user).update(lat=lat, lon=lon)

        print(f"Saved coords for {request.user.username}: {lat}, {lon}")

        return JsonResponse({'status': 'success'})

def checkout_view(request):
    if request.method == "POST":
        first_item = CartItem.objects.filter(user=request.user).first()

        lat = request.POST.get("id_lat")
        lon = request.POST.get("id_lon")
        phone = request.POST.get("phone")
        landmark = request.POST.get("landmark")

        # Save location + landmark to cart
        if first_item:
            if lat and lon:
                first_item.lat = float(lat)
                first_item.lon = float(lon)
            first_item.address_text = landmark
            first_item.save()

        # Save phone to profile
        if request.user.is_authenticated:
            profile, _ = Profile.objects.get_or_create(user=request.user)
            profile.phone_number = phone
            profile.save()

        return redirect("payment")

    return redirect("cart")



#View for driver
@login_required
def driver_dashboard(request):
    try:
        driver_profile = request.user.driver
    except Driver.DoesNotExist:
        driver_profile = None

    available_deliveries = Delivery.objects.filter(status="new", driver=None)
    my_current_jobs = Delivery.objects.filter(driver=driver_profile, status="picked") if driver_profile else []

    return render(request, "driver_dashboard.html", {
        "deliveries": available_deliveries,
        "my_jobs": my_current_jobs
    })




@login_required
def accept_delivery(request, delivery_id):
    # Ensure the user is actually a Driver
    try:
        driver_profile = request.user.driver
    except Driver.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'You are not a registered driver.'})

    # Find the delivery and assign the driver
    delivery = Delivery.objects.get(id=delivery_id)

    if delivery.driver is None:
        delivery.driver = driver_profile
        delivery.status = "picked"
        delivery.save()
        return JsonResponse({'success': True, 'message': 'Order accepted!'})
    else:
        return JsonResponse({'success': False, 'error': 'Order already taken by another driver.'})


import json
from django.http import JsonResponse
from .models import CartItem, Profile, Delivery


def payment(request):
    # Determine the user's cart
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart_items = CartItem.objects.filter(session_key=session_key)

    totals = calculate_cart_totals(cart_items)

    if request.method == "POST":
        if not cart_items.exists():
            return JsonResponse({'success': False, 'error': 'Cart is empty'})

        # 1. Capture data from the JavaScript fetch request
        try:
            # If you are sending JSON data from JS
            data = json.loads(request.body)
            phone = data.get('phone', 'Not provided')
        except:
            # Fallback for standard form POST
            phone = request.POST.get('phone', 'Not provided')

        # 2. Generate the items summary before clearing the cart
        # This creates a string like: "2x Greek salad, 1x Soda"
        items_summary = ", ".join([f"{item.quantity}x {item.food_name}" for item in cart_items])

        first_item = cart_items.first()
        landmark = first_item.address_text or "No landmark provided"
        lat = float(first_item.lat) if first_item.lat else 0.0
        lng = float(first_item.lon) if first_item.lon else 0.0

        # 3. Create delivery using DIRECT data (No Profile needed)
        delivery = Delivery.objects.create(
            customer=request.user if request.user.is_authenticated else None,
            customer_name=request.user.username if request.user.is_authenticated else "Guest",
            total_amount=totals['grand_total'],
            items_json=items_summary,  # Now capturing items!
            lat=lat,
            lng=lng,
            phone_number=phone,        # Capturing direct from the form
            landmark=landmark,
            status="new"
        )

        request.session['paid'] = True
        request.session['delivery_token'] = delivery.token

        # 4. Telegram Alerts
        if not delivery.notified:
            if lat != 0.0 and lng != 0.0:
                send_telegram_location(lat, lng)

            send_telegram_alert(
                f"🍔 New Order!\n"
                f"👤 Customer: {delivery.customer_name}\n"
                f"📞 Phone: {phone}\n"
                f"📦 Items: {items_summary}\n"
                f"📍 Landmark: {landmark}\n"
                f"💰 Total: GHS {totals['grand_total']}"
            )
            delivery.notified = True
            delivery.save()

        # 5. Clear cart
        cart_items.delete()

        return JsonResponse({'success': True, 'message': 'Order placed successfully!'})

    # (Keep context as is for the GET request)
    context = {
        'cart_items': cart_items,
        'subtotal': totals['subtotal'],
        'delivery_fee': totals['delivery_fee'],
        'total_ghs': totals['grand_total'],
        'paystack_amount': int(totals['grand_total'] * 100),
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
    }
    return render(request, 'payment.html', context)

@login_required
def create_delivery_from_cart(request):

    user_cart = CartItem.objects.filter(user=request.user)

    if not user_cart.exists():
        return redirect('cart')

    totals = calculate_cart_totals(user_cart)
    first_item = user_cart.first()

    # Ensure profile exists
    profile, _ = Profile.objects.get_or_create(user=request.user)
    phone = profile.phone_number or "0000000000"

    # Ensure landmark exists
    landmark = first_item.address_text if first_item.address_text else "No landmark provided"

    lat = float(first_item.lat) if first_item.lat else 0.0
    lng = float(first_item.lon) if first_item.lon else 0.0

    new_order = Delivery.objects.create(
        customer=request.user,
        customer_name=request.user.username,
        total_amount=totals['grand_total'],
        lat=lat,
        lng=lng,
        phone_number=phone,
        landmark=landmark,
        status="new"
    )

    # Clear cart
    user_cart.delete()

    # Optional: Send Telegram alert
    if lat != 0.0 and lng != 0.0:
        send_telegram_location(lat, lng)
    send_telegram_alert(
        f"🍔 New Order!\n"
        f"👤 Customer: {request.user.username}\n"
        f"📞 Phone: {phone}\n"
        f"📍 Landmark: {landmark}\n"
        f"💰 Total: GHS {totals['grand_total']}"
    )

    return render(request, "order_success.html", {"order": new_order})



@require_POST
def save_delivery_details(request):
    data = json.loads(request.body)
    phone = data.get('phone')
    landmark = data.get('landmark')

    if request.user.is_authenticated:
        # Save Landmark to the Cart
        CartItem.objects.filter(user=request.user).update(address_text=landmark)
        # Save Phone to the User Profile
        profile, _ = Profile.objects.get_or_create(user=request.user)
        profile.phone_number = phone
        profile.save()

    return JsonResponse({'success': True})


@login_required
@require_POST
def accept_delivery(request, delivery_id):
    try:
        driver_profile = request.user.driver
        delivery = get_object_or_404(Delivery, id=delivery_id, status="new")
        print(f"DEBUG: Delivery found. Status is: {delivery.status}")

        # Update delivery status and assign driver
        delivery.driver = driver_profile
        delivery.status = "picked"  # Matches your 'my_jobs' filter
        delivery.save()

        return JsonResponse({
            'success': True,
            'lat': str(delivery.lat),  # Send coordinates back to JS
            'lng': str(delivery.lng)
        })
    except Driver.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Not registered as a driver.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# Decline delivery
@csrf_exempt
def decline_delivery(request, delivery_id):
    if request.method == "POST":
        delivery = get_object_or_404(Delivery, id=delivery_id)
        delivery.driver = None  # unassign the driver
        delivery.status = "new"
        delivery.save()
        return JsonResponse({"success": True, "delivery_id": delivery_id})
    return JsonResponse({"success": False}, status=400)


@login_required
@require_POST
def verify_delivery_token(request, delivery_id):
    data = json.loads(request.body)
    token_entered = data.get('token')
    delivery = get_object_or_404(Delivery, id=delivery_id, driver__user=request.user)

    # Assuming your Delivery model has a 'delivery_token' field
    if delivery.delivery_token == token_entered:
        delivery.status = "completed"
        delivery.save()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Incorrect token.'})


def check_new_jobs(request):
    # Count only the jobs that haven't been picked up yet
    count = Delivery.objects.filter(status="new", driver=None).count()
    return JsonResponse({'count': count})