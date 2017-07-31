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

    def test_university_id_empty(self):
        ''' If university_id is not entered it is set as ''
        '''
        teaching_assistant = TeachingAssistant.objects.create(
            first_name="Paco",
            last_name="Taco",
            email="paco@utsc.utoronto.ca",
        )
        teaching_assistant = TeachingAssistant.objects.get(university_id='')
        self.assertIsNotNone(teaching_assistant)

    def test_university_id_not_unique_1(self):
        '''Error raised when two entries have the same primary key
        '''
        TeachingAssistant.objects.create(
            first_name="Paco",
            last_name="Taco",
            email="paco@utsc.utoronto.ca",
        )

        with self.assertRaises(IntegrityError):
            TeachingAssistant.objects.create(
                first_name="Paco1",
                last_name="Taco1",
                email="paco1@utsc.utoronto.ca",
            )

    def test_university_id_not_unique_2(self):
        '''Error raised when two entries have the same primary key
        '''
        TeachingAssistant.objects.create(
            first_name="Paco",
            last_name="Taco",
            email="paco@utsc.utoronto.ca",
            university_id=999999999,
        )

        with self.assertRaises(IntegrityError):
            TeachingAssistant.objects.create(
                first_name="Paco1",
                last_name="Taco1",
                email="paco1@utsc.utoronto.ca",
                university_id=999999999,
            )

    def test_first_name_empty(self):
        '''Although it is mandatory in the admin page but it can be bypassed
        here
        '''
        teaching_assistant = TeachingAssistant.objects.create(
            university_id=999999999,
            last_name="Taco",
            email="paco@utsc.utoronto.ca",
        )
        self.assertIsNotNone(teaching_assistant)

    def test_first_name_not_unique(self):
        '''First names do not have to be unique
        '''
        teaching_assistant = TeachingAssistant.objects.create(
            university_id=1,
            first_name="Paco",
            last_name="Taco",
            email="paco@utsc.utoronto.ca",
        )

        teaching_assistant1 = TeachingAssistant.objects.create(
            university_id=2,
            first_name="Paco",
            last_name="Taco1",
            email="paco1@utsc.utoronto.ca",
        )
        self.assertIsNotNone(teaching_assistant)
        self.assertIsNotNone(teaching_assistant1)

    def test_last_name_empty(self):
        '''Although it is mandatory in the admin page but it can be bypassed
        here
        '''
        teaching_assistant = TeachingAssistant.objects.create(
            university_id=999999999,
            first_name="Paco",
            email="paco@utsc.utoronto.ca",
        )
        self.assertIsNotNone(teaching_assistant)

    def test_last_name_not_unique(self):
        '''Last names do not have to be unique
        '''
        teaching_assistant = TeachingAssistant.objects.create(
            university_id=1,
            first_name="Paco",
            last_name="Taco",
            email="paco@utsc.utoronto.ca",
        )

        teaching_assistant1 = TeachingAssistant.objects.create(
            university_id=2,
            first_name="Paco1",
            last_name="Taco",
            email="paco1@utsc.utoronto.ca",
        )
        self.assertIsNotNone(teaching_assistant)
        self.assertIsNotNone(teaching_assistant1)

    def test_email_empty(self):
        '''Although it is mandatory in the admin page but it can be bypassed
        here
        '''
        teaching_assistant = TeachingAssistant.objects.create(
            university_id=999999999,
            first_name="Paco",
            last_name="Taco",
        )
        self.assertIsNotNone(teaching_assistant)

    def test_email_not_unique(self):
        '''Emails do not have to be unique
        '''
        teaching_assistant = TeachingAssistant.objects.create(
            university_id=1,
            first_name="Paco",
            last_name="Taco",
            email="paco@utsc.utoronto.ca",
        )

        teaching_assistant1 = TeachingAssistant.objects.create(
            university_id=2,
            first_name="Paco1",
            last_name="Taco1",
            email="paco@utsc.utoronto.ca",
        )
        self.assertIsNotNone(teaching_assistant)
        self.assertIsNotNone(teaching_assistant1)
