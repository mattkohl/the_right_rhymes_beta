from django.test import TestCase
from api.forms import ArtistForm


class ArtistFormTest(TestCase):

    def test_form_renders_artist_name_input(self):
        form = ArtistForm()
        self.assertIn('placeholder="Artist name"', form.as_p())
        self.assertIn('class="input-field"', form.as_p())
