from django.db import models
from schedule.models.events import Event
from schedule.models.calendars import Calendar
import constants


class _Person(models.Model):
    utorid = models.CharField(max_length=50, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()

    def __unicode__(self):
        return "{0} {1}".format(self.first_name, self.last_name)


class Instructor(_Person):
    pass


class TeachingAssistant(Instructor):
    pass


class Student(_Person):
    number = models.PositiveIntegerField()
    ids = models.ManyToManyField("Identification", blank=True)


class Identification(models.Model):
    description = models.CharField(max_length=500)
    value = models.CharField(max_length=100)


class Course(models.Model):
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=254)
    calendar = models.ForeignKey(Calendar)
    section = models.CharField(max_length=1, choices=constants._SECTION_CODES)
    session = models.CharField(max_length=2, choices=constants._SESSION_CODES)
    instructors = models.ManyToManyField("Instructor", blank=True)
    students = models.ManyToManyField("Student", blank=True)
    tuts = models.ManyToManyField("Tutorial", blank=True)
    pracs = models.ManyToManyField("Practical", blank=True)

    def __unicode__(self):
        return self.code


class Tutorial(Event):
    ta = models.ForeignKey(Instructor)

    def __unicode__(self):
        return self.title


class Practical(Event):
    ta = models.ForeignKey(Instructor)

    def __unicode__(self):
        return self.title
