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

EXPECTED_TEST_1_COLUMNS = {
    0: {'name': "FORENAMES", 'output_name': 'FORENAMES'},
    1: {'name': "SURNAME", 'output_name': 'SURNAME'},
    2: {'name': "DOB", 'output_name': 'DOB'},
    3: {'name': "SEX", 'output_name': 'SEX'},
    4: {'name': "POSTCODE", 'output_name': 'POSTCODE'},
    5: {'name': "NHS_NUMBER", 'output_name': 'NHS_NUMBER'},
    6: {'name': "SYSTEM_NUMBER", 'output_name': 'SYSTEM_NUMBER'},
    7: {'name': "ADDRESS1", 'output_name': 'ADDRESS1'},
    8: {'name': "ADDRESS2", 'output_name': 'ADDRESS2'},
    9: {'name': "ADDRESS3", 'output_name': 'ADDRESS3'},
    10: {'name': "ADDRESS4", 'output_name': 'ADDRESS4'},
    11: {'name': "ADDRESS5", 'output_name': 'ADDRESS5'},
    12: {'name': "LOCAL_ID", 'output_name': 'LOCAL_ID'},
}

EXPECTED_TEST_2_COLUMNS = {
    0: {'name': "FORENAMES", 'output_name': 'FORENAMES'},
    1: {'name': "SURNAME", 'output_name': 'SURNAME'},
    2: {'name': "SURNAME", 'output_name': None},
    3: {'name': "SEX", 'output_name': 'SEX'},
    4: {'name': "POSTCODE", 'output_name': 'POSTCODE'},
    5: {'name': "NHS_NUMBER", 'output_name': 'NHS_NUMBER'},
    6: {'name': "SYSTEM_NUMBER", 'output_name': 'SYSTEM_NUMBER'},
    7: {'name': "ADDRESS1", 'output_name': 'ADDRESS1'},
    8: {'name': "ADDRESS2", 'output_name': 'ADDRESS2'},
    9: {'name': "ADDRESS3", 'output_name': 'ADDRESS3'},
    10: {'name': "ADDRESS4", 'output_name': 'ADDRESS4'},
    11: {'name': "ADDRESS5", 'output_name': 'ADDRESS5'},
    12: {'name': "LOCAL_ID", 'output_name': 'LOCAL_ID'},
}

EXPECTED_TEST_3_COLUMNS = {
    0: {'name': "FORENAMES", 'output_name': 'FORENAMES'},
    1: {'name': "SURNAME", 'output_name': 'SURNAME'},
    2: {'name': "", 'output_name': None},
    3: {'name': "SEX", 'output_name': 'SEX'},
    4: {'name': "POSTCODE", 'output_name': 'POSTCODE'},
    5: {'name': "NHS_NUMBER", 'output_name': 'NHS_NUMBER'},
    6: {'name': "SYSTEM_NUMBER", 'output_name': 'SYSTEM_NUMBER'},
    7: {'name': "ADDRESS1", 'output_name': 'ADDRESS1'},
    8: {'name': "ADDRESS2", 'output_name': 'ADDRESS2'},
    9: {'name': "ADDRESS3", 'output_name': 'ADDRESS3'},
    10: {'name': "ADDRESS4", 'output_name': 'ADDRESS4'},
    11: {'name': "ADDRESS5", 'output_name': 'ADDRESS5'},
    12: {'name': "LOCAL_ID", 'output_name': 'LOCAL_ID'},
}

EXPECTED_TEST_4_COLUMNS = {
    0: {'name': "FORE NAMES", 'output_name': 'FORENAMES'},
    1: {'name': "SUR NAME", 'output_name': 'SURNAME'},
    2: {'name': "D O B", 'output_name': "DOB"},
    3: {'name': "S E X", 'output_name': 'SEX'},
    4: {'name': "POST CODE", 'output_name': 'POSTCODE'},
    5: {'name': "NHS NUMBER", 'output_name': 'NHS_NUMBER'},
    6: {'name': "SYSTEM NUMBER", 'output_name': 'SYSTEM_NUMBER'},
    7: {'name': "ADDRESS 1", 'output_name': 'ADDRESS1'},
    8: {'name': "ADDRESS 2", 'output_name': 'ADDRESS2'},
    9: {'name': "ADDRESS 3", 'output_name': 'ADDRESS3'},
    10: {'name': "ADDRESS 4", 'output_name': 'ADDRESS4'},
    11: {'name': "ADDRESS 5", 'output_name': 'ADDRESS5'},
    12: {'name': "LOCAL ID", 'output_name': 'LOCAL_ID'},
}


@pytest.mark.parametrize("filename, expected", [
    ('test_1.csv', EXPECTED_TEST_1_COLUMNS),
    ('test_1.tsv', EXPECTED_TEST_1_COLUMNS),
    ('test_1.psv', EXPECTED_TEST_1_COLUMNS),
    ('test_2.csv', EXPECTED_TEST_2_COLUMNS),
    ('test_3.csv', EXPECTED_TEST_3_COLUMNS),
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
    (EXPECTED_TEST_1_COLUMNS),
    (EXPECTED_TEST_2_COLUMNS),
    (EXPECTED_TEST_3_COLUMNS),
    (EXPECTED_TEST_4_COLUMNS),
])
def test_services_upload__auto_match__correct(client, faker, upload_files, columns):
    u = create_user(faker)

    batch = create_batches(u, 1, faker)[0]

    for index, c in columns.items():
        batch.columns.append(
            Column(column_index=index, name=c['name'], batch_id=batch.id)
        )

    update_batch(batch)

    automap_batch_columns(batch)

    expected = {i: e['output_name'] for i, e in columns.items() if e['output_name']}

    assert len(batch.mappings) == len(expected)
    assert {m.column.column_index: m.output_name for m in batch.mappings} == expected
