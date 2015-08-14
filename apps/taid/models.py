from django.db import models
from django.core.exceptions import ValidationError

import constants


class _UniversityMember(models.Model):
    university_id = models.CharField(max_length=50, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()

    def __unicode__(self):
        return "{0} {1}".format(self.first_name, self.last_name)


class Teacher(_UniversityMember):
    pass


class Instructor(Teacher):
    pass


class TeachingAssistant(Teacher):
    pass


class Student(_UniversityMember):
    student_number = models.CharField(max_length=10, blank=True)


class Identification(models.Model):
    value = models.CharField(max_length=100)
    student = models.ForeignKey(Student)
    description = models.CharField(max_length=500, blank=True)


class Course(models.Model):
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=254)
    section_code = models.CharField(max_length=1, choices=constants._SECTION_CODES)
    lecture_session = models.CharField(max_length=2, choices=constants._SESSION_CODES)
    instructors = models.ManyToManyField("Instructor", blank=True)
    students = models.ManyToManyField("Student", blank=True)

    def __unicode__(self):
        return self.code


class Tutorial(models.Model):
    code = models.CharField(max_length=20)
    course = models.ForeignKey(Course)
    ta = models.ManyToManyField("TeachingAssistant")

    def __unicode__(self):
        return self.code


class Practical(models.Model):
    code = models.CharField(max_length=20)
    course = models.ForeignKey(Course)
    ta = models.ManyToManyField("TeachingAssistant")

    def __unicode__(self):
        return self.code


class Assignment(models.Model):
    name = models.CharField(max_length=254)
    total = models.DecimalField(max_digits=6, decimal_places=3)
    parent = models.ForeignKey("self", null=True, blank=True, related_name="subparts")
    marks = models.ManyToManyField("Mark", blank=True, related_name="student_marks")

    def __unicode__(self):
        return self.name


class Mark(models.Model):
    value = models.DecimalField(max_digits=6, decimal_places=3)
    student = models.ForeignKey("Student")
    assignment = models.ForeignKey("Assignment")

    def __unicode__(self):
        return "{0} ({1}): {2}/{3}".format(
                self.assignment.name,
                self.student,
                self.value,
                self.assignment.total,
                )
