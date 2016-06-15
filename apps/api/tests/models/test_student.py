from django.test import TestCase
from django.db import IntegrityError

from apps.api.models import Student
from unittest import skip


class StudentTestCase(TestCase):
    def test_student_created(self):
        Student.objects.create(
                university_id=999999999,
                first_name="Paco",
                last_name="Taco",
                email="paco@utsc.utoronto.ca",
                student_number=111111111,
                )
        paco = Student.objects.get(university_id=999999999)
        self.assertIsNotNone(paco)

    @skip("Weird behavior, skipping for now") 
    def test_university_id_mandatory(self):
        with self.assertRaises(IntegrityError):
            paco = Student.objects.create(
                    first_name="Paco",
                    last_name="Taco",
                    email="paco@utsc.utoronto.ca",
                    student_number=111111111,
                    )

    def test_first_name_not_mandatory(self):
        paco = Student.objects.create(
                university_id=999999999,
                last_name="Taco",
                email="paco@utsc.utoronto.ca",
                student_number=111111111,
                )
        self.assertIsNotNone(paco)

    def test_last_name_not_mandatory(self):
        paco = Student.objects.create(
                university_id=999999999,
                first_name="Paco",
                email="paco@utsc.utoronto.ca",
                student_number=111111111,
                )
        self.assertIsNotNone(paco)

    def test_email_not_mandatory(self):
        paco = Student.objects.create(
                university_id=999999999,
                first_name="Paco",
                last_name="Taco",
                student_number=111111111,
                )
        self.assertIsNotNone(paco)

    def test_student_number_not_mandatory(self):
        paco = Student.objects.create(
                university_id=999999999,
                first_name="Paco",
                last_name="Taco",
                )
        self.assertIsNotNone(paco)
