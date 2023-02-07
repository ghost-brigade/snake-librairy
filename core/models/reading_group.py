from django.db import models
from core.models.library import Library
from core.models.book import Book
from django.contrib.auth import get_user_model

User = get_user_model()


class ReadingGroup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='reading_group_members')
    reading_sessions = models.ManyToManyField(Book, through='ReadingSession')
    created_at = models.DateField(auto_now_add=True)
