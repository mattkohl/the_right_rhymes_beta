from django import forms

from api.models import Artist, Example, Song, Place


EMPTY_NAME_ERROR = "You can't have an empty name"


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
        error_messages = {
            'name': {'required': EMPTY_NAME_ERROR}
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
        error_messages = {
            'full_name': {'required': EMPTY_NAME_ERROR}
        }