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
    
]
