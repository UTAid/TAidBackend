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
        paco = Student.objects.get(university_id=999999999)
        self.assertIsNotNone(paco)

    def test_university_id_not_mandatory_for_first(self):
        ''' If university_id is not entered it is set as ''
        '''
        paco = Student.objects.create(
            first_name="Paco",
            last_name="Taco",
            email="paco@utsc.utoronto.ca",
            student_number=111111111,
        )
        paco = Student.objects.get(university_id='')
        self.assertIsNotNone(paco)

    def test_university_id_mandatory(self):
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
                first_name="Paco",
                last_name="Taco",
                email="paco@utsc.utoronto.ca",
                student_number=111111111,
            )

    def test_first_name_not_mandatory(self):
        '''Although it is mandatory in the admin page but it can be bypassed
        here
        '''
        paco = Student.objects.create(
            university_id=999999999,
            last_name="Taco",
            email="paco@utsc.utoronto.ca",
            student_number=111111111,
        )
        self.assertIsNotNone(paco)

    def test_last_name_not_mandatory(self):
        '''Although it is mandatory in the admin page but it can be bypassed
        here
        '''
        paco = Student.objects.create(
            university_id=999999999,
            first_name="Paco",
            email="paco@utsc.utoronto.ca",
            student_number=111111111,
        )
        self.assertIsNotNone(paco)

    def test_email_not_mandatory(self):
        '''Although it is mandatory in the admin page but it can be bypassed
        here
        '''
        paco = Student.objects.create(
            university_id=999999999,
            first_name="Paco",
            last_name="Taco",
            student_number=111111111,
        )
        self.assertIsNotNone(paco)

    def test_student_number_not_mandatory(self):
        '''Although it is mandatory in the admin page but it can be bypassed
        here
        '''
        paco = Student.objects.create(
            university_id=999999999,
            first_name="Paco",
            last_name="Taco",
        )
        self.assertIsNotNone(paco)
