from django.db import models
from accounts.models import user_details
from admin_side.models import Book,order_status
from datetime import datetime
from django.utils import timezone
# Create your models here.
class Address(models.Model):
    user = models.ForeignKey(user_details, on_delete=models.CASCADE)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)


class Cart(models.Model):
    user = models.ForeignKey(user_details, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return f"{self.quantity}x {self.book.title} in cart for {self.cart.user.username}"




class Order(models.Model):
    user = models.ForeignKey(user_details, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    order_date = models.DateTimeField(default=datetime.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self):
        return f"Order {self.id} for {self.user.username} on {self.order_date}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_status = models.ForeignKey(order_status,default=1,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantity}x {self.book.title} in order {self.order.id}"

class wallet(models.Model):
    user = models.ForeignKey(user_details, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self):
        return f"wallet for {self.user.username}"  
  
# class other(models.Model):
#     user = models.ForeignKey(user_details, on_delete=models.CASCADE)
#     discount =models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     def __str__(self):
#         return f"wallet for {self.user.username}"  

class wishlist(models.Model):
    user = models.ForeignKey(user_details, on_delete=models.CASCADE)
    item = models.ForeignKey(Book, on_delete=models.CASCADE)
    
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(user_details, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.order_item.book.title} by {self.user.username}"
    
    