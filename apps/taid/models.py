from django.db import models
from django.core.exceptions import ValidationError

from apps.taid import parsers

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


class Lecture(models.Model):
    code = models.CharField(max_length=20)
    instructors = models.ManyToManyField("Instructor", blank=True)
    students = models.ManyToManyField("Student", blank=True)

    def __unicode__(self):
        return self.code


class Tutorial(models.Model):
    code = models.CharField(max_length=20)
    ta = models.ManyToManyField("TeachingAssistant")
    students = models.ManyToManyField("Student", blank=True)

    def __unicode__(self):
        return self.code


class Practical(models.Model):
    code = models.CharField(max_length=20)
    ta = models.ManyToManyField("TeachingAssistant")
    students = models.ManyToManyField("Student", blank=True)

    def __unicode__(self):
        return self.code


class Assignment(models.Model):
    name = models.CharField(max_length=254)
    rubric_entries = models.ManyToManyField("Rubric", blank=True, related_name="rubric_entries")

    def __unicode__(self):
        return self.name


class Rubric(models.Model):
    name = models.CharField(max_length=254)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    assignment = models.ForeignKey("Assignment")

    def __unicode__(self):
        return "{0} for {1}".format(self.name, self.assignment)


class Mark(models.Model):
    value = models.DecimalField(max_digits=6, decimal_places=2)
    student = models.ForeignKey("Student")
    rubric = models.ForeignKey("Rubric")

    def __unicode__(self):
        return "{0} ({1}): {2}/{3}".format(
            self.rubric.name,
            self.student,
            self.value,
            self.rubric.total,
        )


class StudentListFile(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    datafile = models.FileField()

    def __unicode__(self):
        return str(self.datafile)

    def save(self, *args, **kwargs):
        if self.id is None:
            parsers.student_parser(self.datafile)
        super(StudentListFile, self).save(*args, **kwargs)


class EnrollmentListFile(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    datafile = models.FileField()

    def __unicode__(self):
        return str(self.datafile)

    def save(self, *args, **kwargs):
        if self.id is None:
            parsers.enrollment_parser(self.datafile)
        super(EnrollmentListFile, self).save(*args, **kwargs)


class MarkFile(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    assignment = models.ForeignKey("Assignment")
    datafile = models.FileField()

    def __unicode__(self):
        return "Marks for {0}".format(self.assignment)

    def save(self, *args, **kwargs):
        if self.id is None:
            parsers.mark_parser(self.assignment, self.datafile)
        super(MarkFile, self).save(*args, **kwargs)
