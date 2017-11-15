'''Creates the database'''

from django.db import models
from schedule.models.events import Event
from apps.api import parsers
from apps.api.validators import validate_csv, ValidationError


class _UniversityMember(models.Model):
    university_id = models.CharField(max_length=50, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()

    class Meta:
        abstract = True

    def __str__(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def __unicode__(self):
        return "{0} {1}".format(self.first_name, self.last_name)


class Teacher(_UniversityMember):
    pass


class Instructor(Teacher):
    pass


class TeachingAssistant(Teacher):
    pass


class TaidEvent(Event):
    pass


class Student(_UniversityMember):
    student_number = models.CharField(max_length=10, blank=True)


class Identification(models.Model):
    value = models.CharField(max_length=100)
    student = models.ForeignKey(Student)
    description = models.CharField(max_length=500, blank=True)
    number = models.PositiveIntegerField()

    def __str__(self):
        return str(self.student)

    def __unicode__(self):
        return str(self.student)


class Lecture(models.Model):
    code = models.CharField(max_length=20)
    instructors = models.ManyToManyField("Instructor", blank=True)
    event = models.ForeignKey("TAidEvent", null=True, blank=True)
    students = models.ManyToManyField("Student", blank=True)

    def __str__(self):
        return self.code

    def __unicode__(self):
        return self.code


class Tutorial(models.Model):
    code = models.CharField(max_length=20)
    teaching_assistant = models.ManyToManyField(
        "TeachingAssistant", blank=True, verbose_name='Teaching Assistant(s)')
    event = models.ForeignKey("TAidEvent", null=True, blank=True)
    students = models.ManyToManyField("Student", blank=True)

    def __str__(self):
        return self.code

    def __unicode__(self):
        return self.code


class Practical(models.Model):
    code = models.CharField(max_length=20)
    teaching_assistant = models.ManyToManyField(
        "TeachingAssistant", blank=True, verbose_name='Teaching Assistant(s)')
    event = models.ForeignKey("TAidEvent", null=True, blank=True)
    students = models.ManyToManyField("Student", blank=True)

    def __str__(self):
        return self.code

    def __unicode__(self):
        return self.code


class Assignment(models.Model):
    name = models.CharField(max_length=254)
    rubric_entries = models.ManyToManyField(
        "Rubric", blank=True, related_name="rubric_entries")

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Rubric(models.Model):
    name = models.CharField(max_length=254)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    assignment = models.ForeignKey("Assignment", blank=True)

    def __str__(self):
        return "{0} for {1}".format(self.name, self.assignment)

    def __unicode__(self):
        return "{0} for {1}".format(self.name, self.assignment)


class Mark(models.Model):
    value = models.DecimalField(max_digits=6, decimal_places=2)
    student = models.ForeignKey("Student")
    rubric = models.ForeignKey("Rubric")

    def __str__(self):
        return "{0} ({1}): {2}/{3}".format(
            self.rubric.name,
            self.student,
            self.value,
            self.rubric.total,
        )

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

    def __str__(self):
        return str(self.datafile)

    def __unicode__(self):
        return str(self.datafile)

    def save(self, *args, **kwargs):
        status = False

        try:
            validate_csv(self.datafile)
            status = True
        except ValidationError:
            status = False

        if status:
            student_list = parsers.StudentList(self.datafile)
            student_list.parse()
            super(StudentListFile, self).save(*args, **kwargs)


class EnrollmentListFile(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    datafile = models.FileField()

    def __str__(self):
        return str(self.datafile)

    def __unicode__(self):
        return str(self.datafile)

    def save(self, *args, **kwargs):
        status = False

        try:
            validate_csv(self.datafile)
            status = True
        except ValidationError:
            status = False

        if status:
            enrollment_list = parsers.EnrollmentList(self.datafile)
            enrollment_list.parse()
            super(EnrollmentListFile, self).save(*args, **kwargs)


class MarkFile(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    assignment = models.ForeignKey("Assignment")
    datafile = models.FileField()

    def __str__(self):
        return "Marks for {0}".format(self.assignment)

    def __unicode__(self):
        return "Marks for {0}".format(self.assignment)

    def save(self, *args, **kwargs):
        status = False

        try:
            validate_csv(self.datafile)
            status = True
        except ValidationError:
            status = False

        if status:
            mark_file = parsers.MarkFile(self.datafile)
            mark_file.parse()
            super(MarkFile, self).save(*args, **kwargs)


class TAListFile(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    datafile = models.FileField()

    def __str__(self):
        return str(self.datafile)

    def __unicode__(self):
        return str(self.datafile)

    def save(self, *args, **kwargs):
        status = False

        try:
            validate_csv(self.datafile)
            status = True
        except ValidationError:
            status = False

        if status:
            ta_list = parsers.TAList(self.datafile)
            ta_list.parse()
            super(TAListFile, self).save(*args, **kwargs)
