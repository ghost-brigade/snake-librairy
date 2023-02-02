from accounts.models import User
from django.db import models


# Create your models here.
class Book(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    book_title = models.CharField(max_length=255)
    cover = models.ImageField(upload_to='cover')
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.book_title


class BookLibrary(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    book_available = models.BooleanField(default=True)
    collection = models.PositiveIntegerField()
    library = models.ForeignKey('Library', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)


class Library(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    books = models.ManyToManyField(Book, through=BookLibrary)


class Genre(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    limit_date = models.DateField()
    created_at = models.DateField(auto_now_add=True)


class ReadingGroup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='members')
    reading_sessions = models.ManyToManyField(Book, through='ReadingSession')
    created_at = models.DateField(auto_now_add=True)


class ReadingSession(models.Model):
    reading_group = models.ForeignKey(ReadingGroup, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date = models.DateField()
    created_at = models.DateField(auto_now_add=True)