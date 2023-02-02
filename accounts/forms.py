from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import User


class CreateUserForm(UserCreationForm):

    password1 = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput,
        help_text='Le mot de passe doit contenir au moins 8 caractères, dont au moins une majuscule, une minuscule, un chiffre et un caractère spécial.',
    )
    password2 = forms.CharField(label='Confirmation du mot de passe', widget=forms.PasswordInput)


    first_name = forms.CharField(max_length=30, label='Nom')
    last_name = forms.CharField(max_length=30, label='Prénom')
    username = forms.CharField(max_length=30, label='Nom d\'utilisateur')
    email = forms.CharField(max_length=100, label='Adresse mail')
    # Trouver un moyen d'éditer le label du mot de passe

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
