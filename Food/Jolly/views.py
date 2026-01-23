import re
import json
from decimal import Decimal
from itertools import groupby
from operator import itemgetter
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import CartItem, Profile, SecurityLog, Driver
from .utils.telegram import send_telegram_alert, send_telegram_location
from django.http import JsonResponse
from .models import Delivery
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta



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

    # --- ADD THIS LOGIC HERE ---
    # Find the most recent delivery for this user that isn't finished yet
    active_delivery = None
    if request.user.is_authenticated:
        active_delivery = Delivery.objects.filter(customer=request.user).exclude(status="delivered").last()

    # If the user is a Guest, we find the delivery by the token stored in their session
    if not active_delivery and request.session.get('delivery_token'):
        active_delivery = Delivery.objects.filter(token=request.session.get('delivery_token')).last()
    # ---------------------------

    context = {
        'cart_items': cart_items,
        'cart_count': sum(item.quantity for item in cart_items),
        'cart_total': totals['subtotal'],
        'grand_total': totals['grand_total'],
        'paid': request.session.get('paid', False),
        'delivery_token': request.session.get('delivery_token'),
        'delivery': active_delivery,
        'delivery_id': active_delivery.id if active_delivery else None,
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
        phone = data.get('phone')  # NEW: Captured from frontend

        # 1. Basic Validation
        if not all([username, email, password, phone]):
            return JsonResponse({'success': False, 'error': 'All fields are required'})

        if len(password) < 6:
            return JsonResponse({'success': False, 'error': 'Password must be at least 6 characters'})

        # 2. Check for existing users
        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'error': 'Username already exists'})

        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'error': 'Email already registered'})

        # 3. Create User and update Profile
        user = User.objects.create_user(username=username, email=email, password=password)

        # Profile is usually created automatically by signals, but we update it here
        profile, _ = Profile.objects.get_or_create(user=user)
        profile.phone_number = phone
        profile.save()

        # 4. Save phone to session so chatbot knows immediately
        request.session['temp_phone'] = phone
        request.session.modified = True

        # 5. Log the user in
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        # 6. Migrate Guest Cart to the new User account
        session_key = request.session.session_key
        if session_key:
            CartItem.objects.filter(session_key=session_key).update(user=user, session_key=None)

        return JsonResponse({'success': True, 'message': 'Account created successfully!'})

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
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
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


import json
import traceback
from django.http import JsonResponse
from django.conf import settings
from groq import Groq
from .models import CartItem  # Ensure this import exists

# Initialize Groq client once
client = Groq(api_key=settings.GROQ_API_KEY)

