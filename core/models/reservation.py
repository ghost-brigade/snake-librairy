from accounts.models import User
from django.db import models
from core.models.book import Book


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    limit_date = models.DateField()
    created_at = models.DateField(auto_now_add=True)
