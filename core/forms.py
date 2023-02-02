from django import forms

from core.models import Book


class AddBookForm(forms.ModelForm):

    book_title = forms.CharField(max_length=30, label='Titre du livre')
    cover = forms.ImageField(label='Couverture du livre')
    collection = forms.IntegerField(label='Nombre d\'exemplaires')
    genre = forms.CharField(max_length=30, label='Genre')

    class Meta:
        model = Book
        exclude = ['author', 'created_at']
