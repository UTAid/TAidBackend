from apps.api import models
from rest_framework import serializers

class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Instructor
        fields = ('url', 'university_id', 'first_name', 'last_name', 'email')


class TeachingAssistantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TeachingAssistant
        fields = ('url', 'university_id', 'first_name', 'last_name', 'email')


class IdentificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Identification
        fields = ('url', 'id', 'student', 'description', 'value')


class StudentSerializer(serializers.ModelSerializer):
    ids = IdentificationSerializer(source="identification_set", many=True, required=False)

    class Meta:
        model = models.Student
        fields = (
                'url',
                'university_id',
                'student_number',
                'first_name',
                'last_name',
                'email',
                'ids',
                )


class LectureSerializer(serializers.ModelSerializer):
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


class TutorialSerializer(serializers.ModelSerializer):
    ta = TeachingAssistantSerializer
    students = StudentSerializer

    class Meta:
        model = models.Tutorial
        fields = ('url', 'id', 'code', 'ta', 'students')


class PracticalSerializer(serializers.ModelSerializer):
    ta = TeachingAssistantSerializer
    students = StudentSerializer

    class Meta:
        model = models.Practical
        fields = ('url', 'id', 'code', 'ta', 'students')


class StudentListFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudentListFile
        fields = ('url', 'id', 'created', 'datafile')
