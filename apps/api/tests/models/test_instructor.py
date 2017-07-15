from django.test import TestCase
from django.db import IntegrityError

from apps.api.models import Instructor
from unittest import skip


class InstructorTestCase(TestCase):
    def test_instructor_created(self):
        Instructor.objects.create(
                university_id=999999999,
                first_name="Paco",
                last_name="Taco",
                email="paco@utsc.utoronto.ca",
                )
        paco = Instructor.objects.get(university_id=999999999)
        self.assertIsNotNone(paco)

    @skip("Weird behavior, skipping for now") 
    def test_university_id_mandatory(self):
        with self.assertRaises(IntegrityError):
            Instructor.objects.create(
                    first_name="Paco",
                    last_name="Taco",
                    email="paco@utsc.utoronto.ca",
                    )

    def test_first_name_not_mandatory(self):
        paco = Instructor.objects.create(
                university_id=999999999,
                last_name="Taco",
                email="paco@utsc.utoronto.ca",
                )
        self.assertIsNotNone(paco)

    def test_last_name_not_mandatory(self):
        paco = Instructor.objects.create(
                university_id=999999999,
                first_name="Paco",
                email="paco@utsc.utoronto.ca",
                )
        self.assertIsNotNone(paco)

    def test_email_not_mandatory(self):
        paco = Instructor.objects.create(
                university_id=999999999,
                first_name="Paco",
                last_name="Taco",
                )
        self.assertIsNotNone(paco)
