from django.apps import apps

import csv


class StudentList(object):
    def __init__(self, file):
        self.file = file
        self.reader = csv.reader(self.file)
        self.results = {}

    def parse(self):
        for i, row in enumerate(self.reader):
            self.results[i] = { "result": None, "message": None }
            try:
                self.results[i] = self._setup_student(row)
            except Exception as e:
                self.results[i]["result"] = "error"
                self.results[i]["message"] = str(e)
        return self.results

    def _setup_student(self, row):
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
            result = { "result": "created", "message": student.pk }
        else:
            result = { "result": "changed", "message": student.pk }

        result["ids"] = []
        for num, val in enumerate(ids, start=1):
            id, created = student.identification_set.update_or_create(
                    value=val,
                    number=num,
                    )
            if created:
                result["ids"].append({ "result": "created", "number": id.number })
            else:
                result["ids"].append({ "result": "changed", "number": id.number })
        return result


class EnrollmentList(object):
    def __init__(self, file):
        self.file = file
        self.reader = csv.reader(self.file)
        self.results = {}

    def parse(self):
        for i, row in enumerate(self.reader):
            self.results[i] = { "result": None, "message": None }
            try:
                self.results[i] = self._setup_enrollment(row)
            except Exception as e:
                self.results[i]["result"] = "error"
                self.results[i]["message"] = str(e)
        return self.results

    def _setup_enrollment(self, row):
        uni_id, lec_id, tut_id, prac_id = row
        _student_model = apps.get_model("api", "Student")
        student = _student_model.objects.get(university_id=uni_id)

        result = { "message": student.pk }

        if lec_id != "":
            _lecture_model = apps.get_model("api", "Lecture")
            lecture = _lecture_model.objects.get(code=lec_id)
            lecture.students.add(student)
            result["lecture"] = { "result": "changed", "message": lecture.code }

        if tut_id != "":
            _tutorial_model = apps.get_model("api", "Tutorial")
            tutorial = _tutorial_model.objects.get(code=tut_id)
            tutorial.students.add(student)
            result["tutorial"] = { "result": "changed", "message": tutorial.code }

        if prac_id != "":
            _practical_model = apps.get_model("api", "Practical")
            practical = _practical_model.objects.get(code=prac_id)
            practical.students.add(student)
            result["practical"] = { "result": "changed", "message": practical.code }

        return result


def mark_parser(assignment, f):
    reader = csv.reader(f)
    names = reader.next()
    totals = reader.next()
    rubrics = _setup_rubric(names, totals)
    for row in reader:
        _setup_mark(rubrics, row)

class MarkFile(object):
    def __init__(self, file):
        self.file = file
        self.reader = csv.reader(self.file)
        self.results = {}

    def parse(self):
        names = self.reader.next()
        totals = self.reader.next()

        _assignment_model = apps.get_model("api", "Assignment")
        self.assignment, created = _assignment_model.objects.get_or_create(name=names[0])
        self.results["message"] = self.assignment.name
        if created:
            self.results["result"] = "created"
        else:
            self.results["result"] = "changed"

        self._setup_rubric(names, totals)

        for i, row in enumerate(self.reader):
            self.results[i] = { "result": None, "message": None }
            try:
                self.results[i] = self._setup_mark(row)
            except Exception as e:
                self.results[i]["result"] = "error"
                self.results[i]["message"] = str(e)
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
        result = { "message": student.pk, "marks": {} }
        for rubric, value in zip(self.rubrics, row[1:]):
            if value == "":
                value = 0.0
            else:
                value = float(value)
            mark, created = _mark_model.objects.update_or_create(
                    value=value, 
                    student=student, 
                    rubric=rubric,
                    )
            if created:
                result["marks"][rubric.name] = { "result": "created", "value": mark.value }
            else:
                result["marks"][rubric.name] = { "result": "changed", "value": mark.value }
        return result