# 1. Define the Tools outside the view
# --- UPDATED AI TOOLS ---
AI_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_item_to_cart",
            "description": "Adds a food item to the cart automatically.",
            "parameters": {
                "type": "object",
                "properties": {
                    "item_name": {"type": "string", "description": "The exact name of the food"},
                    "quantity": {"type": "integer", "default": 1}
                },
                "required": ["item_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_user_contact",
            "description": "Saves the user's phone number and delivery landmark.",
            "parameters": {
                "type": "object",
                "properties": {
                    "phone": {"type": "string", "description": "The customer's phone number"},
                    "landmark": {"type": "string", "description": "A nearby landmark for delivery"}
                },
                "required": ["phone"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "trigger_checkout",
            "description": "Call this when the user says they want to pay, checkout, or finish the order."
        }
    }
]


# ---  AI CHATBOT VIEW ---
def ai_chatbot(request):
    user_message = request.GET.get("message", "").strip().lower()

    if not user_message:
        return JsonResponse({"reply": "Akwaaba! 👋 I'm JollyBot! How can I help? 😊"})

    # Determine cart items for context
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        session_key = request.session.session_key
        cart_items = CartItem.objects.filter(session_key=session_key) if session_key else []

    cart_desc = ", ".join([f"{i.quantity}x {i.food_name}" for i in cart_items]) or "Empty"

    # --- CONTACT & LANDMARK RESOLUTION ---
    user_phone = None
    user_landmark = None

    # 1. AUTHENTICATED USER → PROFILE FIRST
    if request.user.is_authenticated:
        profile, _ = Profile.objects.get_or_create(user=request.user)
        if profile.phone_number and profile.phone_number.strip():
            user_phone = profile.phone_number.strip()
            request.session['temp_phone'] = user_phone  # ONLY save if exists
            request.session.modified = True

        first_cart = cart_items.first()
        if first_cart and first_cart.address_text and first_cart.address_text.strip():
            user_landmark = first_cart.address_text.strip()
            request.session['temp_landmark'] = user_landmark
            request.session.modified = True

    # 2. GUEST USER → FALL BACK TO SESSION
    else:
        user_phone = request.session.get('temp_phone')
        user_landmark = request.session.get('temp_landmark')

    # 3. FINAL FALLBACK
    if not user_phone:
        user_phone = "unknown"
    if not user_landmark:
        user_landmark = "unknown"

    has_contact = user_phone != "unknown"

    # --- SYSTEM RULES FOR AI ---
    rules = f"""
    You are JollyBot 🍽️, a food-ordering assistant.

    ⚠️ CRITICAL RULE:
    - If CONTACT SAVED is Yes, NEVER ask for phone again.

    CURRENT CART: {cart_desc}
    CONTACT SAVED: {"Yes" if has_contact else "No"}
    PHONE NUMBER: {user_phone}
    LANDMARK: {user_landmark}

    MENU:
    - Garden Salad: GHS 12
    - Greek Salad: GHS 12
    - Veg Salad: GHS 18
    - Jollof Rice: GHS 15
    - Pasta: GHS 15
    - Grilled Chicken: GHS 18
    - Fried Rice: GHS 13
    - Soda: GHS 2
    - Juice: GHS 5

    AUTOMATION RULES:
    1. If user wants food → call add_item_to_cart.
    2. If user wants to checkout:
       - If CONTACT SAVED is No → ask for phone & landmark.
       - If CONTACT SAVED is Yes → IMMEDIATELY call trigger_checkout.
    3. NEVER ask for phone if CONTACT SAVED is Yes.
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": rules},
                {"role": "user", "content": user_message}
            ],
            tools=AI_TOOLS,
            tool_choice="auto"
        )

        resp_msg = response.choices[0].message

        if resp_msg.tool_calls:
            tool_call = resp_msg.tool_calls[0]
            func_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            # --- ADD TO CART ---
            if func_name == "add_item_to_cart":
                prices = {
                    "garden salad": 12, "greek salad": 12, "veg salad": 18,
                    "jollof rice": 15, "pasta": 15, "grilled chicken": 18,
                    "fried rice": 13, "soda": 2, "juice": 5
                }
                food_name = args.get("item_name", "").lower()
                if food_name in prices:
                    if not request.user.is_authenticated and not request.session.session_key:
                        request.session.create()
                    session_key = request.session.session_key

                    CartItem.objects.create(
                        user=request.user if request.user.is_authenticated else None,
                        session_key=None if request.user.is_authenticated else session_key,
                        food_name=food_name.title(),
                        food_price=prices[food_name],
                        quantity=args.get("quantity", 1)
                    )
                    return JsonResponse({
                        "reply": f"Done! I've added {food_name.title()} to your cart. 🛒 Ready to checkout?",
                        "action": "refresh_ui"
                    })
                else:
                    return JsonResponse({"reply": f"Sorry, we don't have {food_name} today! 😅"})

            # --- SAVE USER CONTACT ---
            if func_name == "save_user_contact":
                phone = args.get("phone")
                landmark = args.get("landmark", "No landmark provided")

                request.session['temp_phone'] = phone
                request.session['temp_landmark'] = landmark
                request.session.modified = True

                if request.user.is_authenticated:
                    prof, _ = Profile.objects.get_or_create(user=request.user)
                    prof.phone_number = phone
                    prof.save()
                    CartItem.objects.filter(user=request.user).update(address_text=landmark)
                else:
                    CartItem.objects.filter(session_key=request.session.session_key).update(address_text=landmark)

                return JsonResponse({
                    "reply": f"Got it! Phone: {phone} and Landmark: {landmark}. We are ready for payment! 💳",
                    "action": "refresh_ui"
                })

            # --- TRIGGER CHECKOUT ---
            if func_name == "trigger_checkout":
                first_item = cart_items.first()
                if not first_item or not first_item.lat or first_item.lat == 0:
                    return JsonResponse({
                        "reply": "I'm ready! 📍 But first, I need your location so the rider can find you. I'm requesting it now...",
                        "action": "request_gps"
                    })

                if not has_contact:
                    return JsonResponse({
                        "reply": "Wait! I still need your phone number for the delivery rider before we can pay. 📞"
                    })

                return JsonResponse({
                    "reply": "Everything is set! Redirecting you to the secure payment page... 💳",
                    "action": "redirect",
                    "url": "/payment/"
                })

        # Default text response
        return JsonResponse({"reply": resp_msg.content})

    except Exception as e:
        print("❌ Groq API ERROR:")
        traceback.print_exc()
        return JsonResponse({"reply": "Oops! My brain stalled. Try again? 😅"}, status=500)


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
    # 1. Deliveries waiting for a driver
    available_deliveries = Delivery.objects.filter(status="new", driver=None)

    # 2. Jobs currently being handled by THIS driver
    my_current_jobs = Delivery.objects.filter(driver__user=request.user, status="picked")

    # 3. FIX: Define the history_jobs variable (Completed deliveries)
    # We filter by the driver's profile and the "delivered" status
    history_jobs = Delivery.objects.filter(driver__user=request.user, status="delivered").order_by('-id')

    # 4. CALCULATE EARNINGS:
    completed_count = history_jobs.count()
    total_earnings = completed_count * 5.0  # GHS 5.00 per delivery

    return render(request, "driver_dashboard.html", {
        "deliveries": available_deliveries,
        "my_jobs": my_current_jobs,
        "history_jobs": history_jobs,  # Now this variable exists!
        "total_earnings": f"{total_earnings:.2f}",
        "driver": {"name": request.user.username}
    })



def payment(request):
    # Determine the user's cart (Auth or Session)
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart_items = CartItem.objects.filter(session_key=session_key)

    if not cart_items.exists():
        return redirect('homepage')

    totals = calculate_cart_totals(cart_items)

    if request.method == "POST":
        # 1. Payment is confirmed! Pull details stored in session
        # (Stored earlier by save_delivery_details)
        phone = request.session.get('temp_phone', 'Not provided')
        landmark = request.session.get('temp_landmark', 'No landmark provided')

        # 2. Get coordinates and prepare order summary
        first_item = cart_items.first()
        lat = float(first_item.lat) if first_item.lat else 0.0
        lng = float(first_item.lon) if first_item.lon else 0.0
        items_summary = ", ".join([f"{item.quantity}x {item.food_name}" for item in cart_items])

        # 3. Create the Delivery record (The actual order)
        delivery = Delivery.objects.create(
            customer=request.user if request.user.is_authenticated else None,
            customer_name=request.user.username if request.user.is_authenticated else "Guest",
            total_amount=totals['grand_total'],
            items_json=items_summary,
            lat=lat,
            lng=lng,
            phone_number=phone,
            landmark=landmark,
            status="new"
        )

        delivery.save()
        # 4. Finalizing
        # We store the token in the session just for the success page
        request.session['paid'] = True
        request.session['delivery_token'] = delivery.token
        request.session.modified = True  # This tells Django to save the data right now

        # 5. Telegram Notifications
        try:
            send_telegram_alert(
                f"💰 PAID ORDER: {delivery.token}\n"
                f"📞 Phone: {phone}\n"
                f"📍 Landmark: {landmark}\n"
                f"💵 Total: GHS {totals['grand_total']}"
            )
            if lat != 0.0:
                send_telegram_location(lat, lng)
        except:
            pass  # Prevent telegram errors from breaking the user experience

        # 6. Clear the cart and cleanup session
        cart_items.delete()
        if 'temp_phone' in request.session: del request.session['temp_phone']
        if 'temp_landmark' in request.session: del request.session['temp_landmark']

        return JsonResponse({'success': True})

    # GET request: Show the payment page
    return render(request, 'payment.html', {
        'cart_items': cart_items,
        'subtotal': totals['subtotal'],
        'delivery_fee': totals['delivery_fee'],
        'total_ghs': totals['grand_total'],
        'paystack_amount': int(totals['grand_total'] * 100),  # Pesewas
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
    })

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
    try:
        data = json.loads(request.body)
        phone = data.get('phone')
        landmark = data.get('landmark')

        # Store in session (Temporary memory)
        request.session['temp_phone'] = phone
        request.session['temp_landmark'] = landmark

        # We still update the CartItem just in case
        if request.user.is_authenticated:
            CartItem.objects.filter(user=request.user).update(address_text=landmark)
        else:
            session_key = request.session.session_key
            CartItem.objects.filter(session_key=session_key).update(address_text=landmark)

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


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
    try:
        data = json.loads(request.body)
        token_entered = data.get('token')

        # Find the delivery assigned to this user
        delivery = get_object_or_404(Delivery, id=delivery_id, driver__user=request.user)

        if delivery.token == token_entered:
            delivery.status = "delivered" # This makes it count towards earnings
            delivery.save()
            return JsonResponse({'success': True})

        return JsonResponse({'success': False, 'error': 'Incorrect token.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def check_new_jobs(request):
    # Count only the jobs that haven't been picked up yet
    count = Delivery.objects.filter(status="new", driver=None).count()
    return JsonResponse({'count': count})




def check_delivery_status(request, delivery_id):
    try:
        delivery = Delivery.objects.get(id=delivery_id)
        return JsonResponse({
            'status': delivery.status,
            'driver_assigned': True if delivery.driver else False,
            # We send these back so Javascript can detect a change
            'driver_name': delivery.driver.user.username if delivery.driver else None
        })
    except Delivery.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)


# --- CUSTOMER VIEW ---
def track_order(request, delivery_id):
    # 1. Fetch the delivery
    delivery = get_object_or_404(Delivery, id=delivery_id)

    # 2. Security Check (Optional but Recommended)
    # Allows viewing if: User owns the order OR has the delivery token in their session
    is_owner = False
    if request.user.is_authenticated and delivery.customer == request.user:
        is_owner = True
    elif request.session.get('delivery_token') == delivery.token:
        is_owner = True

    # 3. Context Data
    # We pass 'delivery' which contains:
    # - delivery.status (new, picked, delivered)
    # - delivery.driver.user.username (Rider Name)
    # - delivery.driver.phone_number (Rider Phone)
    # - delivery.phone_number (Customer Phone)

    return render(request, 'track_order.html', {
        'delivery': delivery,
        'is_owner': is_owner,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY  # If you show a map
    })

# --- DRIVER REPORT VIEW ---
@login_required
def driver_reports(request):
    try:
        driver_profile = request.user.driver
    except Driver.DoesNotExist:
        return redirect('homepage')

    # Calculate Earnings
    completed_jobs = Delivery.objects.filter(driver=driver_profile, status="delivered")

    # Simple stats
    total_delivered = completed_jobs.count()
    total_earned = total_delivered * 5.00

    # Weekly breakdown (Last 7 days)
    last_week = timezone.now() - timedelta(days=7)
    weekly_jobs = completed_jobs.filter(created_at__gte=last_week).count()
    weekly_earned = weekly_jobs * 5.00

    return render(request, "driver_reports.html", {
        "total_delivered": total_delivered,
        "total_earned": total_earned,
        "weekly_jobs": weekly_jobs,
        "weekly_earned": weekly_earned,
        "history": completed_jobs.order_by('-created_at')[:10]  # Last 10 jobs
    })

