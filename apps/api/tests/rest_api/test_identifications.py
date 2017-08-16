from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from apps.api.models import Identification, Student


class CreateIdentificationTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(username="omg", email="omg@omg.com", password="omg")
        self.test_student = Student.objects.create(
                university_id="pacotaco",
                first_name="Paco",
                last_name="Taco",
                email="paco@taco.com",
                student_number=999999999,
                )

    def tearDown(self):
        self.auth_user.delete()
        self.test_student.delete()

    def test_create_identification(self):
        url = reverse("identification-list")
        data = {
                "value": 999999999,
                "description": "T-Card number",
                "student": self.test_student.pk,
                "number": 1,
               }
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Identification.objects.count(), 1)
        self.assertEqual(int(Identification.objects.get().value), 999999999)
        self.assertEqual(Identification.objects.get().student, self.test_student)


class ReadIdentificationTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(username="omg", email="omg@omg.com", password="omg")
        self.test_student = Student.objects.create(
                university_id="pacotaco",
                first_name="Paco",
                last_name="Taco",
                email="paco@taco.com",
                student_number=999999999,
                )
        self.test_identification = Identification.objects.create(
                student=self.test_student,
                value=999999999,
                description="tcard",
                number=1,
                )

    def tearDown(self):
        self.auth_user.delete()
        self.test_student.delete()
        self.test_identification.delete()

    def test_read_identification_list(self):
        url = reverse("identification-list")
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_identification_list(self):
        url = reverse("identification-detail", args=[self.test_identification.pk])
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UpdateIdentificationTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(username="omg", email="omg@omg.com", password="omg")
        self.test_student = Student.objects.create(
                university_id="pacotaco",
                first_name="Paco",
                last_name="Taco",
                email="paco@taco.com",
                student_number=999999999,
                )
        self.test_identification = Identification.objects.create(
                student=self.test_student,
                value=999999999,
                description="tcard",
                number = 1,
                )

    def tearDown(self):
        self.auth_user.delete()
        self.test_student.delete()
        self.test_identification.delete()

    def test_update_identification(self):
        url = reverse("identification-detail", args=[self.test_identification.pk])
        data = {
                "student": "pacotaco",
                "value": "CHANGED",
                "description": "tcard",
                'number':1,
               }
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteIdentificationTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(username="omg", email="omg@omg.com", password="omg")
        self.test_student = Student.objects.create(
                university_id="pacotaco",
                first_name="Paco",
                last_name="Taco",
                email="paco@taco.com",
                student_number=999999999,
                )
        self.test_identification = Identification.objects.create(
                student=self.test_student,
                value=999999999,
                description="tcard",
                number=1,
                )

    def tearDown(self):
        self.auth_user.delete()
        self.test_student.delete()

    def test_delete_identification(self):
        url = reverse("identification-detail", args=[self.test_identification.pk])
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
