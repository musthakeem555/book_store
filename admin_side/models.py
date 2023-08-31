from django.db import models

# Create your models here.
# models.py


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # description = models.TextField(blank=True)
    # parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name

from django.db import models

class Book(models.Model):
    # Existing fields
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    cover_image = models.ImageField(upload_to='static/images/book_covers', blank=True, null=True)
    back_image = models.ImageField(upload_to='static/images/book_covers', blank=True, null=True)
    featured = models.BooleanField(default=False) 
    stock = models.PositiveIntegerField(default=0)
    # New fields for e-commerce website
    # sku = models.CharField(max_length=100, unique=True)  # Stock Keeping Unit
      # Number of books in stock
    # publication_date = models.DateField()               # Date of publication
          # Whether the book is featured on the homepage
    # rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)  # Average rating of the book
    # num_ratings = models.PositiveIntegerField(default=0)  # Number of ratings the book has received

    # Add any other fields relevant to your e-commerce website

    def __str__(self):
        return self.title
      
class order_status(models.Model):
    order_status = models.CharField(max_length=100)
    # description = models.TextField(blank=True)
    # parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.order_status

class Coupon(models.Model):
    DISCOUNT_TYPE_CHOICES = (
        ('amount', 'Amount'),
        ('percentage', 'Percentage'),
    )
    coupon_code=models.CharField(max_length=10,unique=True)
    description=models.TextField()
    minimum_amount=models.IntegerField()
    discount_type=models.CharField(max_length=20,choices=DISCOUNT_TYPE_CHOICES)
    discount=models.DecimalField(max_digits=5,decimal_places=2)
    valid_from=models.DateTimeField()
    valid_to=models.DateTimeField()
    active=models.BooleanField(default=True)
     
    def _str_(self):
        return self.coupon_code    



   




