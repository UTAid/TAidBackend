'''Validates if the file given is a csv file'''

import csv
from re import match
from django.core.exceptions import ValidationError


class ColumnError(Exception):
    '''Exception raised if the number of columns in the csv file header does
    not match the rest'''
    pass


class MultipleUtoridOccurences(Exception):
    '''Exception raised if the same utor id occurs multiple times in a file
    '''
    pass


class InvalidUtorid(Exception):
    '''Utor id not valid. It has to be 8 characters long and only contain
    alphanumberic symbols
    '''
    pass


class InvalidData(Exception):
    '''If the data at a given column does not have the proper structure or
    seem valid
    '''
    pass


def _is_lowercase_alphabet(value):
    '''Check if the given parameter is entirely lowercase

    Attribute:
        value: str

    Returns:
        A boolean that determines if the parameter 'value' is completely
        lowercase or not
    '''
    return len(match('[a-z]+', value).group(0)) == len(value)


def _is_alphabet(value):
    '''Check if the given parameter is an alphabet either upper or lowercase

    Attribute:
        value: str

    Returns:
        A boolean that determines if the parameter 'value' is composed
        entirely of alphabet characters
    '''
    return len(match('[A-Za-z]+', value).group(0)) == len(value)


def _is_alphanumeric(value):
    '''Check if the given parameter is composed of alphabet and numeric
    characters

    Attribute:
        value: str

    Returns:
        A boolean that determines if the parameter 'value' is composed of
        alphabet and numeric characters
    '''
    return len(match('[A-Za-z0-9]+', value).group(0)) == len(value)


def _is_alphanumeric_and_symbols(value):
    '''Check if the given parameter is composed of alphabet, numeric and
    certain symbols

    Attribute:
        value: str

    Returns:
        A boolean that determines if the parameter 'value' is composed of
        alphabet, numeric and certain symbol characters
    '''
    return len(match('[A-Za-z0-9_.!@#$%^&*()\' ]+', value).group(0)) == len(value)


def _is_numeric(value):
    '''Check if the given parameter is composed of numeric characters

    Attribute:
        value: str

    Returns:
        A boolean that determines if the parameter 'value' is composed of
        numberic characters
    '''
    return len(match('[0-9]+', value).group(0)) == len(value)


def _valid_utorid(value):
    '''Check if the given parameter is a valid utorid

    Attribute:
        value: str

    Returns:
        A boolean that determines if the parameter 'value' is a valid utorid.
        Utor id is 8 characters in length and composed of alphabet and number
    '''
    return len(value) == 8 and _is_alphanumeric(value)


def _valid_student_number(value):
    '''Check if the given parameter is a valid student number

    Attribute:
        value: str

    Returns:
        A boolean that determines if the parameter 'value' is a valid student
        number. A student number has 9 or 10 number digits
    '''
    return (len(value) == 9 or len(value) == 10) and _is_alphanumeric(value)


def _valid_email(value):
    '''Check if the given parameter is a valid email

    Attribute:
        value: str

    Returns:
        A boolean that determines if the parameter 'value' is an email
    '''
    value = value.split('@')
    username = len(match('[A-Za-z.]+', value[0]).group(0)) == len(value[0])
    domain_name = len(match('[A-Za-z.]+', value[1]).group(0)) == len(value[1])
    return username and domain_name


def enrollment_validation(value, col_number=4):
    '''Validation for enrollment list files

    Attributes:
        value: Open csv file object. Contents of file. Has to be of format:
            uni_id, lec_id, tut_id, prac_id
        col_number: int. It is set to 4 as default. It says how many columns
                the file should have

    Raises:
        ColumnError: if there are more columns present than that specified in
            col_number parameter
        InvalidUtorid: if the utorid is not valid
        InvalidData: if the data present in the given column is not the
            specified format
        MultipleUtoridOccurences: if an utorid appears multiple times
    '''
    utorid = set()
    error_utorid = set()

    for line_number, line in enumerate(value, start=1):
        row = (line.decode('ascii')).strip().split(',')
        if len(row) != col_number:
            raise ColumnError(
                'Row: {}. Expected: {} columns. Found: {} columns'.format(
                    line_number, col_number, len(row)))

        if _valid_utorid(row[0]) is False:
            raise InvalidUtorid(
                'Invalid utorid at row: {}, column: 0'.format(line_number))

        if row[0] not in utorid:
            utorid.add(row[0])
        else:
            error_utorid.add(row[0])

        for column in range(1, col_number):
            if row[column] != '' and _is_alphanumeric(row[column]) is False:
                raise InvalidData(
                    'Invalid data at row: {}, column: {}'.format(
                        line_number, column))

    if len(error_utorid) > 0:
        raise MultipleUtoridOccurences(', '.join(error_utorid))


