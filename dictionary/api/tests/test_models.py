from django.test import TestCase
from django.contrib.auth.models import User
from api.models import Sense


class BaseTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="test", email="ad@min.com", password="admin", is_superuser=True)


class SenseModelTest(BaseTest):

    first_data = {
        "definition": "The first (ever) sense",
        "headword": "test sense",
        "part_of_speech": "noun",
    }

    second_data = {
        "definition": "Sense the second",
        "headword": "test sense",
        "part_of_speech": "noun",
    }

    def test_saving_and_retrieving_senses(self):
        first_sense = Sense(owner=self.user, **self.first_data)
        first_sense.save()

        second_sense = Sense(owner=self.user, **self.second_data)
        second_sense.save()

        saved_senses = Sense.objects.all()
        self.assertEqual(saved_senses.count(), 2)

        first_saved_sense = saved_senses[0]
        second_saved_sense = saved_senses[1]
        self.assertEqual(first_saved_sense.definition, 'The first (ever) sense')
        self.assertEqual(second_saved_sense.definition, 'Sense the second')
        self.assertEqual(first_saved_sense.headword, second_saved_sense.headword)
