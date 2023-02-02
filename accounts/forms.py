from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import User


class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label='Nom')
    last_name = forms.CharField(max_length=30, label='Prénom')
    username = forms.CharField(max_length=30, label='Nom d\'utilisateur')
    email = forms.CharField(max_length=100, label='Adresse mail')
    # Trouver un moyen d'éditer le label du mot de passe

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
