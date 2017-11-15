'''Test Rubric from models'''

from django.test import TestCase
from django.db import IntegrityError

from apps.api.models import Rubric, Assignment, Student, Mark


class RubricTestCase(TestCase):
    '''Test Rubric from models'''

    def setUp(self):
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

    def tearDown(self):
        self.test_student1.delete()
        self.assignment1.delete()

    def test_rubric_created(self):
        rubric = Rubric.objects.create(
            name="Test Rubric 1",
            total=100,
            assignment=self.assignment1,
        )
        self.assertIsNotNone(rubric)

    def test_rubric_one_mark(self):
        rubric = Rubric.objects.create(
            name="Test Rubric 1",
            total=100,
            assignment=self.assignment1,
        )
        rubric.mark_set.create(
            value=20,
            student=self.test_student1,
        )
        self.assertEquals(rubric.mark_set.count(), 1)
        self.assertIsNotNone(rubric)

    def test_rubric_multiple_mark(self):
        rubric = Rubric.objects.create(
            name="Test Rubric 1",
            total=100,
            assignment=self.assignment1,
        )
        rubric.mark_set.create(
            value=20,
            student=self.test_student1,
        )
        rubric.mark_set.create(
            value=55,
            student=self.test_student1,
        )
        self.assertEquals(rubric.mark_set.count(), 2)
        self.assertIsNotNone(rubric)
