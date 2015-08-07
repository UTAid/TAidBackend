from django.db import models
from schedule.models.events import Event
from schedule.models.calendars import Calendar
from django.core.exceptions import ValidationError
from django.db import connection
import constants


class _Person(models.Model):
    utorid = models.CharField(max_length=50, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()

    def __unicode__(self):
        return "{0} {1}".format(self.first_name, self.last_name)


class Teacher(_Person):
    pass


class Instructor(Teacher):
    pass


class TeachingAssistant(Teacher):
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
    section = models.CharField(max_length=1, verbose_name="Section Code", choices=constants._SECTION_CODES)
    lecture_sections = models.CommaSeparatedIntegerField(max_length=50, blank=True, verbose_name="Lecture Section (Comman Seperated)")
    instructors = models.ManyToManyField("Instructor", blank=True)
    students = models.ManyToManyField("Student", blank=True)
    tuts = models.ManyToManyField("Tutorial", blank=True)
    pracs = models.ManyToManyField("Practical", blank=True)

    def __unicode__(self):
        return self.code

class Tutorial(Event):
    code = models.CharField(max_length=20)
    ta = models.ForeignKey(Teacher, null=True, blank=True)

    def _getCourseName(self):
        string = "";
        cursor = connection.cursor()
        sql = 'SELECT code from taid_course_tuts tact INNER JOIN taid_course tac ON tact.tutorial_id=' + str(self.id)
        cursor.execute(sql)

        for row in cursor.fetchall():
            print row
            string += row[0] + ","

        return string[:-1]

    def __unicode__(self):
        print self.id

        if (self.id == None):
            return self.code
        else:
            return self._getCourseName() + " " + self.code

    def __getattribute__(self, name):
        if (name == "title"):
            return self.__unicode__()

        return super(Tutorial, self).__getattribute__(name)


class Practical(Event):
    code = models.CharField(max_length=20)
    ta = models.ForeignKey(Instructor, null=True, blank=True)

    def _getCourseName(self):
        string = "";
        cursor = connection.cursor()
        sql = 'SELECT code from taid_course_pracs tacp INNER JOIN taid_course tac ON tacp.practical_id=' + str(self.id)
        cursor.execute(sql)

        for row in cursor.fetchall():
            string += row[0] + ","

        return string[:-1]

    def __unicode__(self):
        if (self.id == None):
            return self.code
        else:
            return self._getCourseName() + " " + self.code

    def __getattribute__(self, name):
        if (name == "title"):
            return self.__unicode__()

        return super(Practical, self).__getattribute__(name)


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

    def clean(self):
        if self.value > self.assignment.total:
            raise ValidationError("{0} is more than {1}".format(
                self.value,
                self.assignment.total,
                ))
        elif self.value < 0.0:
            raise ValidationError("{0} is less than 0.0".format(self.value))


class GradeFile(models.Model):
    name = models.CharField(max_length=254)
    definitions = models.ManyToManyField("GradeDefinition", blank=True)


class GradeDefinition(models.Model):
    name = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=6, decimal_places=3)
    assignment = models.ForeignKey("Assignment")
    parent = models.ForeignKey("self", null=True, blank=True, related_name="subdefinitions")
