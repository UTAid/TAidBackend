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


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    instructors = InstructorSerializer
    students = StudentSerializer

    class Meta:
        model = models.Course
        fields = (
                'url',
                'id',
                'code',
                'title',
                'section_code',
                'lecture_session',
                'instructors',
                'students',
                )


class TutorialSerializer(serializers.HyperlinkedModelSerializer):
    course = CourseSerializer
    ta = TeachingAssistantSerializer

    class Meta:
        model = models.Tutorial
        fields = ('url', 'id', 'code', 'course', 'ta')


class PracticalSerializer(serializers.HyperlinkedModelSerializer):
    course = CourseSerializer
    ta = TeachingAssistantSerializer

    class Meta:
        model = models.Practical
        fields = ('url', 'id', 'code', 'course', 'ta')
