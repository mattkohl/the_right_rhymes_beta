from django import forms

from api.models import Artist, Example, Song, Place


class ArtistForm(forms.models.ModelForm):

    class Meta:
        model = Artist
        fields = ('name',)
        widgets = {
            'name': forms.fields.TextInput(attrs={
                'placeholder': 'Artist name',
                'class': 'input-field',
            })
        }


class ExampleForm(forms.Form):
    pass
