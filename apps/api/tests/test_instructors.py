from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from apps.api.models import Instructor


class CreateInstructorTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(username="omg", email="omg@omg.com", password="omg")

    def tearDown(self):
        self.auth_user.delete()

    def test_create_instructor(self):
        url = reverse("instructor-list")
        data = {
                "university_id": "pacotaco",
                "first_name": "Paco",
                "last_name": "Taco",
                "email": "paco@taco.com",
               }
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Instructor.objects.count(), 1)
        self.assertEqual(Instructor.objects.get().university_id, "pacotaco")


class ReadInstructorTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(username="omg", email="omg@omg.com", password="omg")
        self.test_instructor = Instructor.objects.create(
                university_id="pacotaco",
                first_name="Paco",
                last_name="Taco",
                email="paco@taco.com",
                )

    def tearDown(self):
        self.auth_user.delete()
        self.test_instructor.delete()

    def test_read_instructor_list(self):
        url = reverse("instructor-list")
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_instructor_list(self):
        url = reverse("instructor-detail", args=[self.test_instructor.pk])
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UpdateInstructorTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(username="omg", email="omg@omg.com", password="omg")
        self.test_instructor = Instructor.objects.create(
                university_id="pacotaco",
                first_name="Paco",
                last_name="Taco",
                email="paco@taco.com",
                )

    def tearDown(self):
        self.auth_user.delete()
        self.test_instructor.delete()

    def test_update_instructor(self):
        url = reverse("instructor-detail", args=[self.test_instructor.pk])
        data = {
                "university_id": "pacotaco",
                "first_name": "Paco",
                "last_name": "Taco",
                "email": "paco@taco.com",
               }
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteInstructorTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(username="omg", email="omg@omg.com", password="omg")
        self.test_instructor = Instructor.objects.create(
                university_id="pacotaco",
                first_name="Paco",
                last_name="Taco",
                email="paco@taco.com",
                )

    def tearDown(self):
        self.auth_user.delete()

    def test_delete_instructor(self):
        url = reverse("instructor-detail", args=[self.test_instructor.pk])
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
