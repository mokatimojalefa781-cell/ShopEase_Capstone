from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Product, CartItem, Order


# -------------------------
# AUTH VIEWS
# -------------------------

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


# -------------------------
# HOME & PRODUCTS
# -------------------------

def home(request):
    """
    Home page:
    - Logged out users see login form + hero
    - Logged in users see products
    """
    products = Product.objects.all()

    context = {
        'products': products,
        'show_login_form': not request.user.is_authenticated,
        'login_form': AuthenticationForm() if not request.user.is_authenticated else None,
    }

    return render(request, 'home.html', context)


def products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})


# -------------------------
# CART & CHECKOUT
# -------------------------

@login_required(login_url='/login/')
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


@login_required(login_url='/login/')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product.name} added to cart.")
    return redirect('cart')


@login_required(login_url='/login/')
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total,
    })


# -------------------------
# STATIC PAGES
# -------------------------

def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')



