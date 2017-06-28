from django.test import TestCase
from api.forms import *


class ArtistFormTest(TestCase):

    def test_form_renders_artist_name_input(self):
        form = ArtistForm()
        self.assertIn('placeholder="Artist name"', form.as_p())
        self.assertIn('class="input-field"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ArtistForm(data={'name': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'], [EMPTY_NAME_ERROR])


class PlaceFormTest(TestCase):

    def test_form_renders_place_name_input(self):
        form = PlaceForm()
        self.assertIn('placeholder="E.g. Houston, Texas, USA"', form.as_p())
        self.assertIn('class="input-field"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = PlaceForm(data={'full_name': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['full_name'], [EMPTY_NAME_ERROR])
