from unittest import mock

from django.db import OperationalError
from django.test import TestCase
from django.urls import Resolver404, resolve

from .views import health, ready


class HealthEndpointTests(TestCase):
    def test_health_returns_ok(self):
        response = self.client.get('/health/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'ok')

    def test_health_names_the_service(self):
        response = self.client.get('/health/')
        self.assertEqual(response.json()['service'], 'devflow-api')

    def test_health_renders_html_for_browsers(self):
        response = self.client.get('/health/', HTTP_ACCEPT='text/html')
        self.assertEqual(response.status_code, 200)

    def test_health_rejects_post(self):
        response = self.client.post('/health/')
        self.assertEqual(response.status_code, 405)

    def test_ready_reaches_the_database(self):
        response = self.client.get('/health/ready/')
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['status'], 'ok')
        self.assertEqual(payload['database'], 'up')

    def test_ready_reports_degraded_when_database_is_down(self):
        with mock.patch('apps.health.views.connection') as connection:
            connection.cursor.side_effect = OperationalError('connection refused')
            response = self.client.get('/health/ready/')
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()['status'], 'degraded')

    def test_health_routes_resolve_to_their_views(self):
        self.assertIs(resolve('/health/').func, health)
        self.assertIs(resolve('/health/ready/').func, ready)

    def test_unknown_path_does_not_resolve(self):
        with self.assertRaises(Resolver404):
            resolve('/does-not-exist/')
