'''Populates the database based on the csv files provided'''

from csv import reader
from django.apps import apps


class StudentList(object):
    '''Populates database with students and their information
    Attributes:
        file: Open csv file object. Contents of file. Has to be of format:
            uni_id, last_name, first_name, number, email, id, id, id
        reader: Reader oject which can iterate over lines in given csv file
        results: A dictionary of the format {int: {'result':'', 'message':''}}
    '''

    def __init__(self, file):
        ''' Inits StudentList given an open file object
        '''
        self.file = file
        self.reader = reader(self.file)
        self.results = {}

    def parse(self):
        '''Updates the models and returns a dict of dict
        Returns:
            A dict of dict. Maps the i-th row to its corresponding data. Ex-
            {int: {'result': '', 'message': ""}}
            Result can be 3 cases -
                error: if models could not be updated. Message describes the
                    error
                created: create a new student on the database with provided
                    info. Message is the uni_id which is the primary_key
                changed: a student with that info already exists in database
                    therefore updates info with the one found in csv file.
                    Message is the uni_id which is the primary_key
        Excepts:
            Excepts all errors but most likely it is for
            django.core.exceptions.AppRegistryNotReady
        '''
        for i, row in enumerate(self.reader):
            self.results[i] = {"result": None, "message": None}
            try:
                self.results[i] = self._setup_student(row)
            except Exception as exception:
                self.results[i]["result"] = "error"
                self.results[i]["message"] = str(exception)
        return self.results

    def _setup_student(self, row):
        '''Updates the database
        Args:
            row: list of string. Contains 7 elements of the format
                [uni_id, last_name, first_name, number, email, id, id, id]
        Returns:
            A dict of dict of the format {int: {'result': '', 'message': ""}}
            Result can be 2 cases -
                created: create a new student on the database with provided
                    info
                changed: a student with that info already exists in database
                    therefore updates info with the one found in csv file
            These 2 cases are determined by comparing the ids with that present
            in the database
        '''
        info, ids = row[:5], row[5:]
        uni_id, last_name, first_name, number, email = info

        _student_model = apps.get_model("api", "Student")
        student, created = _student_model.objects.update_or_create(
            university_id=uni_id,
            first_name=first_name,
            last_name=last_name,
            student_number=number,
            email=email,
        )
        if created:
            result = {"result":
                      "created", "message": student.pk}
        else:
            result = {"result": "changed", "message": student.pk}

        result["ids"] = []
        for num, val in enumerate(ids, start=1):
            identity, created = student.identification_set.update_or_create(
                value=val,
                number=num,
            )
            if created:
                result["ids"].append(
                    {"result": "created", "number": identity.number})
            else:
                result["ids"].append(
                    {"result": "changed", "number": identity.number})
        return result


class EnrollmentList(object):
    '''Populates database with students and the lecture, tutorials and
        practicals they are enrolled in
    Attributes:
        file: Open csv file object. Contents of file. Has to be of format:
            uni_id, lec_id, tut_id, prac_id
        reader: Reader oject which can iterate over lines in given csvfile
        results: A dictionary of the format {int: {'result':'', 'message':''}}
    '''

    def __init__(self, file):
        '''Inits EnrollmentList given an open file object
        '''
        self.file = file
        self.reader = reader(self.file)
        self.results = {}

    def parse(self):
        '''Updates the models and returns a dict of dict
        Returns:
            A dict of dict. Maps the i-th row to its corresponding data. Ex-
            {int: {'result': '', 'message': ""}}
            Result can be 3 cases -
                error: if models could not be updated. Message describes
                    the error
                changed: changes the lecture, tutorial or practical associated
                    with the student. Message is the uni_id, lec_id, tut_id
                    or prac_id
        Excepts:
            Excepts all errors but most likely it is for
            django.core.exceptions.AppRegistryNotReady
        '''
        for i, row in enumerate(self.reader):
            self.results[i] = {"result": None, "message": None}
            try:
                self.results[i] = self._setup_enrollment(row)
            except Exception as exception:
                self.results[i]["result"] = "error"
                self.results[i]["message"] = str(exception)
        return self.results

    def _setup_enrollment(self, row):
        '''Updates the database
        Args:
            row: list of string. Contains 4 elements of the format
                [uni_id, lec_id, tut_id, prac_id]
                lec_id, tut_id and prac_id can be empty strings
        Returns:
            A dict of dict of the format {int: {'result': '', 'message': ""}}
            Result can be empty or -
                changed: this is when the lecture, tutorial or practical
                    associated with the student is changed
        '''
        uni_id, lec_id, tut_id, prac_id = row
        _student_model = apps.get_model("api", "Student")
        student = _student_model.objects.get(university_id=uni_id)

        result = {"message": student.pk}

        if lec_id != "":
            _lecture_model = apps.get_model("api", "Lecture")
            lecture = _lecture_model.objects.get(code=lec_id)
            lecture.students.add(student)
            result["lecture"] = {"result": "changed", "message": lecture.code}

        if tut_id != "":
            _tutorial_model = apps.get_model("api", "Tutorial")
            tutorial = _tutorial_model.objects.get(code=tut_id)
            tutorial.students.add(student)
            result["tutorial"] = {
                "result": "changed", "message": tutorial.code}

        if prac_id != "":
            _practical_model = apps.get_model("api", "Practical")
            practical = _practical_model.objects.get(code=prac_id)
            practical.students.add(student)
            result["practical"] = {
                "result": "changed", "message": practical.code}

        return result


