from accounts.models import User
from django.db import models
from core.models.genre import Genre


class Book(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    cover = models.ImageField(upload_to='cover')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
