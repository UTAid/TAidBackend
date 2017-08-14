'''Converts models to JSON'''

from apps.api import models, parsers
from apps.api.validators import validate_csv
from rest_framework import serializers


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Instructor
        fields = ("url", "university_id", "first_name", "last_name", "email")


class TeachingAssistantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TeachingAssistant
        fields = ("url", "university_id", "first_name", "last_name", "email")


class IdentificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Identification
        fields = ("url", "id", "student", "description", "value")


class StudentSerializer(serializers.ModelSerializer):
    ids = IdentificationSerializer(
        source="identification_set", many=True, required=False, read_only=True)

    class Meta:
        model = models.Student
        fields = (
            "url",
            "university_id",
            "student_number",
            "first_name",
            "last_name",
            "email",
            "ids",
        )


class LectureSerializer(serializers.ModelSerializer):
    instructors = InstructorSerializer
    students = StudentSerializer

    class Meta:
        model = models.Lecture
        fields = (
            "url",
            "id",
            "code",
            "instructors",
            "students",
        )


class TutorialSerializer(serializers.ModelSerializer):
    teaching_assistant = TeachingAssistantSerializer
    students = StudentSerializer

    class Meta:
        model = models.Tutorial
        fields = ("url", "id", "code", "teaching_assistant", "students")


class PracticalSerializer(serializers.ModelSerializer):
    teaching_assistant = TeachingAssistantSerializer
    students = StudentSerializer

    class Meta:
        model = models.Practical
        fields = ("url", "id", "code", "teaching_assistant", "students")


class MarkSerializer(serializers.ModelSerializer):
    value = serializers.DecimalField
    student = StudentSerializer

    class Meta:
        model = models.Mark
        fields = ("url", "id", "value", "student")


class RubricSerializer(serializers.ModelSerializer):
    marks = MarkSerializer(source="mark_set", many=True, required=False, read_only=True)

    class Meta:
        model = models.Rubric
        fields = ("url", "name", "total", "marks")


class AssignmentSerializer(serializers.ModelSerializer):
    rubric_entries = RubricSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = models.Assignment
        fields = ("url", "name", "rubric_entries")


class StudentListSerializer(serializers.Serializer):
    file = serializers.FileField(validators=(validate_csv,))

    def update(self, instance, validated_data):
        instance.file = validated_data.get("file", instance.file)
        return instance

    def create(self, validated_data):
        return parsers.StudentList(**validated_data)


class EnrollmentListSerializer(serializers.Serializer):
    file = serializers.FileField(validators=(validate_csv,))

    def update(self, instance, validated_data):
        instance.file = validated_data.get("file", instance.file)
        return instance

    def create(self, validated_data):
        return parsers.EnrollmentList(**validated_data)


class MarkFileSerializer(serializers.Serializer):
    file = serializers.FileField(validators=(validate_csv,))

    def update(self, instance, validated_data):
        instance.file = validated_data.get("file", instance.file)
        return instance

    def create(self, validated_data):
        return parsers.MarkFile(**validated_data)


class TAListSerializer(serializers.Serializer):
    file = serializers.FileField(validators=(validate_csv,))

    def update(self, instance, validated_data):
        instance.file = validated_data.get("file", instance.file)
        return instance

    def create(self, validated_data):
        return parsers.TAList(**validated_data)
