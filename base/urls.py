from django.urls import path
from . import views

urlpatterns = [
    path("", views.shop_main, name="shop"),
    path("all-products", views.shop_all, name="shopAll"),
    path("new-arrivals", views.new_arrival, name="newArrivals"),
    path("shopping-cart", views.cart, name="cart"),
    
]
