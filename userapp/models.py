from django.db import models
from accounts.models import user_details
from admin_side.models import Book
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
