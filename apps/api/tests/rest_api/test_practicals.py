from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from apps.api.models import Practical


class CreatePracticalTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(
            username="omg", email="omg@omg.com", password="omg")

    def tearDown(self):
        self.auth_user.delete()

    def test_create_practical(self):
        url = reverse("practical-list")
        data = {
            "code": "CSCA08",
        }
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Practical.objects.count(), 1)
        self.assertEqual(Practical.objects.get().code, "CSCA08")


class ReadPracticalTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(
            username="omg", email="omg@omg.com", password="omg")
        self.test_practical = Practical.objects.create(code="CSCA08")

    def tearDown(self):
        self.auth_user.delete()
        self.test_practical.delete()

    def test_read_practical_list(self):
        url = reverse("practical-list")
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_practical_list(self):
        url = reverse("practical-detail", args=[self.test_practical.pk])
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UpdatePracticalTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(
            username="omg", email="omg@omg.com", password="omg")
        self.test_practical = Practical.objects.create(code="CSCA08")

    def tearDown(self):
        self.auth_user.delete()
        self.test_practical.delete()

    def test_update_practical(self):
        url = reverse("practical-detail", args=[self.test_practical.pk])
        data = {
            "code": "CHANGED",
        }
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeletePracticalTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(
            username="omg", email="omg@omg.com", password="omg")
        self.test_practical = Practical.objects.create(code="CSCA08")

    def tearDown(self):
        self.auth_user.delete()

    def test_delete_practical(self):
        url = reverse("practical-detail", args=[self.test_practical.pk])
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
