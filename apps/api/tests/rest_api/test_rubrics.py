from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from apps.api.models import Assignment, Rubric


class CreateRubricTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(username="omg", email="omg@omg.com", password="omg")

        self.assignment1 = Assignment.objects.create(
            name = "Test Assignment1",
        )

    def tearDown(self):
        self.auth_user.delete()
        self.assignment1.delete()

    def test_create_rubric(self):
        url = reverse("rubric-list")

        data = {
                "name": "Test",
                "total": 100,
                "assignment" : self.assignment1.pk,
               }
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rubric.objects.count(), 1)



class ReadRubricTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(username="omg", email="omg@omg.com", password="omg")

        assignment1 = Assignment.objects.create(
            name = "Test Assignment1",
        )
        self.rubric = Rubric.objects.create(
            name = "Test Rubric",
            total = 100,
            assignment = assignment1,
        )


    def tearDown(self):
        self.auth_user.delete()
        self.rubric.delete()

    def test_read_rubric_list(self):
        url = reverse("rubric-list")
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_assignment_list(self):
        url = reverse("rubric-detail", args=[self.rubric.pk])
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UpdateRubricTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(username="omg", email="omg@omg.com", password="omg")

        assignment1 = Assignment.objects.create(
            name = "Test Assignment1",
        )
        self.rubric = Rubric.objects.create(
            name = "Test Rubric",
            total = 100,
            assignment = assignment1,
        )


    def tearDown(self):
        self.auth_user.delete()
        self.rubric.delete()

    def test_update_rubric(self):
        url = reverse("rubric-detail", args=[self.rubric.pk])
        data = {
                "name": "New Test Rubric",
                "total": 50,
               }
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteRubricTests(APITestCase):
    def setUp(self):
        self.auth_user = User.objects.create_user(username="omg", email="omg@omg.com", password="omg")

        assignment1 = Assignment.objects.create(
            name = "Test Assignment1",
        )
        self.rubric = Rubric.objects.create(
            name = "Test Rubric",
            total = 100,
            assignment = assignment1,
        )

    def tearDown(self):
        self.auth_user.delete()
        self.rubric.delete()

    def test_delete_rubric(self):
        url = reverse("rubric-detail", args=[self.rubric.pk])
        self.client.force_authenticate(user=self.auth_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
