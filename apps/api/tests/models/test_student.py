'''Test Student from models'''

from django.test import TestCase
from django.db import IntegrityError

from apps.api.models import Student


class StudentTestCase(TestCase):
    '''Test Student from models'''

    def test_student_created(self):
        '''Properly created student with all the necessary info
        '''
        Student.objects.create(
            university_id=999999999,
            first_name="Paco",
            last_name="Taco",
            email="paco@utsc.utoronto.ca",
            student_number=111111111,
        )
        student = Student.objects.get(university_id=999999999)
        self.assertIsNotNone(student)

    def test_university_id_empty(self):
        ''' If university_id is not entered it is set as ''
        '''
        student = Student.objects.create(
            first_name="Paco",
            last_name="Taco",
            email="paco@utsc.utoronto.ca",
            student_number=111111111,
        )
        student = Student.objects.get(university_id='')
        self.assertIsNotNone(student)

    def test_university_id_not_unique_1(self):
        '''Error raised when two entries have the same primary key
        '''
        Student.objects.create(
            first_name="Paco",
            last_name="Taco",
            email="paco@utsc.utoronto.ca",
            student_number=111111111,
        )

        with self.assertRaises(IntegrityError):
            Student.objects.create(
                first_name="Paco1",
                last_name="Taco1",
                email="paco1@utsc.utoronto.ca",
                student_number=222222222,
            )

    def test_university_id_not_unique_2(self):
        '''Error raised when two entries have the same primary key
        '''
        Student.objects.create(
            first_name="Paco",
            last_name="Taco",
            email="paco@utsc.utoronto.ca",
            student_number=111111111,
            university_id=999999999,
        )

        with self.assertRaises(IntegrityError):
            Student.objects.create(
                first_name="Paco1",
                last_name="Taco1",
                email="paco1@utsc.utoronto.ca",
                student_number=222222222,
                university_id=999999999,
            )

    def test_first_name_empty(self):
        '''Although it is mandatory in the admin page but it can be bypassed
        here
        '''
        student = Student.objects.create(
            student_number=111111111,
            university_id=999999999,
            last_name="Taco",
            email="paco@utsc.utoronto.ca",
        )
        self.assertIsNotNone(student)

    def test_first_name_not_unique(self):
        '''First names do not have to be unique
        '''
        student = Student.objects.create(
            student_number=111111111,
            university_id=1,
            first_name="Paco",
            last_name="Taco",
            email="paco@utsc.utoronto.ca",
        )

        student1 = Student.objects.create(
            student_number=222222222,
            university_id=2,
            first_name="Paco",
            last_name="Taco1",
            email="paco1@utsc.utoronto.ca",
        )
        self.assertIsNotNone(student)
        self.assertIsNotNone(student1)

    def test_last_name_empty(self):
        '''Although it is mandatory in the admin page but it can be bypassed
        here
        '''
        student = Student.objects.create(
            student_number=111111111,
            university_id=999999999,
            first_name="Paco",
            email="paco@utsc.utoronto.ca",
        )
        self.assertIsNotNone(student)

    def test_last_name_not_unique(self):
        '''Last names do not have to be unique
        '''
        student = Student.objects.create(
            student_number=111111111,
            university_id=1,
            first_name="Paco",
            last_name="Taco",
            email="paco@utsc.utoronto.ca",
        )

        student1 = Student.objects.create(
            student_number=222222222,
            university_id=2,
            first_name="Paco1",
            last_name="Taco",
            email="paco1@utsc.utoronto.ca",
        )
        self.assertIsNotNone(student)
        self.assertIsNotNone(student1)

    def test_email_empty(self):
        '''Although it is mandatory in the admin page but it can be bypassed
        here
        '''
        student = Student.objects.create(
            student_number=111111111,
            university_id=999999999,
            first_name="Paco",
            last_name="Taco",
        )
        self.assertIsNotNone(student)

    def test_email_not_unique(self):
        '''Emails do not have to be unique
        '''
        student = Student.objects.create(
            student_number=111111111,
            university_id=1,
            first_name="Paco",
            last_name="Taco",
            email="paco@utsc.utoronto.ca",
        )

        student1 = Student.objects.create(
            student_number=222222222,
            university_id=2,
            first_name="Paco1",
            last_name="Taco1",
            email="paco@utsc.utoronto.ca",
        )
        self.assertIsNotNone(student)
        self.assertIsNotNone(student1)

    def test_student_number_empty(self):
        '''Although it is mandatory in the admin page but it can be bypassed
        here
        '''
        student = Student.objects.create(
            university_id=999999999,
            first_name="Paco",
            last_name="Taco",
            email="paco@utsc.utoronto.ca",
        )
        self.assertIsNotNone(student)

    def test_student_number_not_unique(self):
        '''Student number do not have to be unique
        '''
        student = Student.objects.create(
            student_number=111111111,
            university_id=1,
            first_name="Paco",
            last_name="Taco",
            email="paco@utsc.utoronto.ca",
        )

        student1 = Student.objects.create(
            student_number=111111111,
            university_id=2,
            first_name="Paco1",
            last_name="Taco1",
            email="paco1@utsc.utoronto.ca",
        )
        self.assertIsNotNone(student)
        self.assertIsNotNone(student1)

    def test_student_number_too_long(self):
        '''Although it is mandatory in the admin page but it can be bypassed
        here
        '''
        student = Student.objects.create(
            student_number=11111111111,
            university_id=2,
            first_name="Paco1",
            last_name="Taco1",
            email="paco1@utsc.utoronto.ca",
        )
        self.assertIsNotNone(student)
