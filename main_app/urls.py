from django.urls import path
from . import views as main_views
from shop import views as shop_views  # import shop app views

urlpatterns = [
    # Home & Auth
    path('', main_views.home, name='home'),
    path('login/', main_views.user_login, name='login'),
    path('register/', main_views.register, name='register'),
    path('logout/', main_views.user_logout, name='logout'),

    # Shop functionality
    path('products/', shop_views.products_view, name='products'),
    path('cart/', shop_views.cart, name='cart'),
    path('checkout/', shop_views.checkout, name='checkout'),
    path('add-to-cart/<int:product_id>/', shop_views.add_to_cart, name='add_to_cart'),

    # Optional static pages
    path('about/', main_views.about, name='about'),
    path('contact/', main_views.contact, name='contact'),
]



