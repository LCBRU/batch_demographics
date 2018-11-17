# -*- coding: utf-8 -*-

import os
import pytest
from batch_demographics.model import Batch, Column
from batch_demographics.services.upload import extract_batch_column_headers
from tests.model_tools import create_batches, create_user, update_batch

TEST_FILE_PATH = os.path.join(
    os.path.dirname(__file__),
    'test_files'
)

EXPECTED_TEST_1_COLUMNS_ALL_CORRECT = {
    1: {'name': "FORENAMES", 'mapping': 'FORENAMES'},
    2: {'name': "SURNAME", 'mapping': 'SURNAME'},
    3: {'name': "DOB", 'mapping': 'DOB'},
    4: {'name': "SEX", 'mapping': 'SEX'},
    5: {'name': "POSTCODE", 'mapping': 'POSTCODE'},
    6: {'name': "NHS_NUMBER", 'mapping': 'NHS_NUMBER'},
    7: {'name': "SYSTEM_NUMBER", 'mapping': 'SYSTEM_NUMBER'},
    8: {'name': "ADDRESS1", 'mapping': 'ADDRESS1'},
    9: {'name': "ADDRESS2", 'mapping': 'ADDRESS2'},
    10: {'name': "ADDRESS3", 'mapping': 'ADDRESS3'},
    11: {'name': "ADDRESS4", 'mapping': 'ADDRESS4'},
    12: {'name': "ADDRESS5", 'mapping': 'ADDRESS5'},
    13: {'name': "LOCAL_ID", 'mapping': 'LOCAL_ID'},
}

EXPECTED_TEST_2_COLUMNS_DUPLICATE_COLUMN = {
    1: {'name': "FORENAMES", 'mapping': 'FORENAMES'},
    2: {'name': "SURNAME", 'mapping': 'SURNAME'},
    3: {'name': "SURNAME", 'mapping': ''},
    4: {'name': "SEX", 'mapping': 'SEX'},
    5: {'name': "POSTCODE", 'mapping': 'POSTCODE'},
    6: {'name': "NHS_NUMBER", 'mapping': 'NHS_NUMBER'},
    7: {'name': "SYSTEM_NUMBER", 'mapping': 'SYSTEM_NUMBER'},
    8: {'name': "ADDRESS1", 'mapping': 'ADDRESS1'},
    9: {'name': "ADDRESS2", 'mapping': 'ADDRESS2'},
    10: {'name': "ADDRESS3", 'mapping': 'ADDRESS3'},
    11: {'name': "ADDRESS4", 'mapping': 'ADDRESS4'},
    12: {'name': "ADDRESS5", 'mapping': 'ADDRESS5'},
    13: {'name': "LOCAL_ID", 'mapping': 'LOCAL_ID'},
}

EXPECTED_TEST_3_COLUMNS_EMPTY_COLUMN_NAME = {
    1: {'name': "FORENAMES", 'mapping': 'FORENAMES'},
    2: {'name': "SURNAME", 'mapping': 'SURNAME'},
    3: {'name': "", 'mapping': ''},
    4: {'name': "SEX", 'mapping': 'SEX'},
    5: {'name': "POSTCODE", 'mapping': 'POSTCODE'},
    6: {'name': "NHS_NUMBER", 'mapping': 'NHS_NUMBER'},
    7: {'name': "SYSTEM_NUMBER", 'mapping': 'SYSTEM_NUMBER'},
    8: {'name': "ADDRESS1", 'mapping': 'ADDRESS1'},
    9: {'name': "ADDRESS2", 'mapping': 'ADDRESS2'},
    10: {'name': "ADDRESS3", 'mapping': 'ADDRESS3'},
    11: {'name': "ADDRESS4", 'mapping': 'ADDRESS4'},
    12: {'name': "ADDRESS5", 'mapping': 'ADDRESS5'},
    13: {'name': "LOCAL_ID", 'mapping': 'LOCAL_ID'},
}

EXPECTED_TEST_4_COLUMNS_INCLUDING_SPACES = {
    1: {'name': "FORE NAMES", 'mapping': 'FORENAMES'},
    2: {'name': "SUR NAME", 'mapping': 'SURNAME'},
    3: {'name': "D O B", 'mapping': "DOB"},
    4: {'name': "S E X", 'mapping': 'SEX'},
    5: {'name': "POST CODE", 'mapping': 'POSTCODE'},
    6: {'name': "NHS NUMBER", 'mapping': 'NHS_NUMBER'},
    7: {'name': "SYSTEM NUMBER", 'mapping': 'SYSTEM_NUMBER'},
    8: {'name': "    A\tDDRESS 1", 'mapping': 'ADDRESS1'},
    9: {'name': "ADDRESS 2", 'mapping': 'ADDRESS2'},
    10: {'name': "ADDRESS 3", 'mapping': 'ADDRESS3'},
    11: {'name': "ADDRESS 4", 'mapping': 'ADDRESS4'},
    12: {'name': "ADDRESS 5", 'mapping': 'ADDRESS5'},
    13: {'name': "LOCAL ID", 'mapping': 'LOCAL_ID'},
}

