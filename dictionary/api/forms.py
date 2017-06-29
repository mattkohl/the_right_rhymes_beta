from django import forms
from django.core.exceptions import ValidationError
from api.models import Annotation, Artist, Domain, Example, Place, SemanticClass, Sense, Song


EMPTY_NAME_ERROR = "You can't have an empty name"
DUPLICATE_ERROR = "You've already got this"


class AnnotationForm(forms.models.ModelForm):
    
    class Meta:
        model = Annotation
        fields = ('text', 'example', 'sense', 'artist', 'place', 'rhymes',)


class ArtistForm(forms.models.ModelForm):

    class Meta:
        model = Artist
        fields = ('name', 'origin')
        widgets = {
            'name': forms.fields.TextInput(attrs={
                'placeholder': 'Artist name',
                'class': 'input-field',
            })
        }
        error_messages = {
            'name': {'required': EMPTY_NAME_ERROR}
        }

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'name': [DUPLICATE_ERROR]}
            self._update_errors(e)


class DomainForm(forms.models.ModelForm):

    class Meta:
        model = Domain
        fields = ('name',)
        widgets = {
            'name': forms.fields.TextInput(attrs={
                'placeholder': 'Domain name',
                'class': 'input-field',
            })
        }
        error_messages = {
            'name': {'required': EMPTY_NAME_ERROR}
        }

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'name': [DUPLICATE_ERROR]}
            self._update_errors(e)


class ExampleForm(forms.models.ModelForm):
    class Meta:
        model = Example
        fields = ('text', 'from_song',)


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
        
        
class SemanticClassForm(forms.models.ModelForm):

    class Meta:
        model = SemanticClass
        fields = ('name',)
        widgets = {
            'name': forms.fields.TextInput(attrs={
                'placeholder': 'Semantic Class name',
                'class': 'input-field',
            })
        }
        error_messages = {
            'name': {'required': EMPTY_NAME_ERROR}
        }

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'name': [DUPLICATE_ERROR]}
            self._update_errors(e)


class SenseForm(forms.models.ModelForm):
    class Meta:
        model = Sense
        fields = ('headword', 'definition', 'part_of_speech', 'etymology', 'notes',
                  'mentioned_in', 'derivatives', 'synonyms', 'antonyms', 'hypernyms',
                  'meronyms', 'domains', 'semantic_classes', 'dictionaries',)


class SongForm(forms.models.ModelForm):
    class Meta:
        model = Song
        fields = ('title', 'primary_artists', 'featured_artists', 'release_date_string',
                  'album', 'lyrics', 'release_date_verified')