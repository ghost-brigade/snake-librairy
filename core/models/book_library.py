from django.db import models
from core.models.book import Book


class BookLibrary(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    book_available = models.BooleanField(default=True)
    collection = models.PositiveIntegerField()
    library = models.ForeignKey('Library', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.book.title + ' - ' + self.library.name