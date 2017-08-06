'''Test Assignment from models'''

from django.test import TestCase
from django.db import IntegrityError

from apps.api.models import Assignment, Rubric


class AssignmentTestCase(TestCase):
    '''Test Assignment from models'''

    def test_assignment_created(self):
        assignment = Assignment.objects.create(
            name = "Test Assignment",
        )
        assignment.rubric_entries.create(
            name = "Rubric",
            total = 100,
            assignment = assignment,
        )
        self.assertIsNotNone(assignment)

    def test_assignment_multiple_rubric(self):
        assignment = Assignment.objects.create(
            name = "Test Assignment",
        )
        assignment.rubric_entries.create(
            name = "Rubric1",
            total = 100,
            assignment = assignment,
        )
        assignment.rubric_entries.create(
            name = "Rubric2",
            total = 150,
            assignment = assignment,
        )
        self.assertIsNotNone(assignment)
