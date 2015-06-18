from django.db import models
import constants

class _Person(models.Model):
    utorid = models.CharField(max_length=50, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    ids = models.ManyToManyField("Identification")

class Instructor(_Person):
    pass

class TeachingAssistant(_Person):
    pass

class Student(_Person):
    number = models.PositiveIntegerField()

class Identification(models.Model):
    person = models.ForeignKey(_Person)
    description = models.CharField(max_length=500)
    value = models.CharField(max_length=100)

class Course(models.Model):
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=254)
    section = models.CharField(max_length=1, choices=constants._SECTION_CODES)
    session = models.CharField(max_length=2, choices=constants._SESSION_CODES)
