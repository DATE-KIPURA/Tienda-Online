from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Product
from .cart import Cart
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def tienda(request):
    products = Product.objects.all()

    # Configura la paginación
    paginator = Paginator(products, 8)  # Muestra 8 productos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
    }
    return render(request, 'store/tienda.html', context)

def add_to_cart(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.add(product=product)
    return redirect('tienda')  # Redirige a la página de la tienda después de agregar al carrito

def cart(request):
    cart = Cart(request)
    context = {
        'cart': cart,
    }
    return render(request, 'store/cart.html', context)

def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.remove(product)
    return redirect('cart')  # Redirige de vuelta al carrito después de eliminar un producto

@require_POST
def update_cart(request):
    cart = Cart(request)
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity'))
    
    product = Product.objects.get(id=product_id)
    cart.update(product, quantity)
    
    return redirect('cart')

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        # Envía el correo electrónico
        send_mail(
            f'Mensaje de {name}',
            message,
            email,
            [settings.DEFAULT_FROM_EMAIL],
        )

        return render(request, 'store/contact.html', {'success': True})

    return render(request, 'store/contact.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('product_list')  # Redirige a la página de inicio después de iniciar sesión
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos')

    return render(request, 'store/login.html')

def logout(request):
    auth_logout(request)
    return redirect('login')  # Redirige a la página de inicio de sesión después de cerrar sesión
