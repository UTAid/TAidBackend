from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from apps.api.models import TeachingAssistant


class CreateTeachingAssistantTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(
            username="omg", email="omg@omg.com", password="omg")

    def tearDown(self):
        self.auth_user.delete()

    def test_create_teaching_assistant(self):
        url = reverse("teachingassistant-list")
        data = {
            "university_id": "pacotaco",
            "first_name": "Paco",
            "last_name": "Taco",
            "email": "paco@taco.com",
        }
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TeachingAssistant.objects.count(), 1)
        self.assertEqual(
            TeachingAssistant.objects.get().university_id, "pacotaco")


class ReadTeachingAssistantTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(
            username="omg", email="omg@omg.com", password="omg")
        self.test_teaching_assistant = TeachingAssistant.objects.create(
            university_id="pacotaco",
            first_name="Paco",
            last_name="Taco",
            email="paco@taco.com",
        )

    def tearDown(self):
        self.auth_user.delete()
        self.test_teaching_assistant.delete()

    def test_read_teaching_assistant_list(self):
        url = reverse("teachingassistant-list")
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_teaching_assistant_list(self):
        url = reverse("teachingassistant-detail",
                      args=[self.test_teaching_assistant.pk])
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UpdateTeachingAssistantTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(
            username="omg", email="omg@omg.com", password="omg")
        self.test_teaching_assistant = TeachingAssistant.objects.create(
            university_id="pacotaco",
            first_name="Paco",
            last_name="Taco",
            email="paco@taco.com",
        )

    def tearDown(self):
        self.auth_user.delete()
        self.test_teaching_assistant.delete()

    def test_update_teaching_assistant(self):
        url = reverse("teachingassistant-detail",
                      args=[self.test_teaching_assistant.pk])
        data = {
            "university_id": "pacotaco",
            "first_name": "Paco",
            "last_name": "Taco",
            "email": "paco@taco.com",
        }
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteTeachingAssistantTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(
            username="omg", email="omg@omg.com", password="omg")
        self.test_teaching_assistant = TeachingAssistant.objects.create(
            university_id="pacotaco",
            first_name="Paco",
            last_name="Taco",
            email="paco@taco.com",
        )

    def tearDown(self):
        self.auth_user.delete()

    def test_delete_teaching_assistant(self):
        url = reverse("teachingassistant-detail",
                      args=[self.test_teaching_assistant.pk])
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
