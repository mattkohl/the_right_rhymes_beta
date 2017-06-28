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


class PlaceForm(forms.models.ModelForm):

    class Meta:
        model = Place
        fields = ('full_name', 'latitude', 'longitude')
        widgets = {
            'full_name': forms.fields.TextInput(attrs={
                'placeholder': 'E.g. Houston, Texas, USA',
                'class': 'input-field',
            })
        }
