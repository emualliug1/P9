from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django import forms


class SignupForm(UserCreationForm):
    username = forms.CharField(label='', widget=forms.TextInput(
            attrs={
                'class:': 'form-control',
                'placeholder': "Nom d'utilisateur", })
    )

    first_name = forms.CharField(label='', widget=forms.TextInput(
            attrs={
                'class:': 'form-control',
                'placeholder': "Nom", })
    )
    last_name = forms.CharField(label='', widget=forms.TextInput(
            attrs={
                'class:': 'form-control',
                'placeholder': "Prénom", })
    )
    email = forms.EmailField(label='', widget=forms.EmailInput(
        attrs={
                'class:': 'form-control',
                'placeholder': "Email", })
    )

    password1 = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={
                'class:': 'form-control',
                'placeholder': 'Mot de passe'})
    )
    password2 = forms.CharField(label='', widget=forms.PasswordInput(
            attrs={
                'class:': 'form-control',
                'placeholder': 'Répéter mot de passe'})
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


class LoginForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(
            attrs={
                'class:': 'form-control',
                'placeholder': "Nom d'utilisateur", })
    )
    password = forms.CharField(label='', widget=forms.PasswordInput(
            attrs={
                'class:': 'form-control',
                'placeholder': 'Mot de passe'})
    )


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='', widget=forms.PasswordInput(
            attrs={
                'class:': 'form-control',
                'placeholder': "Ancien Mot de passe", })
    )
    new_password1 = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={
            'class:': 'form-control',
            'placeholder': "Nouveau Mot de passe", })
    )
    new_password2 = forms.CharField(label='', widget=forms.PasswordInput(
            attrs={
                'class:': 'form-control',
                'placeholder': "Répéter Mot de pase", })
    )
