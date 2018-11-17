# -*- coding: utf-8 -*-

import os
import pytest
from batch_demographics.model import Batch, Column
from batch_demographics.services.upload import extract_batch_column_headers, automap_batch_columns
from tests.model_tools import create_batches, create_user, update_batch

TEST_FILE_PATH = os.path.join(
    os.path.dirname(__file__),
    'test_files'
)

EXPECTED_TEST_1_COLUMNS_ALL_CORRECT = {
    0: {'name': "FORENAMES", 'mapping': 'FORENAMES'},
    1: {'name': "SURNAME", 'mapping': 'SURNAME'},
    2: {'name': "DOB", 'mapping': 'DOB'},
    3: {'name': "SEX", 'mapping': 'SEX'},
    4: {'name': "POSTCODE", 'mapping': 'POSTCODE'},
    5: {'name': "NHS_NUMBER", 'mapping': 'NHS_NUMBER'},
    6: {'name': "SYSTEM_NUMBER", 'mapping': 'SYSTEM_NUMBER'},
    7: {'name': "ADDRESS1", 'mapping': 'ADDRESS1'},
    8: {'name': "ADDRESS2", 'mapping': 'ADDRESS2'},
    9: {'name': "ADDRESS3", 'mapping': 'ADDRESS3'},
    10: {'name': "ADDRESS4", 'mapping': 'ADDRESS4'},
    11: {'name': "ADDRESS5", 'mapping': 'ADDRESS5'},
    12: {'name': "LOCAL_ID", 'mapping': 'LOCAL_ID'},
}

EXPECTED_TEST_2_COLUMNS_DUPLICATE_COLUMN = {
    0: {'name': "FORENAMES", 'mapping': 'FORENAMES'},
    1: {'name': "SURNAME", 'mapping': 'SURNAME'},
    2: {'name': "SURNAME", 'mapping': ''},
    3: {'name': "SEX", 'mapping': 'SEX'},
    4: {'name': "POSTCODE", 'mapping': 'POSTCODE'},
    5: {'name': "NHS_NUMBER", 'mapping': 'NHS_NUMBER'},
    6: {'name': "SYSTEM_NUMBER", 'mapping': 'SYSTEM_NUMBER'},
    7: {'name': "ADDRESS1", 'mapping': 'ADDRESS1'},
    8: {'name': "ADDRESS2", 'mapping': 'ADDRESS2'},
    9: {'name': "ADDRESS3", 'mapping': 'ADDRESS3'},
    10: {'name': "ADDRESS4", 'mapping': 'ADDRESS4'},
    11: {'name': "ADDRESS5", 'mapping': 'ADDRESS5'},
    12: {'name': "LOCAL_ID", 'mapping': 'LOCAL_ID'},
}

EXPECTED_TEST_3_COLUMNS_EMPTY_COLUMN_NAME = {
    0: {'name': "FORENAMES", 'mapping': 'FORENAMES'},
    1: {'name': "SURNAME", 'mapping': 'SURNAME'},
    2: {'name': "", 'mapping': ''},
    3: {'name': "SEX", 'mapping': 'SEX'},
    4: {'name': "POSTCODE", 'mapping': 'POSTCODE'},
    5: {'name': "NHS_NUMBER", 'mapping': 'NHS_NUMBER'},
    6: {'name': "SYSTEM_NUMBER", 'mapping': 'SYSTEM_NUMBER'},
    7: {'name': "ADDRESS1", 'mapping': 'ADDRESS1'},
    8: {'name': "ADDRESS2", 'mapping': 'ADDRESS2'},
    9: {'name': "ADDRESS3", 'mapping': 'ADDRESS3'},
    10: {'name': "ADDRESS4", 'mapping': 'ADDRESS4'},
    11: {'name': "ADDRESS5", 'mapping': 'ADDRESS5'},
    12: {'name': "LOCAL_ID", 'mapping': 'LOCAL_ID'},
}

EXPECTED_TEST_4_COLUMNS_INCLUDING_SPACES = {
    0: {'name': "FORE NAMES", 'mapping': 'FORENAMES'},
    1: {'name': "SUR NAME", 'mapping': 'SURNAME'},
    2: {'name': "D O B", 'mapping': "DOB"},
    3: {'name': "S E X", 'mapping': 'SEX'},
    4: {'name': "POST CODE", 'mapping': 'POSTCODE'},
    5: {'name': "NHS NUMBER", 'mapping': 'NHS_NUMBER'},
    6: {'name': "SYSTEM NUMBER", 'mapping': 'SYSTEM_NUMBER'},
    7: {'name': "    A\tDDRESS 1", 'mapping': 'ADDRESS1'},
    8: {'name': "ADDRESS 2", 'mapping': 'ADDRESS2'},
    9: {'name': "ADDRESS 3", 'mapping': 'ADDRESS3'},
    10: {'name': "ADDRESS 4", 'mapping': 'ADDRESS4'},
    11: {'name': "ADDRESS 5", 'mapping': 'ADDRESS5'},
    12: {'name': "LOCAL ID", 'mapping': 'LOCAL_ID'},
}

