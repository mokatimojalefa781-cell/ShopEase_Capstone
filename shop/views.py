from django.shortcuts import render

def products(request):
    return render(request, 'products.html')

def cart(request):
    return render(request, 'cart.html')

def checkout(request):
    return render(request, 'checkout.html')
