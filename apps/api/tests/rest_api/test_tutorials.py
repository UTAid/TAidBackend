from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from apps.api.models import Tutorial, Student, Instructor


class CreateTutorialTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(username="omg", email="omg@omg.com", password="omg")

    def tearDown(self):
        self.auth_user.delete()

    def test_create_tutorial(self):
        url = reverse("tutorial-list")
        data = {
                "code": "CSCA08",
               }
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tutorial.objects.count(), 1)
        self.assertEqual(Tutorial.objects.get().code, "CSCA08")


class ReadTutorialTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(username="omg", email="omg@omg.com", password="omg")
        self.test_tutorial = Tutorial.objects.create(code="CSCA08")

    def tearDown(self):
        self.auth_user.delete()
        self.test_tutorial.delete()

    def test_read_tutorial_list(self):
        url = reverse("tutorial-list")
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_tutorial_list(self):
        url = reverse("tutorial-detail", args=[self.test_tutorial.pk])
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UpdateTutorialTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(username="omg", email="omg@omg.com", password="omg")
        self.test_tutorial = Tutorial.objects.create(code="CSCA08")

    def tearDown(self):
        self.auth_user.delete()
        self.test_tutorial.delete()

    def test_update_tutorial(self):
        url = reverse("tutorial-detail", args=[self.test_tutorial.pk])
        data = {
                "code": "CHANGED",
               }
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteTutorialTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(username="omg", email="omg@omg.com", password="omg")
        self.test_tutorial = Tutorial.objects.create(code="CSCA08")

    def tearDown(self):
        self.auth_user.delete()

    def test_delete_tutorial(self):
        url = reverse("tutorial-detail", args=[self.test_tutorial.pk])
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
