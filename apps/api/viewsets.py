from apps.api import models, serializers

from rest_framework import viewsets, routers, parsers
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework_csv.renderers import CSVRenderer


class InstructorViewSet(viewsets.ModelViewSet):
    queryset = models.Instructor.objects.all().order_by('university_id')
    serializer_class = serializers.InstructorSerializer


class TeachingAssistantViewSet(viewsets.ModelViewSet):
    queryset = models.TeachingAssistant.objects.all().order_by('university_id')
    serializer_class = serializers.TeachingAssistantSerializer


class StudentListCSVRenderer(CSVRenderer):
    header = None


class StudentViewSet(viewsets.ModelViewSet):
    queryset = models.Student.objects.all().order_by('university_id')
    serializer_class = serializers.StudentSerializer

    @list_route(methods=["post"])
    def upload(self, request):
        s = serializers.StudentListSerializer(data=request.data)
        if not s.is_valid():
            return Response(s.errors)
        student_list = s.save()
        return Response(student_list.parse())

    @list_route(methods=["get"], renderer_classes=(StudentListCSVRenderer,))
    def export(self, request):
        student = models.Student.objects.get(university_id="kuadav")
        content = [
                [student.university_id,
                student.first_name,
                student.last_name,
                student.email,
                student.student_number]
        ]
        return Response(content)

    @list_route(methods=["post"])
    def enroll(self, request):
        s = serializers.EnrollmentListSerializer(data=request.data)
        if not s.is_valid():
            return Response(s.errors)
        enrollment_list = s.save()
        return Response(enrollment_list.parse())


class IdentificationViewSet(viewsets.ModelViewSet):
    queryset = models.Identification.objects.all()
    serializer_class = serializers.IdentificationSerializer


class LectureViewSet(viewsets.ModelViewSet):
    queryset = models.Lecture.objects.all().order_by('code')
    serializer_class = serializers.LectureSerializer


class TutorialViewSet(viewsets.ModelViewSet):
    queryset = models.Tutorial.objects.all().order_by('code')
    serializer_class = serializers.TutorialSerializer


class PracticalViewSet(viewsets.ModelViewSet):
    queryset = models.Practical.objects.all().order_by('code')
    serializer_class = serializers.PracticalSerializer


class MarkFileViewSet(viewsets.ModelViewSet):
    queryset = models.Mark.objects.all().order_by('student')
    serializer_class = serializers.MarkSerializer

    @list_route(methods=["post"])
    def upload(self, request):
        s = serializers.MarkFileSerializer(data=request.data)
        if not s.is_valid():
            return Response(s.errors)
        mark_file = s.save()
        return Response(mark_file.parse())


router = routers.DefaultRouter()
router.register(r'instructors', InstructorViewSet)
router.register(r'teaching_assistants', TeachingAssistantViewSet)
router.register(r'students', StudentViewSet)
router.register(r'identifications', IdentificationViewSet)
router.register(r'lectures', LectureViewSet)
router.register(r'tutorials', TutorialViewSet)
router.register(r'practicals', PracticalViewSet)
router.register(r'marks', MarkFileViewSet)
