from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('userlist',views.userlist,name='userlist'),
    path('blockuser/<int:id>',views.blockuser,name='blockuser'),
    path('unblockuser/<int:id>',views.unblockuser,name='unblockuser'),
    path('addcategory',views.add_category,name='addcategory'),
    path('categorylist',views.categorylist,name='categorylist'),
    path('editcategory/<int:id>',views.editcategory,name='editcategory'),
    path('deletecategory/<int:id>',views.deletecategory,name='deletecategory'),
    path('addbook',views.addbook,name='addbook'),
    path('admbooklist',views.admbooklist,name='admbooklist'),
    path('editbook/<int:id>',views.editbook,name='editbook'),
    path('deletebook/<int:id>',views.deletebook,name='deletebook'),
    path('adm_order',views.order_management,name='adm_order'),
    path('coupon',views.coupon,name='coupon'),
    path('addcoupon',views.add_coupon,name='add_coupon'),
    path('editcoupon/<int:id>',views.edit_coupon,name='edit_coupon'),
    path('deletecoupon/<int:id>',views.delete_coupon,name='delete_coupon'),
]
