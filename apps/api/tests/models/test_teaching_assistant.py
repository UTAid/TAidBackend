'''Test Teaching Assistant from models'''

from django.test import TestCase
from django.db import IntegrityError

from apps.api.models import TeachingAssistant


class TeachingAssistantTestCase(TestCase):
    '''Test Teaching Assistant from models'''

    def test_teaching_assistant_created(self):
        '''Properly created teaching assistant with all the necessary info
        '''
        TeachingAssistant.objects.create(
            university_id=999999999,
            first_name="Paco",
            last_name="Taco",
            email="paco@utsc.utoronto.ca",
        )
        paco = TeachingAssistant.objects.get(university_id=999999999)
        self.assertIsNotNone(paco)

    def test_university_id_not_mandatory_for_first(self):
        ''' If university_id is not entered it is set as ''
        '''
        paco = TeachingAssistant.objects.create(
            first_name="Paco",
            last_name="Taco",
            email="paco@utsc.utoronto.ca",
        )
        paco = TeachingAssistant.objects.get(university_id='')
        self.assertIsNotNone(paco)

    def test_university_id_mandatory(self):
        '''Error raised when two entries have the same primary key
        '''
        TeachingAssistant.objects.create(
            first_name="Paco",
            last_name="Taco",
            email="paco@utsc.utoronto.ca",
        )

        with self.assertRaises(IntegrityError):
            TeachingAssistant.objects.create(
                first_name="Paco",
                last_name="Taco",
                email="paco@utsc.utoronto.ca",
            )

    def test_first_name_not_mandatory(self):
        '''Although it is mandatory in the admin page but it can be bypassed
        here
        '''
        paco = TeachingAssistant.objects.create(
            university_id=999999999,
            last_name="Taco",
            email="paco@utsc.utoronto.ca",
        )
        self.assertIsNotNone(paco)

    def test_last_name_not_mandatory(self):
        '''Although it is mandatory in the admin page but it can be bypassed
        here
        '''
        paco = TeachingAssistant.objects.create(
            university_id=999999999,
            first_name="Paco",
            email="paco@utsc.utoronto.ca",
        )
        self.assertIsNotNone(paco)

    def test_email_not_mandatory(self):
        '''Although it is mandatory in the admin page but it can be bypassed
        here
        '''
        paco = TeachingAssistant.objects.create(
            university_id=999999999,
            first_name="Paco",
            last_name="Taco",
        )
        self.assertIsNotNone(paco)
