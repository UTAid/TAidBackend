'''Test Identification from models'''

from django.test import TestCase

from apps.api.models import Identification, Student


class IdentificationTestCase(TestCase):
    '''Test Identification from models'''

    def setUp(self):
        self.test_student = Student.objects.create(
            university_id=999999999,
            first_name="Paco",
            last_name="Taco",
            email="paco@utsc.utoronto.ca",
            student_number=111111111,
        )

    def tearDown(self):
        self.test_student.delete()

    def test_identification_created(self):
        identification = Identification.objects.create(
            value='1',
            student=self.test_student,
            description="Test",
            number=1,
        )
        self.assertEquals(self.test_student.identification_set.count(), 1)
        self.assertIsNotNone(identification)

    def test_empty_value(self):
        identification = Identification.objects.create(
            student=self.test_student,
            description="Test",
            number=1,
        )
        self.assertIsNotNone(identification)

    def test_empty_description(self):
        identification = Identification.objects.create(
            value='1',
            student=self.test_student,
            number=1,
        )
        self.assertIsNotNone(identification)

    def test_create_with_least_param(self):
        identification = Identification.objects.create(
            student=self.test_student,
            number=1,
        )
        self.assertIsNotNone(identification)

    def test_identification_multiple_created(self):
        identification1 = Identification.objects.create(
            value='1',
            student=self.test_student,
            description="Test",
            number=1,
        )
        identification2 = Identification.objects.create(
            value='1',
            student=self.test_student,
            description="Test",
            number=1,
        )
        self.assertEquals(self.test_student.identification_set.count(), 2)
        self.assertIsNotNone(identification1)
        self.assertIsNotNone(identification2)
