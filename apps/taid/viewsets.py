from django.shortcuts import render
from apps.taid import models, serializers

from rest_framework import viewsets


class InstructorViewSet(viewsets.ModelViewSet):
    queryset = models.Instructor.objects.all().order_by('university_id')
    serializer_class = serializers.InstructorSerializer


class TeachingAssistantViewSet(viewsets.ModelViewSet):
    queryset = models.TeachingAssistant.objects.all().order_by('university_id')
    serializer_class = serializers.TeachingAssistantSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = models.Student.objects.all().order_by('university_id')
    serializer_class = serializers.StudentSerializer


class IdentificationViewSet(viewsets.ModelViewSet):
    queryset = models.Identification.objects.all()
    serializer_class = serializers.IdentificationSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = models.Course.objects.all().order_by('code')
    serializer_class = serializers.CourseSerializer


class TutorialViewSet(viewsets.ModelViewSet):
    queryset = models.Tutorial.objects.all().order_by('code')
    serializer_class = serializers.TutorialSerializer


class PracticalViewSet(viewsets.ModelViewSet):
    queryset = models.Practical.objects.all().order_by('code')
    serializer_class = serializers.PracticalSerializer
