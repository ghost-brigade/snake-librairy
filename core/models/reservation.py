from accounts.models import User
from django.db import models
from core.models.book_library import BookLibrary


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_library = models.ForeignKey(BookLibrary, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    limit_date = models.DateField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.book_library.book.title + ' - ' + self.user.username