def mark_validation(value):
    '''Validation for mark files

    Attribute:
        value: Open csv file object. Contents of file. Has to be of format:
            assignment_name, rubric_name_1, ... , rubric_name_n
            "",rubric_total_1, ... , rubric_total_n
            university_id, rubric_mark_1, ... , rubric_mark_n

    Raises:
        ColumnError: if there are more columns present than that specified in
            the header of the csv file
        InvalidUtorid: if the utorid is not valid
        InvalidData: if the data present in the given column is not the
            specified format
        MultipleUtoridOccurences: if an utorid appears multiple times
    '''
    utorid = set()
    error_utorid = set()

    for line_number, line in enumerate(value, start=1):
        row = (line.decode('ascii')).strip().split(',')

        if line_number == 1:
            col_number = len(row)
            for column in range(0, col_number):
                if row[column] != '""' and _is_alphanumeric_and_symbols(
                 row[column]) is False:
                    raise InvalidData(
                        'Invalid data at row: {}, column: {}'.format(
                            line_number, column + 1))
        elif line_number == 2:
            if len(row) != col_number:
                raise ColumnError(
                    'Row: {}. Expected: {} columns. Found: {} columns'.format(
                        line_number, col_number, len(row)))

            for column in range(0, col_number):
                if row[column] != '""' and _is_alphanumeric_and_symbols(
                 row[column]) is False:
                    raise InvalidData(
                        'Invalid data at row: {}, column: {}'.format(
                            line_number, column + 1))
        else:
            if len(row) != col_number:
                raise ColumnError(
                    'Row: {}. Expected: {} columns. Found: {} columns'.format(
                        line_number, col_number, len(row)))

            if _valid_utorid(row[0]) is False:
                raise InvalidUtorid(
                    'Invalid utorid at row: {}, column: 0'.format(line_number))

            if row[0] not in utorid:
                utorid.add(row[0])
            else:
                error_utorid.add(row[0])

            for column in range(1, col_number):
                if row[column] != '' and _is_numeric(row[column]) is False:
                    raise InvalidData(
                        'Invalid data at row: {}, column: {}'.format(
                            line_number, column))

    if len(error_utorid) > 0:
        raise MultipleUtoridOccurences(', '.join(error_utorid))


def student_validation(value, col_number=8):
    '''Validation for student list files

    Attributes:
        value: Open file object. Contents of file. Has to be of format:
            uni_id, last_name, first_name, number, email, id, id, id
        col_number: int. It is set to 8 as default. It says how many columns
                the file should have

    Raises:
        ColumnError: if there are more columns present than that specified in
            col_number parameter
        InvalidUtorid: if the utorid is not valid
        InvalidData: if the data present in the given column is not the
            specified format
        MultipleUtoridOccurences: if an utorid appears multiple times
    '''
    utorid = set()
    error_utorid = set()

    for line_number, line in enumerate(value, start=1):
        row = (line.decode('ascii')).strip().split(',')

        if len(row) != col_number:
            raise ColumnError(
                'Row: {}. Expected: {} columns. Found: {} columns'.format(
                    line_number, col_number, len(row)))

        if _valid_utorid(row[0]) is False:
            raise InvalidUtorid(
                'Invalid utorid at row: {}, column: 0'.format(line_number))

        if row[0] not in utorid:
            utorid.add(row[0])
        else:
            error_utorid.add(row[0])

        if _is_alphabet(row[1]) is False:
            raise InvalidData(
                'Invaid first name at row: {}'.format(line_number))

        if _is_alphabet(row[2]) is False:
            raise InvalidData(
                'Invaid last name at row: {}'.format(line_number))

        if _valid_student_number(row[3]) is False:
            raise InvalidData(
                'Invaid student number at row: {}'.format(line_number))

        if _valid_email(row[4]) is False:
            raise InvalidData('Invaid email at row: {}'.format(line_number))

        for column in range(5, col_number):
            if row[column] != '' and _is_alphanumeric(row[column]) is False:
                raise InvalidData(
                    'Invaid id at row: {}, col: {}'.format(
                        line_number, column))

    if len(error_utorid) > 0:
        raise MultipleUtoridOccurences(', '.join(error_utorid))


def ta_validation(value, col_number=4):
    '''Validation for ta list files

    Attributes:
        value: Open csv file object. Contents of file. Has to be of format:
            uni_id, last_name, first_name, email
        col_number: int. It is set to 4 as default. It says how many columns
                the file should have

    Raises:
        ColumnError: if there are more columns present than that specified in
            col_number parameter
        InvalidUtorid: if the utorid is not valid
        InvalidData: if the data present in the given column is not the
            specified format
        MultipleUtoridOccurences: if an utorid appears multiple times
    '''
    utorid = set()
    error_utorid = set()

    for line_number, line in enumerate(value, start=1):
        row = (line.decode('ascii')).strip().split(',')

        if len(row) != col_number:
            raise ColumnError(
                'Row: {}. Expected: {} columns. Found: {} columns'.format(
                    line_number, col_number, len(row)))

        if _valid_utorid(row[0]) is False:
            raise InvalidUtorid(
                'Invalid utorid at row: {}, column: 0'.format(line_number))

        if row[0] not in utorid:
            utorid.add(row[0])
        else:
            error_utorid.add(row[0])

        if _is_alphabet(row[1]) is False:
            raise InvalidData(
                'Invaid first name at row: {}'.format(line_number))

        if _is_alphabet(row[2]) is False:
            raise InvalidData(
                'Invaid last name at row: {}'.format(line_number))

        if _valid_email(row[3]) is False:
            raise InvalidData('Invaid email at row: {}'.format(line_number))

    if len(error_utorid) > 0:
        raise MultipleUtoridOccurences(', '.join(error_utorid))


def validate_csv(value):
    '''Validates if a file is a csv file

    Attributes:
        value: is a file object

    Raises:
        ValidationError: if the file is not csv or falied to parse the file
    '''
    if not value.name.endswith(".csv"):
        raise ValidationError("Invalid file type")
    try:
        csv.reader(value)
    except csv.Error:
        raise ValidationError("Failed to parse the CSV file")
