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

def generate_studentlist_file():
    num_of_students = randint(80, 120 + 1)
    student_utorid = []

    for i in range(num_of_students):
        first_name, last_name = _generate_name()
        utorid = _generate_utorid(first_name, last_name)
        email = _generate_email(first_name, last_name)
        student_number = _generate_student_number()

        student_utorid.append(utorid)

        row = "{} {} {} {} {} {} {} {}".format(utorid, last_name, first_name, student_number, email, _generate_id(), _generate_id(), _generate_id())

    return student_utorid

generate_studentlist_file()
