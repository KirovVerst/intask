from rest_framework.test import APITestCase
from rest_framework import status


class BaseTestCase(APITestCase):
    def test_get_main_page(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_get_docs(self):
        r = self.client.get("/api/v1/docs/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
