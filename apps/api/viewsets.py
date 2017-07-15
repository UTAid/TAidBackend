'''Performs get and post requests'''

from apps.api import models, serializers

from rest_framework import viewsets, routers, parsers
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework_csv.renderers import CSVRenderer
from django.core.exceptions import ObjectDoesNotExist


class NoHeaderCSVRenderer(CSVRenderer):
    # This is a slight hack because django-rest-framework-csv doesn't have the
    # option to create CSVs without headers
    def tablize(self, data, header=None, labels=None):
        data = super(NoHeaderCSVRenderer, self).tablize(data, header, labels)
        if len(data) > 0:
            data = data[1:]
        return data


class InstructorViewSet(viewsets.ModelViewSet):
    queryset = models.Instructor.objects.all().order_by('university_id')
    serializer_class = serializers.InstructorSerializer


class TeachingAssistantViewSet(viewsets.ModelViewSet):
    queryset = models.TeachingAssistant.objects.all().order_by('university_id')
    serializer_class = serializers.TeachingAssistantSerializer

    @list_route(methods=["post"])
    def upload(self, request):
        s = serializers.TAListSerializer(data=request.data)
        if not s.is_valid():
            return Response(s.errors)
        ta_list = s.save()
        return Response(ta_list.parse())

    @list_route(methods=["get"], renderer_classes=(NoHeaderCSVRenderer,))
    def export(self, request):
        content = []
        for university_id in request.GET.getlist("id"):
            ta = models.TeachingAssistant.objects.get(
                university_id=university_id)
            row = [
                ta.university_id,
                ta.first_name,
                ta.last_name,
                ta.email,
            ]
            content.append(row)
        return Response(content)


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

    @list_route(methods=["get"], renderer_classes=(NoHeaderCSVRenderer,))
    def export(self, request):
        content = []
        for university_id in request.GET.getlist("id"):
            student = models.Student.objects.get(university_id=university_id)
            row = [
                student.university_id,
                student.first_name,
                student.last_name,
                student.email,
                student.student_number,
            ]
            for identification in student.identification_set.all():
                row.append(identification.value)
            content.append(row)
        return Response(content)

    @list_route(methods=["post"])
    def enroll(self, request):
        s = serializers.EnrollmentListSerializer(data=request.data)
        if not s.is_valid():
            return Response(s.errors)
        enrollment_list = s.save()
        return Response(enrollment_list.parse())

    @list_route(methods=["get"], renderer_classes=(NoHeaderCSVRenderer,))
    def enrolled(self, request):
        content = []
        for university_id in request.GET.getlist("id"):
            student = models.Student.objects.get(university_id=university_id)
            lec = student.lecture_set.first()
            tut = student.tutorial_set.first()
            pra = student.practical_set.first()
            row = [
                student.university_id,
                "" if lec is None else lec.code,
                "" if tut is None else tut.code,
                "" if pra is None else pra.code,
            ]
            content.append(row)
        print(content)
        return Response(content)


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


class MarkViewSet(viewsets.ModelViewSet):
    queryset = models.Mark.objects.all().order_by("student")
    serializer_class = serializers.MarkSerializer


class RubricViewSet(viewsets.ModelViewSet):
    queryset = models.Rubric.objects.all().order_by("name")
    serializer_class = serializers.RubricSerializer


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = models.Assignment.objects.all().order_by("name")
    serializer_class = serializers.AssignmentSerializer

    @list_route(methods=["post"])
    def upload(self, request):
        s = serializers.MarkFileSerializer(data=request.data)
        if not s.is_valid():
            return Response(s.errors)
        mark_file = s.save()
        return Response(mark_file.parse())

    @detail_route(methods=["get"], renderer_classes=(NoHeaderCSVRenderer,))
    def export(self, request, pk):
        assignment = models.Assignment.objects.prefetch_related(
            "rubric_entries").get(id=pk)
        rubrics = assignment.rubric_entries.all()
        num_entries = rubrics.count() + 1
        content = [[""] * num_entries, [""] * num_entries]
        content[0][0] = assignment.name
        for index, rubric in enumerate(rubrics, start=1):
            content[0][index] = rubric.name
            content[1][index] = rubric.total

        # This is valid since each TAid instance is a single class.
        for student in models.Student.objects.prefetch_related("mark_set", "mark_set__rubric"):
            row = [""] * num_entries
            row[0] = student.university_id
            for index, rubric in enumerate(rubrics, start=1):
                try:
                    mark = student.mark_set.get(rubric=rubric)
                    row[index] = mark.value
                except ObjectDoesNotExist:
                    continue
            content.append(row)
        return Response(content)


router = routers.DefaultRouter()
router.register(r'instructors', InstructorViewSet)
router.register(r'teaching_assistants', TeachingAssistantViewSet)
router.register(r'students', StudentViewSet)
router.register(r'identifications', IdentificationViewSet)
router.register(r'lectures', LectureViewSet)
router.register(r'tutorials', TutorialViewSet)
router.register(r'practicals', PracticalViewSet)
router.register(r'assignments', AssignmentViewSet)
router.register(r'rubrics', RubricViewSet)
router.register(r'marks', MarkViewSet)
