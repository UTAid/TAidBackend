from django.test import TestCase
from django.core.files.base import ContentFile
from apps.api import parsers
from apps.api.models import Student, Lecture, Tutorial, Practical, TeachingAssistant, Assignment, Rubric, Mark


class StudentListParserTests(TestCase):

    def test_student_parser_empty(self):
        '''Nothing to parse'''
        content = ""
        test_file = ContentFile(content.encode())
        student_list_obj = parsers.StudentList(test_file)
        student_list_obj.parse()

        self.assertEqual(Student.objects.count(), 0)

    def test_student_parser_one(self):
        '''One student to parse'''
        content = "canvi241,Cano,Vi,209415323,Vi.Cano@nowhere.com,ci1nva24,vi2c1na4,24vic1an"
        test_file = ContentFile(content.encode())
        student_list_obj = parsers.StudentList(test_file)
        student_list_obj.parse()

        entry = Student.objects.get(pk="canvi241")
        ids = entry.identification_set.all()
        self.assertEqual(entry.last_name, "Cano")
        self.assertEqual(entry.first_name, "Vi")
        self.assertEqual(entry.student_number, "209415323")
        self.assertEqual(entry.email, "Vi.Cano@nowhere.com")
        self.assertTrue(ids.get(value="ci1nva24"))
        self.assertTrue(ids.get(value="vi2c1na4"))
        self.assertTrue(ids.get(value="24vic1an"))

    def test_student_parser_many(self):
        '''multiple students to parse'''
        content = "couade63,Couchman,Adella,2081414346," + \
            "Adella.Couchman@nowhere.com,ued3oca6,d63ecuao,3uac6doe\r\n" + \
            "staild32,Staplins,Ilda,2021649638,Ilda.Staplins@nowhere.com," + \
            "a2tdlsi3,d2tsi3la,2iads3lt\r\n" + "bisbea71,Bison,Beatris," + \
            "203143295,Beatris.Bison@nowhere.com,7sabibe1,eibs17ab,ie1asbb7"
        test_file = ContentFile(content.encode())
        student_list_obj = parsers.StudentList(test_file)
        student_list_obj.parse()

        for row in content.split('\r\n'):
            student_data = row.split(',')
            entry = Student.objects.get(pk=student_data[0])
            ids = entry.identification_set.all()
            self.assertEqual(entry.last_name, student_data[1])
            self.assertEqual(entry.first_name, student_data[2])
            self.assertEqual(entry.student_number, student_data[3])
            self.assertEqual(entry.email, student_data[4])
            self.assertTrue(ids.get(value=student_data[5]))
            self.assertTrue(ids.get(value=student_data[6]))
            self.assertTrue(ids.get(value=student_data[7]))
        self.assertEqual(Student.objects.count(), 3)

    def test_student_parser_conflict(self):
        '''Same student with same info is sent to be parsed twice. There
        should be only one student at the end
        '''
        content = "canvi241,Cano,Vi,209415323,Vi.Cano@nowhere.com,ci1nva24,vi2c1na4,24vic1an"
        test_file = ContentFile(content.encode())
        student_list_obj = parsers.StudentList(test_file)
        student_list_obj.parse()
        student_list_obj.parse()

        self.assertEqual(Student.objects.count(), 1)

    def test_student_changed_info(self):
        '''Student information is changed when requested'''
        content = "canvi241,Cano,Vi,209415323,Vi.Cano@nowhere.com,ci1nva24\r\n" + \
            "canvi241,Canol,Vi,209415323,Vi.Cano@nowhere.com,ci1nva23,ci1nva25"
        test_file = ContentFile(content.encode())
        student_list_obj = parsers.StudentList(test_file)
        student_list_obj.parse()

        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(Student.objects.get(pk="canvi241").last_name, "Canol")
        self.assertEqual(Student.objects.get(
            pk="canvi241").identification_set.count(), 2)
        self.assertEqual(Student.objects.get(
            pk="canvi241").identification_set.all()[0].value, 'ci1nva23')
        self.assertEqual(Student.objects.get(
            pk="canvi241").identification_set.all()[1].value, 'ci1nva25')

    def test_student_parser_bad_format(self):
        '''Does not enter student when bad formatting is entered'''
        content = "canvi241"
        test_file = ContentFile(content.encode())
        student_list_obj = parsers.StudentList(test_file)
        student_list_obj.parse()

        self.assertEqual(Student.objects.count(), 0)


