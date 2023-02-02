from accounts.models import User
from django.db import models


# Create your models here.
class Book(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    book_title = models.CharField(max_length=255)
    cover = models.ImageField(upload_to='cover')
    book_available = models.BooleanField(default=True)
    collection = models.PositiveIntegerField()
    genre = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.book_title
