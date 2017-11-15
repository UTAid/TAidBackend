'''Creates csv files for testing'''

from random import choice, randint
from string import ascii_lowercase, digits
from faker import Faker


def _generate_random_char(num_of_char, letters=False):
    '''Generates specified amount of random characters. Either letters or numbers

    Args:
        num_of_char: int specifying the number of characters to return
        letters: bool set as false by default. If false no letters and only
            numbers. If true only letters and no numbers

    Return:
        Returns str of randomly generated characters
    '''
    output = ""
    for i in range(num_of_char):
        if letters is False:
            output += choice(digits)
        else:
            output += choice(ascii_lowercase)
    return output


def _generate_name():
    '''Generates a random name

    Return:
        Returns two string values. First parameter is the first name and second
        is the last name
    '''
    name = Faker().name().split()

    while len(name) != 2:
        name = Faker().name().split()

    return name[0], name[1]


def _generate_utorid(first_name, last_name, utor_id_length=8):
    '''Generates utor id from the person's first and last name

    Args:
        first_name: str of the person's first name
        last_name: str of the person's last name
        utor_id_length: int set as 8 by deafult. This is the length of the
            random utor id to be generated

    Return:
        Returns a string of the randomly generated utor id. Ex - jorcar75,
        usually 6 characters followed by 2 numbers
    '''
    utorid = last_name if len(last_name) < 3 else last_name[:3]
    utorid += first_name if len(first_name) < 3 else first_name[:3]

    utorid += _generate_random_char(utor_id_length - len(utorid))

    return utorid.lower()


def _generate_email(first_name, last_name):
    '''Generates email address from a person's first and last name

    Args:
        first_name: str of the person's first name
        last_name: str of the person's last name

    Return:
        Returns a string which contains an email address generated from the
        person's first and last name. Ex - first_name.last_name@nowhere.com
    '''
    return first_name + "." + last_name + "@nowhere.com"


def _generate_student_number(length=9):
    '''Generates student number which is generated randomly

    Args:
        length: int is set as 9 by default. This determines the length of the
            student number

    Return:
        Returns a string which contains a randomly generated student number.
        Ex - 209415323
    '''
    return _generate_random_char(length, False)


def _generate_id(length=8):
    '''Generates an id which is randomly generated

    Args:
        length: int is set as 8 by default. This determines the length of
        the id

    Return:
        Returns a string which contains randomly generated id. Ex - vi2c1na4
        it contais letters and numbers at random locations
    '''
    identity = ""
    for i in range(length):
        identity += choice(digits + ascii_lowercase)
    return identity


def generate_studentlist_file(file_name):
    '''Generates student list test file

    Args:
        file_name: str which contains the name of the file to write to

    Return:
        Returns a list of str containing utor id of students.
        Also creates a csv file of the format utorid,last_name,first_name,
        student_number,email,id,id,id
    '''
    num_of_students = randint(80, 120)
    student_utorid = []

    file = open(file_name + "_studentList.csv", "w")

    for i in range(num_of_students):
        first_name, last_name = _generate_name()
        utorid = _generate_utorid(first_name, last_name)
        email = _generate_email(first_name, last_name)
        student_number = _generate_student_number()

        student_utorid.append(utorid)

        file.write("{} {} {} {} {} {} {} {}\n".format(
            utorid, last_name, first_name, student_number, email, _generate_id(
            ), _generate_id(), _generate_id()))

    file.close()

    return student_utorid


def generate_mark_file(utorid, file_name, num_of_assignment=-1):
    '''Generates mark test file

    Args:
        utorid: list of str which contains utor id of students. Assigns marks
            to assignments for these students
        file_name: str which contains the name of the file to write to
        num_of_assignment: int which is set as -1 by default. If it is -1
            randomly decides the number of assignments. If not -1 then
            generates info for that many assignments

    Return:
        Returns None.
        Creates a csv file of the format -
            "",Assignment_001,Assignment_002,Assignment_003
            "",assignment1_total, assignment2_total, assignment3_total
            utorid,student_mark1, student_mark2, student_mark3
    '''
    row = '"",'
    total_marks = '"",'
    marks = []

    num_of_assignment = randint(
        3, 6) if num_of_assignment == -1 else num_of_assignment

    file = open(file_name + "_marks.csv", "w")

    for i in range(1, num_of_assignment + 1):
        row += "Assignment{0:0=3d},".format(i)
        marks.append(randint(50, 100))
        total_marks += "{},".format(marks[i - 1])

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
    '''Generates enrollment test file

    Args:
        utorid: list of str which contains utor id of students. Assigns
            students to different practicals and tutorials
        file_name: str which contains the name of the file to write to

    Return:
        Returns None.
        Creates a csv file of the format -
            utorid, lecture_number, tutoral_number, practical_number
    '''
    file = open(file_name + "_enrollmentList.csv", "w")

    for ids in utorid:
        row = "{},".format(ids)
        row += "L{0:0=4d},T{0:0=4d},P{0:0=4d}".format(
            randint(1, 4), randint(1, 4), randint(1, 4))
        file.write(row + "\n")

    file.close()


def generate_talist_file(file_name):
    '''Generates TA test file

    Args:
        file_name: str which contains the name of the file to write to

    Return:
        Returns None.
        Creates a csv file of the format -
            utorid,last_name,first_name,email
    '''
    file = open(file_name + "_taList.csv", "w")

    for i in range(randint(6, 25)):
        first_name, last_name = _generate_name()
        row = "{},{},{},{}".format(_generate_utorid(
            first_name, last_name), last_name, first_name, _generate_email(
                first_name, last_name))
        file.write(row + "\n")

    file.close()


def main():
    '''Generates student list, mark, enrollemnt list and ta list file

    Return:
        Returns None.
        Creates csv files for student list, mark, enrollemnt list and ta
        list file
    '''
    course_name = input("Enter name of file: ")
    utorid_list = generate_studentlist_file(course_name)
    generate_mark_file(utorid_list, course_name)
    generate_enrollmentlist_file(utorid_list, course_name)
    generate_talist_file(course_name)


if __name__ == "__main__":
    main()
