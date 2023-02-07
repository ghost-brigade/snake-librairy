from django.contrib import admin
from .models import Book, BookLibrary, Genre, Library, ReadingGroup, ReadingSession, Reservation

# Register your models here.
admin.site.register(Book)
admin.site.register(BookLibrary)
admin.site.register(Genre)
admin.site.register(Library)
admin.site.register(ReadingGroup)
admin.site.register(ReadingSession)
admin.site.register(Reservation)