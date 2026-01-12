from django.urls import path
from . import views
from .views import accept_delivery, decline_delivery

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('menu/', views.menu, name='menu'),
    path('contact/', views.contact, name='contact'),
    path('mobile/', views.mobile, name='mobile'),

    # New stuff
    path('payment/', views.payment, name='payment'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/count/', views.get_cart_count, name='get_cart_count'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('terms/', views.terms, name='terms'),
    path('ai-chat/', views.ai_chatbot, name='ai_chatbot'),
    path('update-cart-location/', views.update_cart_location, name='update_cart_location'),
    path("driver/dashboard/", views.driver_dashboard, name="driver_dashboard"),
    path('cart/save-delivery-details/', views.save_delivery_details, name='save_delivery_details'),
    path('checkout/', views.checkout_view, name='checkout'),
    path("driver/accept-delivery/<int:delivery_id>/", accept_delivery),
    path("driver/decline-delivery/<int:delivery_id>/", decline_delivery),
    path('verify-token/<int:delivery_id>/', views.verify_delivery_token, name='verify_token'),



]
