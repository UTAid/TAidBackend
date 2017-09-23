from random import choice, randint
from faker import Faker
from string import ascii_lowercase, digits

def _generate_random_char(num_of_char, letters=False):
    output = ""
    for i in range(num_of_char):
        if letters is False:
            output += choice(digits)
        else:
            output += choice(ascii_lowercase)
    return output


def _generate_name():
    name = Faker().name().split()

    while len(name) != 2:
        name = Faker().name().split()

    return name[0], name[1]


def _generate_utorid(first_name, last_name, utor_id_length = 8):
    utorid = ""

    utorid += last_name if len(last_name) < 3 else last_name[:3]
    utorid += first_name if len(first_name) < 3 else first_name[:3]

    utorid += _generate_random_char(utor_id_length - len(utorid))

    return utorid.lower()


def _generate_email(first_name, last_name):
    return first_name + "." + last_name + "@nowhere.com"

def _generate_student_number(length = 9):
    return _generate_random_char(length)

def _generate_id(length=8):
    identity = ""
    for i in range(length):
        identity += choice(digits + ascii_lowercase)
    return identity

def generate_studentlist_file(file_name):
    num_of_students = randint(80, 120)
    student_utorid = []

    file = open(file_name+"_studentList.csv", "w")

    for i in range(num_of_students):
        first_name, last_name = _generate_name()
        utorid = _generate_utorid(first_name, last_name)
        email = _generate_email(first_name, last_name)
        student_number = _generate_student_number()

        student_utorid.append(utorid)

        file.write("{} {} {} {} {} {} {} {}\n".format(utorid, last_name, first_name, student_number, email, _generate_id(), _generate_id(), _generate_id()))

    file.close()

    return student_utorid

def generate_mark_file(utorid, file_name, num_of_assignment=-1):
    row = '"",'
    total_marks = '"",'
    marks = []

    num_of_assignment = randint(3, 6) if num_of_assignment == -1 else num_of_assignment

    file = open(file_name+"_marks.csv", "w")

    for i in range(1, num_of_assignment + 1):
        row += "Assignment{0:0=3d},".format(i)
        marks.append(randint(50, 100))
        total_marks += "{},".format(marks[i-1])

    file.write(row[:-1] + "\n")
    file.write(total_marks[:-1] + "\n")

    for ids in utorid:
        row = "{},".format(ids)
        for mark in marks:
            student_mark = randint(15, mark + 10)
            student_mark = "" if student_mark < 20 else student_mark
            row += "{},".format(student_mark)
        file.write(row[:-1] + "\n")

    file.close()

def generate_enrollmentlist_file(utorid, file_name):
    file = open(file_name+"_enrollmentList.csv", "w")

    for ids in utorid:
        row = "{},".format(ids)
        row += "L{0:0=4d},T{0:0=4d}".format(randint(1, 4), randint(1, 4))
        file.write(row + "\n")

    file.close()

def generate_talist_file(file_name):
    file = open(file_name+"_taList.csv", "w")

    for i in range(randint(6,25)):
        first_name, last_name = _generate_name()
        row = "{},{},{},{}".format(_generate_utorid(first_name, last_name), last_name, first_name, _generate_email(first_name, last_name))
        file.write(row + "\n")

    file.close()

if __name__ == "__main__":
    course_name = input("Enter name of file: ")
    utorid = generate_studentlist_file(course_name)
    generate_mark_file(utorid, course_name)
    generate_enrollmentlist_file(utorid, course_name)
    generate_talist_file(course_name)
