"""
utils.py
Utility helpers for CSV validation and pre-processing.
The functions help to ensure uploaded CSVs match expected columns and types.
"""
import csv
from io import StringIO

def read_csv_stream(file_storage):
    """
    Read a Flask FileStorage object and return a list of dictionaries (rows).
    """
    content = file_storage.stream.read().decode("utf-8")
    reader = csv.DictReader(StringIO(content))
    return list(reader)

def validate_columns(required_columns, csv_columns):
    """
    Check that all required columns are present in csv_columns.
    Returns (True, []) if ok, otherwise (False, missing_columns).
    """
    missing = [c for c in required_columns if c not in csv_columns]
    return (len(missing) == 0, missing)
