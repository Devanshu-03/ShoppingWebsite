from django.urls import path
from store import views
from .views import *
from .views import Placeorder

urlpatterns = [
    path('',Index.as_view(),name='index'),
    path('store',Store.as_view(),name='store'),
    path('add_cart/<int:product_id>',views.add_cart,name='add_cart'),
    path('remove_cart/<int:product_id>',views.remove_cart,name='remove_cart'),
    path('remove_cart_item/<int:product_id>',views.remove_cart_item,name='remove_cart_item'),
    path('placeorder',Placeorder.as_view(),name='placeorder'),
    path('cart',cart.as_view(),name='cart'),
    path('search',search.as_view(),name="search"),
    path('register',Register.as_view(),name='register'),
    path('login',Login.as_view(),name='login'),
    path('logout',Logout,name='logout'),


]