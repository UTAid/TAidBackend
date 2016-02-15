from django.test import TestCase
from django.apps import apps
from django.core.files.base import ContentFile
from apps.taid import parsers


class StudentListParserTests(TestCase):

    def test_student_parser_empty(self):
        f1 = ContentFile("")
        parsers.student_parser(f1)

        stuModel = apps.get_model("taid", "Student")
        self.assertEqual(stuModel.objects.count(), 0)

    def test_student_parser_one(self):
        f1 = ContentFile("canvi241,Cano,Vi,209415323,Vi.Cano@nowhere.com,ci1nva24,vi2c1na4,24vic1an")
        parsers.student_parser(f1)

        stuModel = apps.get_model("taid", "Student")
        entry = stuModel.objects.get(pk="canvi241")
        ids = entry.identification_set.all()
        self.assertEqual(entry.last_name, "Cano")
        self.assertEqual(entry.first_name, "Vi")
        self.assertEqual(entry.student_number, "209415323")
        self.assertEqual(entry.email, "Vi.Cano@nowhere.com")
        self.assertTrue(ids.get(value="ci1nva24"))
        self.assertTrue(ids.get(value="vi2c1na4"))
        self.assertTrue(ids.get(value="24vic1an"))

    def test_student_parser_many(self):
        f1Content = "couade63,Couchman,Adella,2081414346,Adella.Couchman@nowhere.com,ued3oca6,d63ecuao,3uac6doe\r\n" +\
            "staild32,Staplins,Ilda,2021649638,Ilda.Staplins@nowhere.com,a2tdlsi3,d2tsi3la,2iads3lt\r\n" +\
            "bisbea71,Bison,Beatris,203143295,Beatris.Bison@nowhere.com,7sabibe1,eibs17ab,ie1asbb7"
        parsers.student_parser(ContentFile(f1Content))

        stuModel = apps.get_model("taid", "Student")
        for row in f1Content.split('\r\n'):
            stuStr = row.split(',')
            entry = stuModel.objects.get(pk=stuStr[0])
            ids = entry.identification_set.all()
            self.assertEqual(entry.last_name, stuStr[1])
            self.assertEqual(entry.first_name, stuStr[2])
            self.assertEqual(entry.student_number, stuStr[3])
            self.assertEqual(entry.email, stuStr[4])
            self.assertTrue(ids.get(value=stuStr[5]))
            self.assertTrue(ids.get(value=stuStr[6]))
            self.assertTrue(ids.get(value=stuStr[7]))

    def test_student_parser_multi_id(self):
        pass

    def test_student_parser_conflict(self):
        pass

    def test_student_parser_bad_format(self):
        pass


class EnrollmentListParserTest(TestCase):
    pass
