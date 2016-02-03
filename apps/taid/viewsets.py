from django.shortcuts import render
from apps.taid import models, serializers

from rest_framework import viewsets, routers, parsers


class InstructorViewSet(viewsets.ModelViewSet):
    queryset = models.Instructor.objects.all().order_by('university_id')
    serializer_class = serializers.InstructorSerializer


class TeachingAssistantViewSet(viewsets.ModelViewSet):
    queryset = models.TeachingAssistant.objects.all().order_by('university_id')
    serializer_class = serializers.TeachingAssistantSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = models.Student.objects.all().order_by('university_id')
    serializer_class = serializers.StudentSerializer


class StudentListFileViewSet(viewsets.ModelViewSet):
    queryset = models.StudentListFile.objects.all()
    serializer_class = serializers.StudentListFileSerializer
    parser_classes = (parsers.MultiPartParser, parsers.FormParser,)

    def perform_create(self, serializer):
        serializer.save(datafile=self.request.data.get('datafile'))


class IdentificationViewSet(viewsets.ModelViewSet):
    queryset = models.Identification.objects.all()
    serializer_class = serializers.IdentificationSerializer


class TutorialViewSet(viewsets.ModelViewSet):
    queryset = models.Tutorial.objects.all().order_by('code')
    serializer_class = serializers.TutorialSerializer


class PracticalViewSet(viewsets.ModelViewSet):
    queryset = models.Practical.objects.all().order_by('code')
    serializer_class = serializers.PracticalSerializer


router = routers.DefaultRouter()
router.register(r'instructors', InstructorViewSet)
router.register(r'teaching_assistants', TeachingAssistantViewSet)
router.register(r'students/upload', StudentListFileViewSet)
router.register(r'students', StudentViewSet)
router.register(r'identifications', IdentificationViewSet)
router.register(r'tutorials', TutorialViewSet)
router.register(r'practicals', PracticalViewSet)
