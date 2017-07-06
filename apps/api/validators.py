'''Validates if the file given is a csv file'''

import csv
from django.core.exceptions import ValidationError


def validate_csv(value):
    '''Validates if a file is a csv file

    Attributes:
        value: is a string which is the name of the file

    Raises:
        ValidationError: if the file is not csv or falied to parse the file
    '''
    if not value.name.endswith(".csv"):
        raise ValidationError("Invalid file type")
    try:
        csv.reader(value)
    except csv.Error:
        raise ValidationError("Failed to parse the CSV file")
