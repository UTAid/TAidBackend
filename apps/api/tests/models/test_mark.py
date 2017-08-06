'''Test Mark from models'''

from django.test import TestCase
from django.db import IntegrityError

from apps.api.models import Mark, Student, Rubric, Assignment


class MarkTestCase(TestCase):
    '''Test Mark from models'''

    def setUp(self):
        self.test_student1 = Student.objects.create(
            university_id=1,
            first_name="Paco",
            last_name="Taco",
            email="paco@utsc.utoronto.ca",
            student_number=1,
        )
        self.assignment1 = Assignment.objects.create(
            name = "Test Assignment1",
        )
        self.rubric1 = Rubric.objects.create(
            name = "Test Rubric 1",
            total = 100,
            assignment = self.assignment1,
        )

    def tearDown(self):
        self.test_student1.delete()
        self.assignment1.delete()
        self.rubric1.delete()

    def test_mark_created(self):
        mark = Mark.objects.create(
            value = 20,
            student = self.test_student1,
            rubric = self.rubric1,
        )
        self.assertIsNotNone(mark)