EXPECTED_TEST_5_COLUMNS_INCLUDING_PUNCTUATION = {
    0: {'name': '"FORENAMES"', 'mapping': 'FORENAMES'},
    1: {'name': "\tSURNAME", 'mapping': 'SURNAME'},
    2: {'name': "D.O.B.", 'mapping': "DOB"},
    3: {'name': "'SEX", 'mapping': 'SEX'},
    4: {'name': "POST-CODE", 'mapping': 'POSTCODE'},
    5: {'name': "NHS=NUMBER", 'mapping': 'NHS_NUMBER'},
    6: {'name': "SYSTEM+NUMBER:", 'mapping': 'SYSTEM_NUMBER'},
    7: {'name': "^ADDRESS~1;", 'mapping': 'ADDRESS1'},
    8: {'name': "#ADDRESS%2,", 'mapping': 'ADDRESS2'},
    9: {'name': "A/DDRESS$3?", 'mapping': 'ADDRESS3'},
    10: {'name': "A£DDR€ESS&4!", 'mapping': 'ADDRESS4'},
    11: {'name': "AD!DRESS*5`¬", 'mapping': 'ADDRESS5'},
    12: {'name': "(<LOC¦AL ID>|)", 'mapping': 'LOCAL_ID'},
}

EXPECTED_TEST_6_COLUMNS_LOWERCASE = {
    0: {'name': "forenames", 'mapping': 'FORENAMES'},
    1: {'name': "surname", 'mapping': 'SURNAME'},
    2: {'name': "dob", 'mapping': 'DOB'},
    3: {'name': "sex", 'mapping': 'SEX'},
    4: {'name': "postcode", 'mapping': 'POSTCODE'},
    5: {'name': "nhs_number", 'mapping': 'NHS_NUMBER'},
    6: {'name': "system_number", 'mapping': 'SYSTEM_NUMBER'},
    7: {'name': "address1", 'mapping': 'ADDRESS1'},
    8: {'name': "address2", 'mapping': 'ADDRESS2'},
    9: {'name': "address3", 'mapping': 'ADDRESS3'},
    10: {'name': "address4", 'mapping': 'ADDRESS4'},
    11: {'name': "address5", 'mapping': 'ADDRESS5'},
    12: {'name': "local_id", 'mapping': 'LOCAL_ID'},
}

EXPECTED_TEST_7_COLUMNS_ALTERNATIVES = {
    0: {'name': "forename", 'mapping': 'FORENAMES'},
    1: {'name': "lastname", 'mapping': 'SURNAME'},
    2: {'name': "date of birth", 'mapping': 'DOB'},
    3: {'name': "gender", 'mapping': 'SEX'},
    4: {'name': "postal code", 'mapping': 'POSTCODE'},
    5: {'name': "snumber", 'mapping': 'SYSTEM_NUMBER'},
}

EXPECTED_TEST_8_COLUMNS_ALTERNATIVES = {
    0: {'name': "first name", 'mapping': 'FORENAMES'},
    1: {'name': "family name", 'mapping': 'SURNAME'},
    2: {'name': "birth date", 'mapping': 'DOB'},
    3: {'name': "uhlsnumber", 'mapping': 'SYSTEM_NUMBER'},
}

EXPECTED_TEST_9_COLUMNS_ALTERNATIVES = {
    0: {'name': "first names", 'mapping': 'FORENAMES'},
    1: {'name': "uhl system number", 'mapping': 'SYSTEM_NUMBER'},
}

EXPECTED_TEST_10_COLUMNS_ALTERNATIVES = {
    0: {'name': "given name", 'mapping': 'FORENAMES'},
}

EXPECTED_TEST_11_COLUMNS_ALTERNATIVES = {
    0: {'name': "given names", 'mapping': 'FORENAMES'},
}


@pytest.mark.parametrize("filename, expected", [
    ('test_1.csv', EXPECTED_TEST_1_COLUMNS_ALL_CORRECT),
    ('test_1.tsv', EXPECTED_TEST_1_COLUMNS_ALL_CORRECT),
    ('test_1.psv', EXPECTED_TEST_1_COLUMNS_ALL_CORRECT),
    ('test_2.csv', EXPECTED_TEST_2_COLUMNS_DUPLICATE_COLUMN),
    ('test_3.csv', EXPECTED_TEST_3_COLUMNS_EMPTY_COLUMN_NAME),
])
def test_services_upload__csv_headers__correct(client, faker, upload_files, filename, expected):
    u = create_user(faker)

    batch = create_batches(u, 1, faker)[0]
    batch.filename = filename
    update_batch(batch)

    upload_files.copy_file_in(batch, TEST_FILE_PATH, filename)

    extract_batch_column_headers(batch)

    assert len(batch.columns) == 13
    assert {c.column_index: c.name for c in batch.columns} == {i: e['name'] for i, e in expected.items()}


@pytest.mark.parametrize("columns", [
    (EXPECTED_TEST_1_COLUMNS_ALL_CORRECT),
    (EXPECTED_TEST_2_COLUMNS_DUPLICATE_COLUMN),
    (EXPECTED_TEST_3_COLUMNS_EMPTY_COLUMN_NAME),
    (EXPECTED_TEST_4_COLUMNS_INCLUDING_SPACES),
    (EXPECTED_TEST_5_COLUMNS_INCLUDING_PUNCTUATION),
    (EXPECTED_TEST_6_COLUMNS_LOWERCASE),
    (EXPECTED_TEST_7_COLUMNS_ALTERNATIVES),
    (EXPECTED_TEST_8_COLUMNS_ALTERNATIVES),
    (EXPECTED_TEST_9_COLUMNS_ALTERNATIVES),
    (EXPECTED_TEST_10_COLUMNS_ALTERNATIVES),
    (EXPECTED_TEST_11_COLUMNS_ALTERNATIVES),
])
def test_services_upload__automap__correct(client, faker, upload_files, columns):
    u = create_user(faker)

    batch = create_batches(u, 1, faker)[0]

    for index, c in columns.items():
        batch.columns.append(
            Column(column_index=index, name=c['name'], batch_id=batch.id)
        )

    update_batch(batch)

    automap_batch_columns(batch)

    expected = {i: e['mapping'] for i, e in columns.items()}

    assert {c.column_index: c.mapping for c in batch.columns} == expected
