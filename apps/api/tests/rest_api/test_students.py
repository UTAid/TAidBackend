from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from apps.api.models import Student
from apps.api.viewsets import StudentViewSet


class CreateStudentTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(username="omg", email="omg@omg.com", password="omg")

    def tearDown(self):
        self.auth_user.delete()

    def test_create_student(self):
        url = reverse("student-list")
        data = {
                "university_id": "pacotaco",
                "first_name": "Paco",
                "last_name": "Taco",
                "email": "paco@taco.com",
                "student_number": 999999999,
               }
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(Student.objects.get().university_id, "pacotaco")


class ReadStudentTests(APITestCase):
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

    def test_read_student_list(self):
        url = reverse("student-list")
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_student_list(self):
        url = reverse("student-detail", args=[self.test_student.pk])
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UpdateStudentTests(APITestCase):
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

    def test_update_student(self):
        url = reverse("student-detail", args=[self.test_student.pk])
        data = {
                "university_id": "pacotaco",
                "first_name": "Paco",
                "last_name": "Taco",
                "email": "paco@taco.com",
                "student_number": 123456789,
               }
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteStudentTests(APITestCase):
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

    def test_delete_student(self):
        url = reverse("student-detail", args=[self.test_student.pk])
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
