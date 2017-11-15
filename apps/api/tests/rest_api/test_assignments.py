from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from apps.api.models import Assignment, Rubric


class CreateAssignmentTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(
            username="omg", email="omg@omg.com", password="omg")

    def tearDown(self):
        self.auth_user.delete()

    def test_create_assignment(self):
        url = reverse("assignment-list")

        data = {
            "name": "Test",
        }
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Assignment.objects.count(), 1)


class ReadAssignmentTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(
            username="omg", email="omg@omg.com", password="omg")
        self.test_assignment = Assignment.objects.create(
            name="Test Assignment",
        )

    def tearDown(self):
        self.auth_user.delete()
        self.test_assignment.delete()

    def test_read_assignment_list(self):
        url = reverse("assignment-list")
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_assignment_list(self):
        url = reverse("assignment-detail", args=[self.test_assignment.pk])
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UpdateAssignmentTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(
            username="omg", email="omg@omg.com", password="omg")
        self.test_assignment = Assignment.objects.create(
            name="Test Assignment",
        )
        self.test_assignment.rubric_entries.create(
            name="Test",
            total=100,
            assignment=self.test_assignment,
        )

    def tearDown(self):
        self.auth_user.delete()
        self.test_assignment.delete()

    def test_update_assignment(self):
        url = reverse("assignment-detail", args=[self.test_assignment.pk])
        data = {
            "name": "New Test Assignment",
        }
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteIdentificationTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(
            username="omg", email="omg@omg.com", password="omg")
        self.test_assignment = Assignment.objects.create(
            name="Test Assignment",
        )
        self.test_assignment.rubric_entries.create(
            name="Test",
            total=100,
            assignment=self.test_assignment,
        )

    def tearDown(self):
        self.auth_user.delete()
        self.test_assignment.delete()

    def test_delete_assignment(self):
        url = reverse("assignment-detail", args=[self.test_assignment.pk])
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
