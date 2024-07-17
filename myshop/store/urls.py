from django.urls import path
from .views import (
    product_list,
    tienda,
    add_to_cart,
    remove_from_cart,
    cart,
    contact,
    login,
    logout,
    update_cart,
)

urlpatterns = [
    path('', product_list, name='product_list'),
    path('tienda/', tienda, name='tienda'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart, name='cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('update_cart/', update_cart, name='update_cart'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
]
