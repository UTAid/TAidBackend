'''Test Lecture from models'''

from django.test import TestCase

from apps.api.models import Lecture, Instructor, Student

class LectureTestCase(TestCase):
    '''Test Lecture from models'''

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

        self.test_instructor1 = Instructor.objects.create(
            university_id=3,
            first_name="Paco",
            last_name="Taco",
            email="paco@utsc.utoronto.ca",
        )

        self.test_instructor2 = Instructor.objects.create(
            university_id=4,
            first_name="Paco",
            last_name="Taco",
            email="paco@utsc.utoronto.ca",
        )

    def tearDown(self):
        self.test_student1.delete()
        self.test_student2.delete()
        self.test_instructor1.delete()
        self.test_instructor2.delete()

    def test_lecture_created(self):
        pass
