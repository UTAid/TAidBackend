'''Test Practical from models'''

from django.test import TestCase
from django.db import IntegrityError

from apps.api.models import Practical, Student, TeachingAssistant


class PracticalTestCase(TestCase):
    '''Test Practical from models'''

    def setUp(self):
        self.test_student1 = Student.objects.create(
            university_id=1,
            first_name="Paco",
            last_name="Taco",
            email="paco@utsc.utoronto.ca",
            student_number=1,
        )

        self.test_student2 = Student.objects.create(
            university_id=2,
            first_name="Paco",
            last_name="Taco",
            email="paco@utsc.utoronto.ca",
            student_number=2,
        )

        self.test_assistant1 = TeachingAssistant.objects.create(
            university_id=3,
            first_name="Paco",
            last_name="Taco",
            email="paco@utsc.utoronto.ca",
        )

        self.test_assistant2 = TeachingAssistant.objects.create(
            university_id=4,
            first_name="Paco",
            last_name="Taco",
            email="paco@utsc.utoronto.ca",
        )

    def tearDown(self):
        self.test_student1.delete()
        self.test_student2.delete()
        self.test_assistant1.delete()
        self.test_assistant2.delete()

    def test_practical_created(self):
        '''No students or teaching assistants associated'''
        practical = Practical.objects.create(
            code="Test",
        )
        self.assertIsNotNone(practical)

    def test_practical_one_student(self):
        '''Practical with one student'''
        practical = Practical.objects.create(
            code="Test",
        )
        practical.students.add(self.test_student1)
        self.assertIsNotNone(practical)

    def test_practical_multiple_student(self):
        '''Practical with multiple students'''
        practical = Practical.objects.create(
            code="Test",
        )
        practical.students.add(self.test_student1)
        practical.students.add(self.test_student2)
        self.assertIsNotNone(practical)

    def test_practical_one_teaching_assistant(self):
        '''Practical with one teaching assistant'''
        practical = Practical.objects.create(
            code="Test",
        )
        practical.teaching_assistant.add(self.test_assistant1)
        self.assertIsNotNone(practical)

    def test_practical_multiple_teaching_assistant(self):
        '''Practical with multiple students'''
        practical = Practical.objects.create(
            code="Test",
        )
        practical.teaching_assistant.add(self.test_assistant1)
        practical.teaching_assistant.add(self.test_assistant2)
        self.assertIsNotNone(practical)

    def test_practical_student_and_teaching_assistant(self):
        '''Practical with students and teaching assistants'''
        practical = Practical.objects.create(
            code="Test",
        )
        practical.students.add(self.test_student1)
        practical.students.add(self.test_student2)
        practical.teaching_assistant.add(self.test_assistant1)
        practical.teaching_assistant.add(self.test_assistant2)
        self.assertIsNotNone(practical)
