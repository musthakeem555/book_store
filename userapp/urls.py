"""
URL configuration for ecom_book project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='home'),
    path('booklist/', views.book_list, name='booklist'),
    path('book_detail/<int:book_id>/', views.book_detail, name='book_detail'),
    path('add_address/', views.add_address, name='add_address'),
    path('address_list/', views.address_list, name='address_list'),
    path('edit_address/<int:address_id>/', views.edit_address, name='edit_address'),
    path('delete_address/<int:address_id>/', views.delete_address, name='delete_address'),
    path('add_to_cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('cart/update/<int:cart_item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/delete/<int:cart_item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('cart/checkout/', views.checkout, name='checkout'),
    path('payment/<int:address_id>', views.payment, name='payment'),
    path('apply_coupon/<int:address_id>/', views.apply_coupon, name='apply_coupon'),
    path('razorpay/<int:address_id>', views.razor, name='razorpay'),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('profile/', views.user_profile, name='user_profile'),
    path('logout/', LogoutView.as_view(next_page='booklist'), name='logout'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('api/coupon/<str:coupon_code>/', views.get_coupon_details, name='get_coupon_details'),

]

