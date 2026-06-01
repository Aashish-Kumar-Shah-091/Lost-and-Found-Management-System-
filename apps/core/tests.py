from django.test import TestCase, Client
from django.urls import reverse


class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_uses_base_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'core/home.html')

    def test_home_contains_navbar(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Lost Items')
        self.assertContains(response, 'Found Items')
        self.assertContains(response, 'Claims')

    def test_home_contains_stats(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'data-counter')

    def test_home_contains_cta(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Report Lost Item')
        self.assertContains(response, 'Report Found Item')
