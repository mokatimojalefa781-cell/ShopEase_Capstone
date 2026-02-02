from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Product, CartItem


# =========================
# HOME (login + register)
# =========================
def home(request):
    if request.user.is_authenticated:
        return redirect('products')

    return render(request, 'shop/home.html', {
        'login_form': AuthenticationForm(),
        'register_form': UserCreationForm()
    })


# =========================
# LOGIN
# =========================
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Welcome back!")
            return redirect('products')
        else:
            messages.error(request, "Invalid username or password.")

    return redirect('home')


# =========================
# REGISTER
# =========================
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('products')
        else:
            messages.error(request, "Registration failed. Please check the form.")

    return redirect('home')


# =========================
# LOGOUT
# =========================
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')


# =========================
# PRODUCTS
# =========================
@login_required
def products(request):
    return render(request, 'shop/products.html', {
        'products': Product.objects.all()
    })


# =========================
# ADD TO CART
# =========================
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        item.quantity += 1
        item.save()

    messages.success(request, f"{product.name} added to cart.")
    return redirect('cart')


# =========================
# CART
# =========================
@login_required
def cart(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in items)

    return render(request, 'shop/cart.html', {
        'items': items,
        'total': total
    })


# =========================
# CHECKOUT
# =========================
@login_required
def checkout(request):
    # Get all cart items for the current user
    items = CartItem.objects.filter(user=request.user)

    if not items.exists():
        messages.error(request, "Your cart is empty!")
        return redirect('products')

    total = sum(item.total_price() for item in items)

    if request.method == "POST":
        # In a real app, payment logic goes here
        # For demo: we just clear the cart and show success

        items.delete()  # Clear the cart
        messages.success(request, "Order confirmed! Thank you for shopping.")

        return render(request, 'shop/checkout_success.html', {'total': total})

    return render(request, 'shop/checkout.html', {
        'items': items,
        'total': total
    })


# =========================
# ABOUT
# =========================
def about(request):
    return render(request, 'shop/about.html')
