from django.contrib.auth.base_user import BaseUserManager
from django.db import models

# Create your models here.
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None):
        if not email:
            raise ValueError("email requis")
        email = self.normalize_email(email)
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """creates new super user with details """

        user = self.create_user(email, username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """
    custom user model
    """
    username = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(unique=True)

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    is_bookseller = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email


class CustomerUser(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_customer")
    bio = models.CharField(max_length=255, default='Customer')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class BookSellerUser(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_bookseller")
    bio = models.CharField(max_length=255, default='Book Seller')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'BookSeller'
        verbose_name_plural = 'BookSellers'
