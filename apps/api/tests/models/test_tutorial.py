'''Test Tutorial from models'''

from django.test import TestCase
from django.db import IntegrityError

from apps.api.models import Tutorial, Student, TeachingAssistant


class TutorialTestCase(TestCase):
    '''Test Tutorial from models'''
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

    def test_tutorial_created(self):
        '''No students or teaching assistants associated'''
        tutorial = Tutorial.objects.create(
            code = "Test",
        )
        self.assertIsNotNone(tutorial)

    def test_tutorial_one_student(self):
        '''Tutorial with one student'''
        tutorial = Tutorial.objects.create(
            code = "Test",
        )
        tutorial.students.add(self.test_student1)
        self.assertIsNotNone(tutorial)

    def test_tutorial_multiple_student(self):
        '''Tutorial with multiple students'''
        tutorial = Tutorial.objects.create(
            code = "Test",
        )
        tutorial.students.add(self.test_student1)
        tutorial.students.add(self.test_student2)
        self.assertIsNotNone(tutorial)

    def test_tutorial_one_teaching_assistant(self):
        '''Tutorial with one teaching assistant'''
        tutorial = Tutorial.objects.create(
            code = "Test",
        )
        tutorial.teaching_assistant.add(self.test_assistant1)
        self.assertIsNotNone(tutorial)

    def test_tutorial_multiple_teaching_assistant(self):
        '''Tutorial with multiple students'''
        tutorial = Tutorial.objects.create(
            code = "Test",
        )
        tutorial.teaching_assistant.add(self.test_assistant1)
        tutorial.teaching_assistant.add(self.test_assistant2)
        self.assertIsNotNone(tutorial)

    def test_tutorial_student_and_teaching_assistant(self):
        '''Tutorial with students and teaching assistants'''
        tutorial = Tutorial.objects.create(
            code = "Test",
        )
        tutorial.students.add(self.test_student1)
        tutorial.students.add(self.test_student2)
        tutorial.teaching_assistant.add(self.test_assistant1)
        tutorial.teaching_assistant.add(self.test_assistant2)
        self.assertIsNotNone(tutorial)
