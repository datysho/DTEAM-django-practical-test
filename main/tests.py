from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
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

class CVAPITestCase(APITestCase):
    def setUp(self):
        self.cv_data = {
            'firstname': 'Alice',
            'lastname': 'Smith',
            'skills': 'Python, Django, REST',
            'projects': 'Project X',
            'bio': 'A skilled developer.',
            'contacts': 'alice.smith@example.com'
        }
        self.cv = CV.objects.create(**self.cv_data)

    def test_list_cv(self):
        url = reverse('cv-list')  # Automatically created by the router
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_retrieve_cv(self):
        url = reverse('cv-detail', args=[self.cv.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['firstname'], self.cv_data['firstname'])

    def test_create_cv(self):
        url = reverse('cv-list')
        new_cv_data = {
            'firstname': 'Bob',
            'lastname': 'Johnson',
            'skills': 'JavaScript, React',
            'projects': 'Project Y',
            'bio': 'Another developer.',
            'contacts': 'bob.johnson@example.com'
        }
        response = self.client.post(url, new_cv_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['firstname'], new_cv_data['firstname'])

    def test_update_cv(self):
        url = reverse('cv-detail', args=[self.cv.id])
        updated_data = {
            'firstname': 'Alice',
            'lastname': 'Smith',
            'skills': 'Python, Django, DRF',
            'projects': 'Project X',
            'bio': 'An expert developer.',
            'contacts': 'alice.smith@example.com'
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['skills'], updated_data['skills'])

    def test_delete_cv(self):
        url = reverse('cv-detail', args=[self.cv.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from .models import RequestLog
from .middleware import RequestLoggingMiddleware

def dummy_get_response(request):
    return None

class RequestLoggingMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = RequestLoggingMiddleware(dummy_get_response)

    def test_logging_for_anonymous_request(self):
        request = self.factory.get('/test-path/?foo=bar')
        request.user = AnonymousUser()
        self.middleware.process_request(request)
        log = RequestLog.objects.last()
        self.assertEqual(log.method, 'GET')
        self.assertEqual(log.path, '/test-path/')
        self.assertEqual(log.query_string, 'foo=bar')
        # REMOTE_ADDR may be empty in test environment
        self.assertIsNone(log.user)

    def test_logging_for_authenticated_user(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        request = self.factory.get('/test-path/')
        request.user = user
        self.middleware.process_request(request)
        log = RequestLog.objects.last()
        self.assertEqual(log.user, user)

