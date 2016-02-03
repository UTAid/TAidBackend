from apps.taid import models
from rest_framework import serializers

class InstructorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Instructor
        fields = ('url', 'university_id', 'first_name', 'last_name', 'email')


class TeachingAssistantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.TeachingAssistant
        fields = ('url', 'university_id', 'first_name', 'last_name', 'email')


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    ids = 'IdentificationSerializer'

    class Meta:
        model = models.Student
        fields = (
                'url',
                'university_id',
                'student_number',
                'first_name',
                'last_name',
                'email',
                )


class IdentificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Identification
        fields = ('url', 'id', 'student', 'description', 'value')


class LectureSerializer(serializers.HyperlinkedModelSerializer):
    instructors = InstructorSerializer
    students = StudentSerializer

    class Meta:
        model = models.Lecture
        fields = (
                'url',
                'id',
                'code',
                'instructors',
                'students',
                )


class TutorialSerializer(serializers.HyperlinkedModelSerializer):
    ta = TeachingAssistantSerializer

    class Meta:
        model = models.Tutorial
        fields = ('url', 'id', 'code', 'ta', 'students')


class PracticalSerializer(serializers.HyperlinkedModelSerializer):
    ta = TeachingAssistantSerializer

    class Meta:
        model = models.Practical
        fields = ('url', 'id', 'code', 'ta', 'students')


class StudentListFileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.StudentListFile
        fields = ('url', 'id', 'created', 'datafile')
