from django.test import TestCase
from django.urls import reverse
from reviews.models import Work


class SearchViewTests(TestCase):
    fixtures = ['reviews/fixtures/new_fixture.json']

    def test_search_by_author_last_name(self):
        response = self.client.get(reverse('search'), {'q': '芥川'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "羅生門")
        self.assertContains(response, "蜘蛛の糸")
        self.assertNotContains(response, "人間失格")

    def test_search_by_author_first_name(self):
        response = self.client.get(reverse('search'), {'q': '竜之介'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "羅生門")
        self.assertContains(response, "蜘蛛の糸")
        self.assertNotContains(response, "人間失格")

    def test_search_by_work_title(self):
        response = self.client.get(reverse('search'), {'q': '羅生門'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "羅生門")
        self.assertNotContains(response, "蜘蛛の糸")
        self.assertNotContains(response, "人間失格")

    def test_search_by_work_title_reading(self):
        response = self.client.get(reverse('search'), {'q': 'らしょうもん'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "羅生門")
        self.assertNotContains(response, "蜘蛛の糸")
        self.assertNotContains(response, "人間失格")