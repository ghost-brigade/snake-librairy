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
        help_text='La date de retour du livre ne peut pas être supérieur à 10 jours après la date du jour.'
    )

    class Meta:
        model = Reservation
        fields = ['limit_date']

    def clean_limit_date(self):
        limit_date = self.cleaned_data.get('limit_date')
        if limit_date and limit_date < timezone.localdate() + timezone.timedelta(days=5):
            raise forms.ValidationError("La date ne peut pas être inférieur à 5 jours après la date du jour.")
        if limit_date and limit_date > timezone.localdate() + timezone.timedelta(days=20):
            raise forms.ValidationError("La date ne peut pas être supérieur à 20 jours après la date du jour")

        return limit_date
