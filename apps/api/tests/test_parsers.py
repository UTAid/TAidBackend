from django.test import TestCase
from django.apps import apps
from django.core.files.base import ContentFile
from apps.api import parsers


class StudentListParserTests(TestCase):

    def test_student_parser_empty(self):
        test_file = ContentFile("")
        student_list_obj = parsers.StudentList(test_file)
        student_list_obj.parse()

        _student_model = apps.get_model("api", "Student")
        self.assertEqual(_student_model.objects.count(), 0)

    def test_student_parser_one(self):
        content = "canvi241,Cano,Vi,209415323,Vi.Cano@nowhere.com,ci1nva24,vi2c1na4,24vic1an"
        test_file = ContentFile(content.encode())
        student_list_obj = parsers.StudentList(test_file)
        student_list_obj.parse()

        _student_model = apps.get_model("api", "Student")
        entry = _student_model.objects.get(pk="canvi241")
        ids = entry.identification_set.all()
        self.assertEqual(entry.last_name, "Cano")
        self.assertEqual(entry.first_name, "Vi")
        self.assertEqual(entry.student_number, "209415323")
        self.assertEqual(entry.email, "Vi.Cano@nowhere.com")
        self.assertTrue(ids.get(value="ci1nva24"))
        self.assertTrue(ids.get(value="vi2c1na4"))
        self.assertTrue(ids.get(value="24vic1an"))

    def test_student_parser_many(self):
        content = "couade63,Couchman,Adella,2081414346," + \
            "Adella.Couchman@nowhere.com,ued3oca6,d63ecuao,3uac6doe\r\n" + \
            "staild32,Staplins,Ilda,2021649638,Ilda.Staplins@nowhere.com," + \
            "a2tdlsi3,d2tsi3la,2iads3lt\r\n" + "bisbea71,Bison,Beatris," + \
            "203143295,Beatris.Bison@nowhere.com,7sabibe1,eibs17ab,ie1asbb7"
        test_file = ContentFile(content.encode())
        student_list_obj = parsers.StudentList(test_file)
        student_list_obj.parse()

        _student_model = apps.get_model("api", "Student")
        for row in content.split('\r\n'):
            student_data = row.split(',')
            entry = _student_model.objects.get(pk=student_data[0])
            ids = entry.identification_set.all()
            self.assertEqual(entry.last_name, student_data[1])
            self.assertEqual(entry.first_name, student_data[2])
            self.assertEqual(entry.student_number, student_data[3])
            self.assertEqual(entry.email, student_data[4])
            self.assertTrue(ids.get(value=student_data[5]))
            self.assertTrue(ids.get(value=student_data[6]))
            self.assertTrue(ids.get(value=student_data[7]))

    def test_student_parser_conflict(self):
        content = "canvi241,Cano,Vi,209415323,Vi.Cano@nowhere.com,ci1nva24,vi2c1na4,24vic1an"
        test_file = ContentFile(content.encode())
        student_list_obj = parsers.StudentList(test_file)
        student_list_obj.parse()
        student_list_obj.parse()

        _student_model = apps.get_model("api", "Student")

        self.assertEqual(_student_model.objects.count(), 1)

    def test_student_parser_bad_format(self):
        content = "canvi241"
        test_file = ContentFile(content.encode())
        student_list_obj = parsers.StudentList(test_file)
        student_list_obj.parse()

        _student_model = apps.get_model("api", "Student")

        self.assertEqual(_student_model.objects.count(), 0)


class EnrollmentListParserTest(TestCase):

    def test_enrollment_parser_empty(self):
        test_file = ContentFile("")
        enrollment_list_obj = parsers.StudentList(test_file)
        enrollment_list_obj.parse()

        _student_model = apps.get_model("api", "Student")
        _lecture_model = apps.get_model("api", "Lecture")
        _tutorial_model = apps.get_model("api", "Tutorial")
        _practical_model = apps.get_model("api", "Practical")

        self.assertEqual(_student_model.objects.count(), 0)
        self.assertEqual(_lecture_model.objects.count(), 0)
        self.assertEqual(_tutorial_model.objects.count(), 0)
        self.assertEqual(_practical_model.objects.count(), 0)
