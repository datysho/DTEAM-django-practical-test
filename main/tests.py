from django.test import TestCase
from django.urls import reverse
from .models import CV

class CVViewsTestCase(TestCase):
    def setUp(self):
        self.cv = CV.objects.create(
            firstname='John',
            lastname='Doe',
            skills='Python, Django',
            projects='Project A',
            bio='Test bio',
            contacts='john.doe@example.com'
        )

    def test_cv_list_view(self):
        response = self.client.get(reverse('cv_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')

    def test_cv_detail_view(self):
        response = self.client.get(reverse('cv_detail', args=[self.cv.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John')