class EnrollmentListParserTests(TestCase):

    def setUp(self):
        self.student1 = Student.objects.create(
            university_id="canvi241",
            first_name="Cano",
            last_name="Vi",
            email="Vi.Cano@nowhere.com",
            student_number="209415323",
        )
        self.student2 = Student.objects.create(
            university_id="racrob58",
            first_name="Racey",
            last_name="Robbin",
            email="Robbin.Racey@nowhere.com",
            student_number="206271143",
        )
        self.tutorial1 = Tutorial.objects.create(
            code="T0001",
        )
        self.tutorial2 = Tutorial.objects.create(
            code="T0002",
        )
        self.lecture1 = Lecture.objects.create(
            code="L0001",
        )
        self.lecture2 = Lecture.objects.create(
            code="L0002",
        )
        self.practical1 = Practical.objects.create(
            code="PRA0001",
        )
        self.practical2 = Practical.objects.create(
            code="PRA0002",
        )

    def tearDown(self):
        self.student1.delete()
        self.student2.delete()
        self.tutorial1.delete()
        self.tutorial2.delete()
        self.lecture1.delete()
        self.lecture2.delete()
        self.practical1.delete()
        self.practical2.delete()

    def test_enrollment_parser_empty(self):
        '''Student is not linked with any classes if it does not say so'''
        content = "canvi241"
        test_file = ContentFile(content.encode())
        enrollment_list_obj = parsers.EnrollmentList(test_file)
        enrollment_list_obj.parse()

        student = Student.objects.get(pk="canvi241")

        self.assertEqual(student.tutorial_set.count(), 0)
        self.assertEqual(student.lecture_set.count(), 0)
        self.assertEqual(student.practical_set.count(), 0)

    def test_enrollment_parser_no_practical(self):
        '''Student is linked with the appropriate classes'''
        content = "canvi241,L0001,T0002,"
        test_file = ContentFile(content.encode())
        enrollment_list_obj = parsers.EnrollmentList(test_file)
        enrollment_list_obj.parse()

        student = Student.objects.get(pk="canvi241")

        self.assertEqual(student.tutorial_set.count(), 1)
        self.assertEqual(student.lecture_set.count(), 1)
        self.assertEqual(student.practical_set.count(), 0)

    def test_enrollment_parser_with_practical(self):
        '''Student is linked with the appropriate classes'''
        content = "canvi241,L0001,T0002,PRA0001"
        test_file = ContentFile(content.encode())
        enrollment_list_obj = parsers.EnrollmentList(test_file)
        enrollment_list_obj.parse()

        student = Student.objects.get(pk="canvi241")

        self.assertEqual(student.tutorial_set.count(), 1)
        self.assertEqual(student.lecture_set.count(), 1)
        self.assertEqual(student.practical_set.count(), 1)

    def test_enrollment_parser_multi_no_practical(self):
        '''Student is linked with the appropriate classes'''
        content = "canvi241,L0001,T0001,\r\n" +\
            "racrob58,L0002,T0002,"
        test_file = ContentFile(content.encode())
        enrollment_list_obj = parsers.EnrollmentList(test_file)
        enrollment_list_obj.parse()

        for i, row in enumerate(content.split('\r\n')):
            enrollment_string = row.split(',')

            student = Student.objects.get(pk=enrollment_string[0])

            lecture = "L000" + str(i + 1)
            tutorial = "T000" + str(i + 1)

            self.assertEqual(student.lecture_set.get().code, lecture)
            self.assertEqual(student.tutorial_set.get().code, tutorial)
            self.assertEqual(student.lecture_set.count(), 1)
            self.assertEqual(student.tutorial_set.count(), 1)

    def test_add_student_multiple_practical(self):
        '''Student is linked with the appropriate classes'''
        content = "canvi241,L0001,T0001,PRA0001\r\n" +\
            "canvi241,L0001,T0001,PRA0002"
        test_file = ContentFile(content.encode())
        enrollment_list_obj = parsers.EnrollmentList(test_file)
        enrollment_list_obj.parse()

        student = Student.objects.get(pk="canvi241")

        for i, row in enumerate(content.split('\r\n')):
            enrollment_string = row.split(',')
            practical = "PRA000" + str(i + 1)

            self.assertEqual(student.practical_set.all()[i].code, practical)

        self.assertEqual(student.lecture_set.get().code, "L0001")
        self.assertEqual(student.tutorial_set.get().code, "T0001")
        self.assertEqual(student.lecture_set.count(), 1)
        self.assertEqual(student.tutorial_set.count(), 1)
        self.assertEqual(student.practical_set.count(), 2)

    def test_enrollment_parser_multi_with_practical(self):
        '''Student is linked with the appropriate classes'''
        content = "canvi241,L0001,T0001,PRA0001\r\n" +\
            "racrob58,L0002,T0002,PRA0002"
        test_file = ContentFile(content.encode())
        enrollment_list_obj = parsers.EnrollmentList(test_file)
        enrollment_list_obj.parse()

        for i, row in enumerate(content.split('\r\n')):
            enrollment_string = row.split(',')

            student = Student.objects.get(pk=enrollment_string[0])

            lecture = "L000" + str(i + 1)
            tutorial = "T000" + str(i + 1)
            practical = "PRA000" + str(i + 1)

            self.assertEqual(student.lecture_set.get().code, lecture)
            self.assertEqual(student.tutorial_set.get().code, tutorial)
            self.assertEqual(student.practical_set.get().code, practical)
            self.assertEqual(student.lecture_set.count(), 1)
            self.assertEqual(student.tutorial_set.count(), 1)
            self.assertEqual(student.practical_set.count(), 1)

    def test_enrollment_parser_multi_no_practical_and_with_practical(self):
        '''Student is linked with the appropriate classes'''
        content = "canvi241,L0001,T0001,\r\n" +\
            "racrob58,L0002,T0002,PRA0002"
        test_file = ContentFile(content.encode())
        enrollment_list_obj = parsers.EnrollmentList(test_file)
        enrollment_list_obj.parse()

        for i, row in enumerate(content.split('\r\n')):
            enrollment_string = row.split(',')

            student = Student.objects.get(pk=enrollment_string[0])

            lecture = "L000" + str(i + 1)
            tutorial = "T000" + str(i + 1)

            if enrollment_string[3] != "":
                practical = "PRA000" + str(i + 1)
                self.assertEqual(student.practical_set.get().code, practical)
                self.assertEqual(student.practical_set.count(), 1)
            else:
                self.assertEqual(student.practical_set.count(), 0)

            self.assertEqual(student.lecture_set.get().code, lecture)
            self.assertEqual(student.tutorial_set.get().code, tutorial)
            self.assertEqual(student.lecture_set.count(), 1)
            self.assertEqual(student.tutorial_set.count(), 1)

    def test_enrollment_parser_no_lecture(self):
        '''Student is linked with the appropriate classes'''
        content = "canvi241,,T0002,PRA0001"
        test_file = ContentFile(content.encode())
        enrollment_list_obj = parsers.EnrollmentList(test_file)
        enrollment_list_obj.parse()

        student = Student.objects.get(pk="canvi241")

        self.assertEqual(student.tutorial_set.count(), 1)
        self.assertEqual(student.lecture_set.count(), 0)
        self.assertEqual(student.practical_set.count(), 1)

    def test_enrollment_parser_with_lecture(self):
        '''Student is linked with the appropriate classes'''
        content = "canvi241,L0001,T0002,PRA0001"
        test_file = ContentFile(content.encode())
        enrollment_list_obj = parsers.EnrollmentList(test_file)
        enrollment_list_obj.parse()

        student = Student.objects.get(pk="canvi241")

        self.assertEqual(student.tutorial_set.count(), 1)
        self.assertEqual(student.lecture_set.count(), 1)
        self.assertEqual(student.practical_set.count(), 1)

    def test_enrollment_parser_multi_no_lecture(self):
        '''Student is linked with the appropriate classes'''
        content = "canvi241,,T0001,PRA0001\r\n" +\
            "racrob58,,T0002,PRA0002"
        test_file = ContentFile(content.encode())
        enrollment_list_obj = parsers.EnrollmentList(test_file)
        enrollment_list_obj.parse()

        for i, row in enumerate(content.split('\r\n')):
            enrollment_string = row.split(',')

            student = Student.objects.get(pk=enrollment_string[0])

            practical = "PRA000" + str(i + 1)
            tutorial = "T000" + str(i + 1)

            self.assertEqual(student.practical_set.get().code, practical)
            self.assertEqual(student.tutorial_set.get().code, tutorial)
            self.assertEqual(student.practical_set.count(), 1)
            self.assertEqual(student.tutorial_set.count(), 1)

    def test_add_student_multiple_lecture(self):
        '''Student is linked with the appropriate classes'''
        content = "canvi241,L0001,T0001,PRA0001\r\n" +\
            "canvi241,L0002,T0001,PRA0001"
        test_file = ContentFile(content.encode())
        enrollment_list_obj = parsers.EnrollmentList(test_file)
        enrollment_list_obj.parse()

        student = Student.objects.get(pk="canvi241")

        for i, row in enumerate(content.split('\r\n')):
            enrollment_string = row.split(',')
            lecture = "L000" + str(i + 1)

            self.assertEqual(student.lecture_set.all()[i].code, lecture)

        self.assertEqual(student.practical_set.get().code, "PRA0001")
        self.assertEqual(student.tutorial_set.get().code, "T0001")
        self.assertEqual(student.practical_set.count(), 1)
        self.assertEqual(student.tutorial_set.count(), 1)
        self.assertEqual(student.lecture_set.count(), 2)

    def test_enrollment_parser_multi_with_lecture(self):
        '''Student is linked with the appropriate classes'''
        content = "canvi241,L0001,T0001,PRA0001\r\n" +\
            "racrob58,L0002,T0002,PRA0002"
        test_file = ContentFile(content.encode())
        enrollment_list_obj = parsers.EnrollmentList(test_file)
        enrollment_list_obj.parse()

        for i, row in enumerate(content.split('\r\n')):
            enrollment_string = row.split(',')

            student = Student.objects.get(pk=enrollment_string[0])

            lecture = "L000" + str(i + 1)
            tutorial = "T000" + str(i + 1)
            practical = "PRA000" + str(i + 1)

            self.assertEqual(student.lecture_set.get().code, lecture)
            self.assertEqual(student.tutorial_set.get().code, tutorial)
            self.assertEqual(student.practical_set.get().code, practical)
            self.assertEqual(student.lecture_set.count(), 1)
            self.assertEqual(student.tutorial_set.count(), 1)
            self.assertEqual(student.practical_set.count(), 1)

    def test_enrollment_parser_multi_no_lecture_and_with_lecture(self):
        '''Student is linked with the appropriate classes'''
        content = "canvi241,,T0001,PRA0001\r\n" +\
            "racrob58,L0002,T0002,PRA0002"
        test_file = ContentFile(content.encode())
        enrollment_list_obj = parsers.EnrollmentList(test_file)
        enrollment_list_obj.parse()

        for i, row in enumerate(content.split('\r\n')):
            enrollment_string = row.split(',')

            student = Student.objects.get(pk=enrollment_string[0])

            practical = "PRA000" + str(i + 1)
            tutorial = "T000" + str(i + 1)

            if enrollment_string[1] != "":
                lecture = "L000" + str(i + 1)
                self.assertEqual(student.lecture_set.get().code, lecture)
                self.assertEqual(student.lecture_set.count(), 1)
            else:
                self.assertEqual(student.lecture_set.count(), 0)

            self.assertEqual(student.practical_set.get().code, practical)
            self.assertEqual(student.tutorial_set.get().code, tutorial)
            self.assertEqual(student.practical_set.count(), 1)
            self.assertEqual(student.tutorial_set.count(), 1)

    def test_enrollment_parser_no_tutorial(self):
        '''Student is linked with the appropriate classes'''
        content = "canvi241,L0001,,PRA0001"
        test_file = ContentFile(content.encode())
        enrollment_list_obj = parsers.EnrollmentList(test_file)
        enrollment_list_obj.parse()

        student = Student.objects.get(pk="canvi241")

        self.assertEqual(student.tutorial_set.count(), 0)
        self.assertEqual(student.lecture_set.count(), 1)
        self.assertEqual(student.practical_set.count(), 1)

    def test_enrollment_parser_with_tutorial(self):
        '''Student is linked with the appropriate classes'''
        content = "canvi241,L0001,T0002,PRA0001"
        test_file = ContentFile(content.encode())
        enrollment_list_obj = parsers.EnrollmentList(test_file)
        enrollment_list_obj.parse()

        student = Student.objects.get(pk="canvi241")

        self.assertEqual(student.tutorial_set.count(), 1)
        self.assertEqual(student.lecture_set.count(), 1)
        self.assertEqual(student.practical_set.count(), 1)

    def test_enrollment_parser_multi_no_tutorial(self):
        '''Student is linked with the appropriate classes'''
        content = "canvi241,L0001,,PRA0001\r\n" +\
            "racrob58,L0002,,PRA0002"
        test_file = ContentFile(content.encode())
        enrollment_list_obj = parsers.EnrollmentList(test_file)
        enrollment_list_obj.parse()

        for i, row in enumerate(content.split('\r\n')):
            enrollment_string = row.split(',')

            student = Student.objects.get(pk=enrollment_string[0])

            lecture = "L000" + str(i + 1)
            practical = "PRA000" + str(i + 1)

            self.assertEqual(student.lecture_set.get().code, lecture)
            self.assertEqual(student.practical_set.get().code, practical)
            self.assertEqual(student.lecture_set.count(), 1)
            self.assertEqual(student.practical_set.count(), 1)

    def test_add_student_multiple_tutorial(self):
        '''Student is linked with the appropriate classes'''
        content = "canvi241,L0001,T0001,PRA0001\r\n" +\
            "canvi241,L0001,T0002,PRA0001"
        test_file = ContentFile(content.encode())
        enrollment_list_obj = parsers.EnrollmentList(test_file)
        enrollment_list_obj.parse()

        student = Student.objects.get(pk="canvi241")

        for i, row in enumerate(content.split('\r\n')):
            enrollment_string = row.split(',')
            tutorial = "T000" + str(i + 1)

            self.assertEqual(student.tutorial_set.all()[i].code, tutorial)

        self.assertEqual(student.lecture_set.get().code, "L0001")
        self.assertEqual(student.practical_set.get().code, "PRA0001")
        self.assertEqual(student.lecture_set.count(), 1)
        self.assertEqual(student.practical_set.count(), 1)
        self.assertEqual(student.tutorial_set.count(), 2)

    def test_enrollment_parser_multi_with_tutorial(self):
        '''Student is linked with the appropriate classes'''
        content = "canvi241,L0001,T0001,PRA0001\r\n" +\
            "racrob58,L0002,T0002,PRA0002"
        test_file = ContentFile(content.encode())
        enrollment_list_obj = parsers.EnrollmentList(test_file)
        enrollment_list_obj.parse()

        for i, row in enumerate(content.split('\r\n')):
            enrollment_string = row.split(',')

            student = Student.objects.get(pk=enrollment_string[0])

            lecture = "L000" + str(i + 1)
            tutorial = "T000" + str(i + 1)
            practical = "PRA000" + str(i + 1)

            self.assertEqual(student.lecture_set.get().code, lecture)
            self.assertEqual(student.tutorial_set.get().code, tutorial)
            self.assertEqual(student.practical_set.get().code, practical)
            self.assertEqual(student.lecture_set.count(), 1)
            self.assertEqual(student.tutorial_set.count(), 1)
            self.assertEqual(student.practical_set.count(), 1)

    def test_enrollment_parser_multi_no_tutorial_and_with_tutorial(self):
        '''Student is linked with the appropriate classes'''
        content = "canvi241,L0001,,PRA0001\r\n" +\
            "racrob58,L0002,T0002,PRA0002"
        test_file = ContentFile(content.encode())
        enrollment_list_obj = parsers.EnrollmentList(test_file)
        enrollment_list_obj.parse()

        for i, row in enumerate(content.split('\r\n')):
            enrollment_string = row.split(',')

            student = Student.objects.get(pk=enrollment_string[0])

            lecture = "L000" + str(i + 1)
            practical = "PRA000" + str(i + 1)

            if enrollment_string[2] != "":
                tutorial = "T000" + str(i + 1)
                self.assertEqual(student.tutorial_set.get().code, tutorial)
                self.assertEqual(student.tutorial_set.count(), 1)
            else:
                self.assertEqual(student.tutorial_set.count(), 0)

            self.assertEqual(student.lecture_set.get().code, lecture)
            self.assertEqual(student.practical_set.get().code, practical)
            self.assertEqual(student.lecture_set.count(), 1)
            self.assertEqual(student.practical_set.count(), 1)


