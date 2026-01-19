from django.urls import path
from . import views

urlpatterns = [
    # Core Pages
    path('', views.homepage, name='homepage'),
    path('menu/', views.menu, name='menu'),
    path('contact/', views.contact, name='contact'),
    path('mobile/', views.mobile, name='mobile'),
    path('terms/', views.terms, name='terms'),

    # Cart & Checkout
    path('cart/', views.cart, name='cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/save-delivery-details/', views.save_delivery_details, name='save_delivery_details'),
    path('update-cart-location/', views.update_cart_location, name='update_cart_location'),

    # Payment & Order Processing
    path('payment/', views.payment, name='payment'),
    path('track-order/<int:delivery_id>/', views.track_order, name='track_order'),
    path('check-delivery-status/<int:delivery_id>/', views.check_delivery_status, name='check_status'),

    # Authentication
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # AI Chatbot
    path('ai-chat/', views.ai_chatbot, name='ai_chatbot'),

    # Driver Features
    path("driver/dashboard/", views.driver_dashboard, name="driver_dashboard"),
    path("driver/accept-delivery/<int:delivery_id>/", views.accept_delivery, name="accept_delivery"),
    path("driver/decline-delivery/<int:delivery_id>/", views.decline_delivery, name="decline_delivery"),
    path('driver/verify-token/<int:delivery_id>/', views.verify_delivery_token, name='verify_token'),
    path('driver/reports/', views.driver_reports, name='driver_reports'),
    path('check-new-jobs/', views.check_new_jobs, name='check_new_jobs'),
]