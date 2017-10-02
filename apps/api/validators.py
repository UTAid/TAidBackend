'''Validates if the file given is a csv file'''

import csv
from re import match
from django.core.exceptions import ValidationError


class ColumnError(Exception):
    '''Exception raised if the number of columns in the csv file header does
    not match the rest'''
    pass


class MultipleUtoridOccurences(Exception):
    pass


class InvalidUtorid(Exception):
    pass


class InvalidData(Exception):
    pass


def _is_lowercase_alphabet(value):
    return len(match('[a-z]+', value).group(0)) == len(value)


def _is_alphabet(value):
    return len(match('[A-Za-z]+', value).group(0)) == len(value)


def _is_alphanumeric(value):
    return len(match('[A-Za-z0-9]+', value).group(0)) == len(value)


def _is_alphanumeric_and_symbols(value):
    return len(match('[A-Za-z0-9@_.]+', value).group(0)) == len(value)


def _is_numeric(value):
    return len(match('[0-9]+', value).group(0)) == len(value)


def _valid_utorid(value):
    return len(value) == 8 and _is_alphanumeric(value)


def _valid_student_number(value):
    return (len(value) == 9 or len(value) == 10) and _is_alphanumeric(value)


def _valid_email(value):
    value = value.split('@')
    status = len(match('[A-Za-z.]+', value[0]).group(0)) == len(value[0])
    status = status and len(
        match('[A-Za-z.]+', value[1]).group(0)) == len(value[1])
    return status


def enrollment_validation(value):
    COL_NUMBER = 4

    for line_number, line in enumerate(value, start=1):
        row = line.strip().split(',')
        if len(row) != COL_NUMBER:
            raise ColumnError('Row: {}.\
                Expected: {} columns. Found: {} columns'.format(
                    line_number, COL_NUMBER, len(row)))

        if _valid_utorid(row[0]) is False:
            raise InvalidUtorid(
                'Invalid utorid at row: {}, column: 0'.format(line_number))

        for column in range(1, COL_NUMBER):
            if row[column] != '' and _is_alphanumeric(row[column]) is False:
                raise InvalidData(
                    'Invalid data at row: {}, column: {}'.format(
                        line_number, column))


def mark_validation(value):
    utorid = set()
    error_utorid = set()

    for line_number, line in enumerate(value, start=1):
        row = line.strip().split(',')

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


def student_validation(value):
    COL_NUMBER = 8

    utorid = set()
    error_utorid = set()

    for line_number, line in enumerate(value, start=1):
        row = line.strip().split(',')

        if len(row) != COL_NUMBER:
            raise ColumnError(
                'Row: {}. Expected: {} columns. Found: {} columns'.format(
                    line_number, COL_NUMBER, len(row)))

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

        for column in range(5, COL_NUMBER):
            if row[column] != '' and _is_alphanumeric(row[column]) is False:
                raise InvalidData(
                    'Invaid id at row: {}, col: {}'.format(
                        line_number, column))

    if len(error_utorid) > 0:
        raise MultipleUtoridOccurences(', '.join(error_utorid))


def ta_validation(value):
    COL_NUMBER = 4

    utorid = set()
    error_utorid = set()

    for line_number, line in enumerate(value, start=1):
        row = line.strip().split(',')

        if len(row) != COL_NUMBER:
            raise ColumnError(
                'Row: {}. Expected: {} columns. Found: {} columns'.format(
                    line_number, COL_NUMBER, len(row)))

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