class TAListParserTests(TestCase):

    def test_ta_parser_empty(self):
        '''No information provided'''
        content = ""
        test_file = ContentFile(content.encode())
        student_list_obj = parsers.TAList(test_file)
        student_list_obj.parse()

        self.assertEqual(TeachingAssistant.objects.count(), 0)

    def test_ta_parser_one(self):
        ''' Information for one TA'''
        content = "canvi241,Cano,Vi,Vi.Cano@nowhere.com"
        test_file = ContentFile(content.encode())
        teaching_assistant_list_obj = parsers.TAList(test_file)
        teaching_assistant_list_obj.parse()

        entry = TeachingAssistant.objects.get(pk="canvi241")
        self.assertEqual(entry.last_name, "Cano")
        self.assertEqual(entry.first_name, "Vi")
        self.assertEqual(entry.email, "Vi.Cano@nowhere.com")

    def test_ta_parser_many(self):
        ''' Information for many TA'''
        content = "couade63,Couchman,Adella,Adella.Couchman@nowhere.com\r\n" + \
            "staild32,Staplins,Ilda,Ilda.Staplins@nowhere.com\r\n" + \
            "bisbea71,Bison,Beatris,Beatris.Bison@nowhere.com"
        test_file = ContentFile(content.encode())
        teaching_assistant_list_obj = parsers.TAList(test_file)
        teaching_assistant_list_obj.parse()

        for row in content.split('\r\n'):
            teaching_assistant_data = row.split(',')

            entry = TeachingAssistant.objects.get(
                pk=teaching_assistant_data[0])
            self.assertEqual(entry.last_name, teaching_assistant_data[1])
            self.assertEqual(entry.first_name, teaching_assistant_data[2])
            self.assertEqual(entry.email, teaching_assistant_data[3])
        self.assertEqual(TeachingAssistant.objects.count(), 3)

    def test_ta_parser_conflict(self):
        ''' If TA with the same information entered twice nothing changes'''
        content = "canvi241,Cano,Vi,Vi.Cano@nowhere.com"
        test_file = ContentFile(content.encode())
        teaching_assistant_list_obj = parsers.TAList(test_file)
        teaching_assistant_list_obj.parse()
        teaching_assistant_list_obj.parse()

        self.assertEqual(TeachingAssistant.objects.count(), 1)

    def test_ta_changed_info(self):
        ''' If ta information updated make sure it is refelected'''
        content = "canvi241,Cano,Vi,209415323,Vi.Cano@nowhere.com\r\n" + \
            "canvi241,Canol,Vi,209415323,Vi.Cano@nowhere.com"
        test_file = ContentFile(content.encode())
        teachong_assistant_obj = parsers.TAList(test_file)
        teachong_assistant_obj.parse()

        self.assertEqual(TeachingAssistant.objects.count(), 1)
        self.assertEqual(TeachingAssistant.objects.get(
            pk="canvi241").last_name, "Canol")

    def test_ta_parser_bad_format(self):
        '''No ta created if not enough information is provided'''
        content = "canvi241"
        test_file = ContentFile(content.encode())
        teaching_assistant_list_obj = parsers.TAList(test_file)
        teaching_assistant_list_obj.parse()

        self.assertEqual(TeachingAssistant.objects.count(), 0)


