from django import forms
from .models import Petition


class PetitionForm(forms.ModelForm):
    class Meta:
        model = Petition
        fields = ['title', 'requested_movie_title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Short title'}),
            'requested_movie_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Movie title to add'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Why should we add this movie?'}),
        }

