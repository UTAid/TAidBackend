from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from apps.api.models import Lecture


class CreateLectureTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(username="omg", email="omg@omg.com", password="omg")

    def tearDown(self):
        self.auth_user.delete()

    def test_create_lecture(self):
        url = reverse("lecture-list")
        data = {
                "code": "CSCA08",
               }
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lecture.objects.count(), 1)
        self.assertEqual(Lecture.objects.get().code, "CSCA08")


class ReadLectureTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(username="omg", email="omg@omg.com", password="omg")
        self.test_lecture = Lecture.objects.create(code="CSCA08")

    def tearDown(self):
        self.auth_user.delete()
        self.test_lecture.delete()

    def test_read_lecture_list(self):
        url = reverse("lecture-list")
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_lecture_list(self):
        url = reverse("lecture-detail", args=[self.test_lecture.pk])
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UpdateLectureTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(username="omg", email="omg@omg.com", password="omg")
        self.test_lecture = Lecture.objects.create(code="CSCA08")

    def tearDown(self):
        self.auth_user.delete()
        self.test_lecture.delete()

    def test_update_lecture(self):
        url = reverse("lecture-detail", args=[self.test_lecture.pk])
        data = {
                "code": "CHANGED",
               }
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteLectureTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(username="omg", email="omg@omg.com", password="omg")
        self.test_lecture = Lecture.objects.create(code="CSCA08")

    def tearDown(self):
        self.auth_user.delete()

    def test_delete_lecture(self):
        url = reverse("lecture-detail", args=[self.test_lecture.pk])
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
