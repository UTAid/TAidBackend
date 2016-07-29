from django.core.exceptions import ValidationError

import csv


def validate_csv(value):
    if not value.name.endswith(".csv"):
        raise ValidationError("Invalid file type")
    try:
        csvreader = csv.reader(value)
    except csv.Error:
        raise ValidationError("Failed to parse the CSV file")
