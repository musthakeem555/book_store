from django.db import models

# Create your models here.
# models.py


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # description = models.TextField(blank=True)
    # parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    cover_image = models.ImageField(upload_to='static/images/book_covers', blank=True, null=True)

    def __str__(self):
        return self.title


   




