from django.db import models
from core.models.book import Book
from core.models.reading_group import ReadingGroup


class ReadingSession(models.Model):
    reading_group = models.ForeignKey(ReadingGroup, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date = models.DateField()
    created_at = models.DateField(auto_now_add=True)
