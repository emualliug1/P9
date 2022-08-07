from django import forms
from blog.models import Ticket, Review ,UserFollows
from authentication.models import User

class TicketForm(forms.ModelForm):
    title = forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'class:': 'form-control',
            'placeholder': "Titre Ticket", })
    )
    description = forms.CharField(label='', widget=forms.Textarea(
        attrs={
            'class:': 'form-control',
            'placeholder': "Description", })
        )
    image = forms.ImageField(label='', widget=forms.FileInput(
        attrs={
            'class:': 'input_file', })
        )

    class Meta:
        model = Ticket
        fields = ('title', 'description', 'image')


class ReviewForm(forms.ModelForm):

    headline = forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'class:': 'form-control',
            'placeholder': "Titre Review", })
        )

    body = forms.CharField(label='', widget=forms.Textarea(
        attrs={
            'class:': 'form-control',
            'placeholder': "Critique", })
        )

    class Meta:
        model = Review
        fields = ('headline', 'rating', 'body')

