from django.test import TestCase
from django.contrib.auth.models import User
from api.models import Sense


class BaseTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="test", email="ad@min.com", password="admin", is_superuser=True)


class SenseModelTest(BaseTest):

    def test_saving_and_retrieving_senses(self):
        first_sense = Sense(definition='The first (ever) sense', owner=self.user)
        first_sense.save()

        second_sense = Sense(definition='Sense the second', owner=self.user)
        second_sense.save()

        saved_senses = Sense.objects.all()
        self.assertEqual(saved_senses.count(), 2)

        first_saved_sense = saved_senses[0]
        second_saved_sense = saved_senses[1]
        self.assertEqual(first_saved_sense.definition, 'The first (ever) sense')
        self.assertEqual(second_saved_sense.definition, 'Sense the second')
