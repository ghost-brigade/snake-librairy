from django import forms
from django.utils import timezone

from core.models import Book
from core.models import Reservation


class AddBookForm(forms.ModelForm):
    book_title = forms.CharField(max_length=30, label='Titre du livre')
    cover = forms.ImageField(label='Couverture du livre')
    collection = forms.IntegerField(label='Nombre d\'exemplaires')
    genre = forms.CharField(max_length=30, label='Genre')

    class Meta:
        model = Book
        exclude = ['author', 'created_at']


class BookReservationForm(forms.ModelForm):
    limit_date = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date'}),
        help_text='Select the date you want to return the book (maximum 10 days after the current date).'
    )

    class Meta:
        model = Reservation
        fields = ['book_library', 'limit_date']

    def clean_limit_date(self):
        limit_date = self.cleaned_data.get('limit_date')
        if limit_date and limit_date > timezone.now() + timezone.timedelta(days=10):
            raise forms.ValidationError("The limit date must be 10 days after the current date or less.")
        return limit_date