class MarkParserTest(TestCase):

    def setUp(self):
        self.student1 = Student.objects.create(
            university_id="canvi241",
            first_name="Cano",
            last_name="Vi",
            email="Vi.Cano@nowhere.com",
            student_number="209415323",
        )
        self.student2 = Student.objects.create(
            university_id="racrob58",
            first_name="Racey",
            last_name="Robbin",
            email="Robbin.Racey@nowhere.com",
            student_number="206271143",
        )

    def tearDown(self):
        self.student1.delete()
        self.student2.delete()

    def test_mark_parser_empty(self):
        '''No assignment, rubric or mark created if no info provided'''
        content = ""
        test_file = ContentFile(content.encode())
        mark_file_obj = parsers.MarkFile(test_file)
        mark_file_obj.parse()

        self.assertEqual(Assignment.objects.count(), 0)
        self.assertEqual(Rubric.objects.count(), 0)
        self.assertEqual(Mark.objects.count(), 0)

    def test_create_one_assignment(self):
        '''Create an assignment'''
        content = "''"
        test_file = ContentFile(content.encode())
        mark_file_obj = parsers.MarkFile(test_file)
        mark_file_obj.parse()

        self.assertEqual(Assignment.objects.count(), 1)
        self.assertEqual(Assignment.objects.all()[0].name, "''")
        self.assertEqual(Rubric.objects.count(), 0)
        self.assertEqual(Mark.objects.count(), 0)

    def test_create_one_rubrics(self):
        '''Create one rubric'''
        content = "'',Assignment_001\r\n" + \
            "'',65"
        test_file = ContentFile(content.encode())
        mark_file_obj = parsers.MarkFile(test_file)
        mark_file_obj.parse()

        self.assertEqual(Assignment.objects.count(), 1)
        self.assertEqual(Rubric.objects.count(), 1)
        self.assertEqual(Mark.objects.count(), 0)

    def test_create_multiple_rubrics(self):
        '''Create multiple rubrics'''
        content = "'',Assignment_001,Assignment_002,Assignment_003,Assignment_004,Assignment_005\r\n" + \
            "'',65,94,95,37,108"
        test_file = ContentFile(content.encode())
        mark_file_obj = parsers.MarkFile(test_file)
        mark_file_obj.parse()

        self.assertEqual(Assignment.objects.count(), 1)
        self.assertEqual(Rubric.objects.count(), 5)
        self.assertEqual(Mark.objects.count(), 0)

    def test_create_one_mark(self):
        content = "'',Assignment_001\r\n" + \
            "'',65\r\ncanvi241,54"
        test_file = ContentFile(content.encode())
        mark_file_obj = parsers.MarkFile(test_file)
        mark_file_obj.parse()

        self.assertEqual(Assignment.objects.count(), 1)
        self.assertEqual(Rubric.objects.count(), 1)
        self.assertEqual(Mark.objects.count(), 1)

    def test_create_multiple_marks(self):
        '''Create multiple marks of unique students'''
        content = "'',Assignment_001,Assignment_002,Assignment_003,Assignment_004,Assignment_005\r\n" + \
            "'',65,94,95,37,108\r\ncanvi241,54,58,,18,51"
        test_file = ContentFile(content.encode())
        mark_file_obj = parsers.MarkFile(test_file)
        mark_file_obj.parse()

        self.assertEqual(Assignment.objects.count(), 1)
        self.assertEqual(Rubric.objects.count(), 5)
        self.assertEqual(Mark.objects.count(), 5)

    def test_change_mark(self):
        '''Mark changed if info for student added more than once'''
        content = "'', Assignment_001\r\n'',65\r\n,canvi241,25\r\ncanvi241, 37"
        test_file = ContentFile(content.encode())
        mark_file_obj = parsers.MarkFile(test_file)
        mark_file_obj.parse()

        self.assertEqual(Assignment.objects.count(), 1)
        self.assertEqual(Rubric.objects.count(), 1)
        self.assertEqual(Mark.objects.count(), 1)
        self.assertEqual(Mark.objects.all()[0].value, 37)

    def test_multiple_student_create_one_mark(self):
        '''One rubric and multiple marks for multiple students'''
        content = "'',Assignment_001\r\n" + \
            "'',65\r\ncanvi241,54\r\nracrob58,56"
        test_file = ContentFile(content.encode())
        mark_file_obj = parsers.MarkFile(test_file)
        mark_file_obj.parse()

        self.assertEqual(Assignment.objects.count(), 1)
        self.assertEqual(Rubric.objects.count(), 1)
        self.assertEqual(Mark.objects.count(), 2)

    def test_multiple_student_create_multiple_marks(self):
        '''Multiple rubrics and marks for multiple students'''
        content = "'',Assignment_001,Assignment_002,Assignment_003,Assignment_004,Assignment_005\r\n" + \
            "'',65,94,95,37,108\r\ncanvi241,54,58,,18,51\r\nracrob58,56,61,95,18,72"
        test_file = ContentFile(content.encode())
        mark_file_obj = parsers.MarkFile(test_file)
        mark_file_obj.parse()

        self.assertEqual(Assignment.objects.count(), 1)
        self.assertEqual(Rubric.objects.count(), 5)
        self.assertEqual(Mark.objects.count(), 10)
