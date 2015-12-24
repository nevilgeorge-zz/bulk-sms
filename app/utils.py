# utils.py
import csv
import re

def normalize_number(input_number):
    """Normalizes the format of a given number,
    so that all numbers can have same format."""

    number = re.sub('[^0-9]', '', input_number)
    if len(number) == 10:
        number = '+1{num}'.format(num=number)

    return number


def read_from_txt_file(f):
    """Read numbers from a txt file and normalize them."""

    items = f.readlines()
    numbers = [normalize_number(item) for item in items]

    return numbers


def read_from_csv_file(f):
    """Read numbers from a csv file and normalize them."""

    reader = csv.reader(f, dialect=csv.excel_tab)
    numbers = []
    for row in reader:
        if len(row) != 0:
            number = normalize_number(row[0])
            numbers.append(number)

    return numbers
