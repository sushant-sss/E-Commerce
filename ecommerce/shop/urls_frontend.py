from django.urls import path
from .views import index, login_page, signup_page, cart_page, items_page

urlpatterns = [
    path('', index, name='home'),
    path('login/', login_page, name='login'),
    path('signup/', signup_page, name='signup'),
    path('cart-page/', cart_page, name='cart_page'),
    path('items-page/', items_page, name='items_page'),
]

