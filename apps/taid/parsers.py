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
    reader = csv.reader(f)
    for row in reader:
        enrollment = _setup_enrollment(row)


def _setup_enrollment(row):
    uni_id, lec_id, tut_id, prac_id = row
    _student_model = models.get_model("taid", "Student")
    student = _student_model.objects.get(university_id=uni_id)
    if lec_id != "":
        _lecture_model = models.get_model("taid", "Lecture")
        lecture = _lecture_model.objects.get(code=lec_id)
        lecture.students.add(student)

    if tut_id != "":
        _tutorial_model = models.get_model("taid", "Tutorial")
        tutorial = _tutorial_model.objects.get(code=tut_id)
        tutorial.students.add(student)

    if prac_id != "":
        _practical_model = models.get_model("taid", "Practical")
        practical = _practical_model.objects.get(code=prac_id)
        practical.students.add(student)


def mark_parser(f):
    reader = csv.reader(f)
    for row in reader:
        mark = _setup_mark(row)


def _setup_mark(row):
    print(row)
