from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

class user_details(AbstractUser):
    phone_number = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    # username = models.CharField(max_length=150,unique=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    
    groups = models.ManyToManyField(
    'auth.Group',
    related_name='customuser_groups'
    
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_user_permissions',
    )