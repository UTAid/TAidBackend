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

    def test_student_parser_conflict(self):
        f1 = ContentFile("canvi241,Cano,Vi,209415323,Vi.Cano@nowhere.com,ci1nva24,vi2c1na4,24vic1an")
        parsers.student_parser(f1)
        parsers.student_parser(f1)

        self.assertEqual(stuModel.objects.count(), 1)

    def test_student_parser_bad_format(self):
        f1 = ContentFile("canvi241")
        parsers.student_parser(f1)

        self.assertEqual(stuModel.objects.count(), 0)


class EnrollmentListParserTest(TestCase):
    
    def test_enrollment_parser_empty(self):
        f1 = ContentFile("")
        parsers.enrollment_parser(f1)

        _student_model = apps.get_model("taid", "Student")
        _lecture_model = apps.get_model("taid", "Lecture")
        _tutorial_model = apps.get_model("taid", "Tutorial")
        _practical_model = apps.get_model("taid", "Practical")

        self.assertEqual(_student_model.objects.count(), 0)
        self.assertEqual(_lecture_model.objects.count(), 0)
        self.assertEqual(_tutorial_model.objects.count(), 0)
        self.assertEqual(_practical_model.objects.count(), 0)


    def test_enrollment_parser_no_practical(self):
        f1 = ContentFile("canvi241,L0003,T0002,")
        parsers.enrollment_parser(f1)

        _student_model = apps.get_model("taid", "Student")
        _lecture_model = apps.get_model("taid", "Lecture")
        _tutorial_model = apps.get_model("taid", "Tutorial")
        _practical_model = apps.get_model("taid", "Practical")

        self.assertEqual(_student_model.university_id, "canvi241")
        self.assertEqual(_lecture_model.code, "L0003")
        self.assertEqual(_tutorial_model.code, "T0002")
        self.assertEqual(_practical_model.objects.count(), 0)


    def test_enrollment_parser_with_practical(self):
        f1 = ContentFile("canvi241,L0003,T0002,PRA0001")
        parsers.enrollment_parser(f1)

        _student_model = apps.get_model("taid", "Student")
        _lecture_model = apps.get_model("taid", "Lecture")
        _tutorial_model = apps.get_model("taid", "Tutorial")
        _practical_model = apps.get_model("taid", "Practical")

        self.assertEqual(_student_model.university_id, "canvi241")
        self.assertEqual(_lecture_model.code, "L0003")
        self.assertEqual(_tutorial_model.code, "T0002")
        self.assertEqual(_practical_model.code, "PRA0001")


    def test_enrollment_parser_multi_no_practical(self):
        f1Content = ContentFile("canvi241,L0001,T0001,\r\n" +\
                                "racrob58,L0002,T0002,\r\n" +\
                                "couade63,L0003,T0003,\r\n" +\
                                "staild32,L0004,T0004,\r\n" +\
                                "bisbea71,L0005,T0005,\r\n" +\
                                "petbil69,L0006,T0006,")

        parsers.enrollment_parser(f1)
        _student_model = apps.get_model("taid", "Student")
        _lecture_model = apps.get_model("taid", "Lecture")
        _tutorial_model = apps.get_model("taid", "Tutorial")
        _practical_model = apps.get_model("taid", "Practical")

        for row in f1Content.split('\r\n'):
            enrollment_string = row.split(",")
            stu_entry =  _student_model.objects.get(enrollment_string[0])
            lec_entry =  _lecture_model.objects.get(enrollment_string[1])
            tut_entry =  _tutorial_model.objects.get(enrollment_string[2])

            self.assertTrue(stu_entry.objects.count() != 0)
            self.assertTrue(lec_entry.objects.count() != 0)
            self.assertTrue(tut_entry.objects.count() != 0)

            self.assertEqual(stu_entry.university_id, enrollment_string[0])
            self.assertEqual(lec_entry.code, enrollment_string[1])
            self.assertEqual(tut_entry.code, enrollment_string[2])
            self.assertEqual(_practical_model.objects.count(), 0)


    def test_enrollment_parser_multi_with_practical(self):
        f1Content = ContentFile("canvi241,L0001,T0001,PRA0001\r\n" +\
                                "racrob58,L0002,T0002,PRA0002\r\n" +\
                                "couade63,L0003,T0003,PRA0003\r\n" +\
                                "staild32,L0004,T0004,PRA0004\r\n" +\
                                "bisbea71,L0005,T0005,PRA0005\r\n" +\
                                "petbil69,L0006,T0006,PRA0006")

        parsers.enrollment_parser(f1)
        _student_model = apps.get_model("taid", "Student")
        _lecture_model = apps.get_model("taid", "Lecture")
        _tutorial_model = apps.get_model("taid", "Tutorial")
        _practical_model = apps.get_model("taid", "Practical")

        for row in f1Content.split('\r\n'):
            enrollment_string = row.split(",")
            stu_entry =  _student_model.objects.get(enrollment_string[0])
            lec_entry =  _lecture_model.objects.get(enrollment_string[1])
            tut_entry =  _tutorial_model.objects.get(enrollment_string[2])
            pra_entry =  _practical_model.objects.get(enrollment_string[3])

            self.assertTrue(stu_entry.objects.count() != 0)
            self.assertTrue(lec_entry.objects.count() != 0)
            self.assertTrue(tut_entry.objects.count() != 0)
            self.assertTrue(pra_entry.objects.count() != 0)

            self.assertEqual(stu_entry.university_id, enrollment_string[0])
            self.assertEqual(lec_entry.code, enrollment_string[1])
            self.assertEqual(tut_entry.code, enrollment_string[2])
            self.assertEqual(pra_entry.code, enrollment_string[3])

    def test_enrollment_parser_multi_no_practical_and_with_practical(self):
        f1Content = ContentFile("canvi241,L0001,T0001,\r\n" +\
                                "racrob58,L0002,T0002,PRA0002\r\n" +\
                                "couade63,L0003,T0003,\r\n" +\
                                "staild32,L0004,T0004,PRA0004\r\n" +\
                                "bisbea71,L0005,T0005,\r\n" +\
                                "petbil69,L0006,T0006,PRA0006")

        parsers.enrollment_parser(f1)
        _student_model = apps.get_model("taid", "Student")
        _lecture_model = apps.get_model("taid", "Lecture")
        _tutorial_model = apps.get_model("taid", "Tutorial")
        _practical_model = apps.get_model("taid", "Practical")

        for row in f1Content.split('\r\n'):
            enrollment_string = row.split(",")
            stu_entry =  _student_model.objects.get(enrollment_string[0])
            lec_entry =  _lecture_model.objects.get(enrollment_string[1])
            tut_entry =  _tutorial_model.objects.get(enrollment_string[2])

            if (enrollment_string[3] != ""):
                pra_entry =  _practical_model.objects.get(enrollment_string[3])
                self.assertEqual(pra_entry.code, enrollment_string[3])

            self.assertEqual(stu_entry.university_id, enrollment_string[0])
            self.assertEqual(lec_entry.code, enrollment_string[1])
            self.assertEqual(tut_entry.code, enrollment_string[2])


class MarkParserTest(TestCase):

    def test_mark_parser_empty(self):
        f1 = ContentFile("")
        assignment_model = apps.get_model("taid", "Assignment")
        student_model = apps.get_model("taid", "Student")
        mark_model = apps.get_model("taid", "Mark")
        rubric_model = apps.get_model("taid", "Rubric")

        self.assertEqual(assignment_model.objects.count(), 0)
        self.assertEqual(student_model.objects.count(), 0)
        self.assertEqual(mark_model.objects.count(), 0)
        self.assertEqual(rubric_model.objects.count(), 0)
            