class MarkFile(object):
    def __init__(self, file):
        self.file = file
        self.reader = reader(self.file)
        self.results = {}

    def parse(self):
        names = self.reader.next()
        totals = self.reader.next()

        _assignment_model = apps.get_model("api", "Assignment")
        self.assignment, created = _assignment_model.objects.get_or_create(
            name=names[0])
        self.results["message"] = self.assignment.name
        if created:
            self.results["result"] = "created"
        else:
            self.results["result"] = "changed"

        self._setup_rubric(names, totals)

        for i, row in enumerate(self.reader):
            self.results[i] = {"result": None, "message": None}
            try:
                self.results[i] = self._setup_mark(row)
            except Exception as exception:
                self.results[i]["result"] = "error"
                self.results[i]["message"] = str(exception)
        return self.results

    def _setup_rubric(self, names, totals):
        self.rubrics = []
        for name, total in zip(names[1:], totals[1:]):
            rubric, _ = self.assignment.rubric_entries.get_or_create(
                name=name,
                total=total,
                assignment=self.assignment,
            )
            self.rubrics.append(rubric)

    def _setup_mark(self, row):
        _student_model = apps.get_model("api", "Student")
        _mark_model = apps.get_model("api", "Mark")
        student = _student_model.objects.get(university_id=row[0])
        result = {"message": student.pk, "marks": {}}
        for rubric, value in zip(self.rubrics, row[1:]):
            if value != "":
                value = float(value)
            mark, created = _mark_model.objects.update_or_create(
                value=value,
                student=student,
                rubric=rubric,
            )
            if created:
                result["marks"][rubric.name] = {
                    "result": "created", "value": mark.value}
            else:
                result["marks"][rubric.name] = {
                    "result": "changed", "value": mark.value}
        return result


class TAList(object):
    '''Populates database with TA information
    Attributes:
        file: Open csv file object. Contents of file. Has to be of format:
            uni_id, last_name, first_name, email
        reader: Reader oject which can iterate over lines in given csv file
        results: A dictionary of the format {int: {'result':'', 'message':''}}
    '''

    def __init__(self, file):
        '''Inits TAList given an open file object
        '''
        self.file = file
        self.reader = reader(self.file)
        self.results = {}

    def parse(self):
        '''Updates the models and returns a dict of dict
        Returns:
            A dict of dict. Maps the i-th row to its corresponding data. Ex-
            {int: {'result': '', 'message': ""}}
            Result can be 3 cases -
                error: if models could not be updated. Message describes
                    the error
                created: if TA is not present in database creates it. Message
                    is uni_id
                changed: if TA is present then changes the info. Message is
                    uni_id
        Excepts:
            Excepts all errors but most likely it is for
            django.core.exceptions.AppRegistryNotReady
        '''
        for i, row in enumerate(self.reader):
            self.results[i] = {"result": None, "message": None}
            try:
                self.results[i] = self._setup_ta(row)
            except Exception as exception:
                self.results[i]["result"] = "error"
                self.results[i]["message"] = str(exception)
        return self.results

    def _setup_ta(self, row):
        '''Updates the database
        Args:
            row: list of string. Contains 4 elements of the format
                [uni_id, last_name, first_name, email]
        Returns:
            A dict of dict of the format {int: {'result': '', 'message': ""}}
            Result can be 2 cases -
                created: create a new TA on the database with provided
                    info. Message is uni_id
                changed: changes the info of a TA that is already present in
                    the database. Message is uni_id
        '''
        uni_id, last_name, first_name, email = row[:4]

        _ta_model = apps.get_model("api", "TeachingAssistant")
        teaching_assistant, created = _ta_model.objects.update_or_create(
            university_id=uni_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        if created:
            result = {"result": "created", "message": teaching_assistant.pk}
        else:
            result = {"result": "changed", "message": teaching_assistant.pk}
        return result
