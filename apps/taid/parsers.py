from django.db import models
from django.core.exceptions import ValidationError

import csv


def student_parser(f):
    reader = csv.reader(f)
    for row in reader:
        student = _setup_student(row)

def _setup_student(row):
    info, ids = row[:5], row[5:]
    uni_id, last_name, first_name, number, email = info

    # Create the student
    _student_model = models.get_model("taid", "Student")
    student = _student_model.objects.create(
            university_id=uni_id,
            first_name=first_name,
            last_name=last_name,
            student_number=number,
            email=email,
            )

    for val in ids:
        student.identification_set.create(value=val)

    return student

def enrollment_parser(f):
    pass

def mark_parser(f):
    pass
