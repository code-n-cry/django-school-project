from http import HTTPStatus

import django.urls
from django.test import Client, TestCase


class StaticUrlTests(TestCase):
    def test_homepage_endpoint_exists(self):
        response = Client().get(django.urls.reverse('homepage:home'))
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK,
        )
