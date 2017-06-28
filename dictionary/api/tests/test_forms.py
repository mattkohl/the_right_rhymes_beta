from django.test import TestCase
from api.forms import *


class ArtistFormTest(TestCase):

    def test_form_renders_artist_name_input(self):
        form = ArtistForm()
        self.assertIn('placeholder="Artist name"', form.as_p())
        self.assertIn('class="input-field"', form.as_p())


class PlaceFormTest(TestCase):

    def test_form_renders_place_name_input(self):
        form = PlaceForm()
        self.assertIn('placeholder="E.g. Houston, Texas, USA"', form.as_p())
        self.assertIn('class="input-field"', form.as_p())
