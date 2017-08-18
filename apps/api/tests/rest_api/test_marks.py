from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from apps.api.models import Mark, Rubric, Student, Assignment


class CreateMarkTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(
            username="omg", email="omg@omg.com", password="omg")

        self.test_student1 = Student.objects.create(
            university_id=1,
            first_name="Paco",
            last_name="Taco",
            email="paco@utsc.utoronto.ca",
            student_number=1,
        )
        assignment1 = Assignment.objects.create(
            name="Test Assignment1",
        )
        self.rubric1 = Rubric.objects.create(
            name="Test Rubric 1",
            total=100,
            assignment=assignment1,
        )

    def tearDown(self):
        self.auth_user.delete()
        self.rubric1.delete()

    def test_create_mark(self):
        url = reverse("mark-list")

        data = {
            "value": 20,
            "student": self.test_student1.pk,
            "rubric": self.rubric1.pk,
        }
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Mark.objects.count(), 1)


class ReadAssignmentTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(
            username="omg", email="omg@omg.com", password="omg")

        test_student1 = Student.objects.create(
            university_id=1,
            first_name="Paco",
            last_name="Taco",
            email="paco@utsc.utoronto.ca",
            student_number=1,
        )
        assignment1 = Assignment.objects.create(
            name="Test Assignment1",
        )
        rubric1 = Rubric.objects.create(
            name="Test Rubric 1",
            total=100,
            assignment=assignment1,
        )
        self.mark = Mark.objects.create(
            value=100,
            student=test_student1,
            rubric=rubric1,
        )

    def tearDown(self):
        self.auth_user.delete()
        self.mark.delete()

    def test_read_mark_list(self):
        url = reverse("mark-list")
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_mark_list(self):
        url = reverse("mark-detail", args=[self.mark.pk])
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UpdateAssignmentTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(
            username="omg", email="omg@omg.com", password="omg")

        self.test_student1 = Student.objects.create(
            university_id=1,
            first_name="Paco",
            last_name="Taco",
            email="paco@utsc.utoronto.ca",
            student_number=1,
        )
        self.assignment1 = Assignment.objects.create(
            name="Test Assignment1",
        )
        self.rubric1 = Rubric.objects.create(
            name="Test Rubric 1",
            total=100,
            assignment=self.assignment1,
        )
        self.mark = Mark.objects.create(
            value=100,
            student=self.test_student1,
            rubric=self.rubric1,
        )

    def tearDown(self):
        self.auth_user.delete()
        self.test_student1.delete()
        self.rubric1.delete()
        self.mark.delete()

    def test_update_mark(self):
        url = reverse("mark-detail", args=[self.mark.pk])
        data = {
            "value": 9000,
            "student": self.test_student1.pk,
            "rubric": self.rubric1.pk,
        }
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteMarkTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(
            username="omg", email="omg@omg.com", password="omg")

        test_student1 = Student.objects.create(
            university_id=1,
            first_name="Paco",
            last_name="Taco",
            email="paco@utsc.utoronto.ca",
            student_number=1,
        )
        assignment1 = Assignment.objects.create(
            name="Test Assignment1",
        )
        rubric1 = Rubric.objects.create(
            name="Test Rubric 1",
            total=100,
            assignment=assignment1,
        )
        self.mark = Mark.objects.create(
            value=100,
            student=test_student1,
            rubric=rubric1,
        )

    def tearDown(self):
        self.auth_user.delete()
        self.mark.delete()

    def test_delete_mark(self):
        url = reverse("mark-detail", args=[self.mark.pk])
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