EXPECTED_TEST_5_COLUMNS_INCLUDING_PUNCTUATION = {
    1: {'name': '"FORENAMES"', 'mapping': 'FORENAMES'},
    2: {'name': "\tSURNAME", 'mapping': 'SURNAME'},
    3: {'name': "D.O.B.", 'mapping': "DOB"},
    4: {'name': "'SEX", 'mapping': 'SEX'},
    5: {'name': "POST-CODE", 'mapping': 'POSTCODE'},
    6: {'name': "NHS=NUMBER", 'mapping': 'NHS_NUMBER'},
    7: {'name': "SYSTEM+NUMBER:", 'mapping': 'SYSTEM_NUMBER'},
    8: {'name': "^ADDRESS~1;", 'mapping': 'ADDRESS1'},
    9: {'name': "#ADDRESS%2,", 'mapping': 'ADDRESS2'},
    10: {'name': "A/DDRESS$3?", 'mapping': 'ADDRESS3'},
    11: {'name': "A£DDR€ESS&4!", 'mapping': 'ADDRESS4'},
    12: {'name': "AD!DRESS*5`¬", 'mapping': 'ADDRESS5'},
    13: {'name': "(<LOC¦AL ID>|)", 'mapping': 'LOCAL_ID'},
}

EXPECTED_TEST_6_COLUMNS_LOWERCASE = {
    1: {'name': "forenames", 'mapping': 'FORENAMES'},
    2: {'name': "surname", 'mapping': 'SURNAME'},
    3: {'name': "dob", 'mapping': 'DOB'},
    4: {'name': "sex", 'mapping': 'SEX'},
    5: {'name': "postcode", 'mapping': 'POSTCODE'},
    6: {'name': "nhs_number", 'mapping': 'NHS_NUMBER'},
    7: {'name': "system_number", 'mapping': 'SYSTEM_NUMBER'},
    8: {'name': "address1", 'mapping': 'ADDRESS1'},
    9: {'name': "address2", 'mapping': 'ADDRESS2'},
    10: {'name': "address3", 'mapping': 'ADDRESS3'},
    11: {'name': "address4", 'mapping': 'ADDRESS4'},
    12: {'name': "address5", 'mapping': 'ADDRESS5'},
    13: {'name': "local_id", 'mapping': 'LOCAL_ID'},
}

EXPECTED_TEST_7_COLUMNS_ALTERNATIVES = {
    1: {'name': "forename", 'mapping': 'FORENAMES'},
    2: {'name': "lastname", 'mapping': 'SURNAME'},
    3: {'name': "date of birth", 'mapping': 'DOB'},
    4: {'name': "gender", 'mapping': 'SEX'},
    5: {'name': "postal code", 'mapping': 'POSTCODE'},
    6: {'name': "snumber", 'mapping': 'SYSTEM_NUMBER'},
}

EXPECTED_TEST_8_COLUMNS_ALTERNATIVES = {
    1: {'name': "first name", 'mapping': 'FORENAMES'},
    2: {'name': "family name", 'mapping': 'SURNAME'},
    3: {'name': "birth date", 'mapping': 'DOB'},
    4: {'name': "uhlsnumber", 'mapping': 'SYSTEM_NUMBER'},
}

EXPECTED_TEST_9_COLUMNS_ALTERNATIVES = {
    1: {'name': "first names", 'mapping': 'FORENAMES'},
    2: {'name': "uhl system number", 'mapping': 'SYSTEM_NUMBER'},
}

EXPECTED_TEST_10_COLUMNS_ALTERNATIVES = {
    1: {'name': "given name", 'mapping': 'FORENAMES'},
}

EXPECTED_TEST_11_COLUMNS_ALTERNATIVES = {
    1: {'name': "given names", 'mapping': 'FORENAMES'},
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

    batch.automap_columns()

    expected = {i: e['mapping'] for i, e in columns.items()}

    assert {c.column_index: c.mapping for c in batch.columns} == expected
