# -*- coding: utf-8 -*-

import pytest
import dateutil.parser

from batch_demographics.model import (
    Batch,
    details_list_schema,
    Details,
)
from batch_demographics.database import db

from tests.utils import assert_objects_equals_dictionaries


@pytest.mark.parametrize("num_of_details", [
    (0),
    (1),
    (10),
])
def test_details_list(client, faker, num_of_details):

    batch = Batch(name='')
    db.session.add(batch)

    expected_details = []

    for _ in range(num_of_details):
        details = Details(**faker.daps_details())
        details.batch = batch

        expected_details.append(details)

        db.session.add(details)

# Create details for another batch to check that it differentiates
    other_batch = Batch(name='')
    db.session.add(other_batch)
    other_details = Details(**faker.daps_details())
    other_details.batch = other_batch
    db.session.add(other_details)

    db.session.commit()

    resp = client.get('/api/batch/{}/details/'.format(batch.id))

    assert resp is not None
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == num_of_details
    assert_objects_equals_dictionaries(objs=expected_details, dics=data)


@pytest.mark.parametrize("num_of_details", [
    (0),
    (1),
    (10),
])
def test_details_add_works(client, faker, num_of_details):

    batch = Batch(name='')
    db.session.add(batch)
    db.session.commit()

    expected_details = []

    for _ in range(num_of_details):
        expected_details.append(faker.daps_details())

    resp = client.post(
        '/api/batch/{}/details/'.format(batch.id),
        json={'details': expected_details}
    )

    assert resp is not None
    assert resp.status_code == 200
    data = resp.get_json()

    actuals = Details.query.all()
    assert_objects_equals_dictionaries(objs=actuals, dics=expected_details)

    assert len(data) == num_of_details
    assert_objects_equals_dictionaries(objs=actuals, dics=data)


@pytest.mark.parametrize("field_name, max_length", [
    ('forename', 100),
    ('surname', 100),
    ('sex', 10),
    ('postcode', 10),
    ('nhs_number', 10),
    ('system_number', 10),
    ('address1', 100),
    ('address2', 100),
    ('address3', 100),
    ('address4', 100),
    ('address5', 100),
    ('local_id', 100),
])
def test_details_add_field_length(client, faker, field_name, max_length):

    # Just over max length
    detail = faker.daps_details()
    detail[field_name] = '*' * (max_length + 1)

    resp = save_single_detail(client, detail)

    assert resp.status_code == 400
    assert Details.query.count() == 0
    data = resp.get_json()
    assert field_name in data['0']
    assert data['0'][field_name] == [
        'Longer than maximum length {}.'.format(max_length)
    ]

    # Exactly max length
    detail = faker.daps_details()
    detail[field_name] = '*' * max_length

    resp = save_single_detail(client, detail)

    assert resp.status_code == 200
    assert Details.query.count() == 1


@pytest.mark.parametrize("date_string,error_message", [
    ('oijeoirjfeoijre', 'Not a valid date.'),
    ('30-Feb-2010', 'Not a valid date.'),
    ('30-30-2010', 'Not a valid date.'),
    ('30-01-1010', 'DOB too far in the past.'),
])
def test_details_add_invalid_date(client, faker, date_string, error_message):

    detail = faker.daps_details()
    detail['dob'] = date_string

    resp = save_single_detail(client, detail)

    assert resp.status_code == 400
    assert Details.query.count() == 0
    data = resp.get_json()

    print(data)

    assert 'dob' in data['0']
    assert data['0']['dob'] == [error_message]


def save_single_detail(client, detail):
    batch = Batch(name='')
    db.session.add(batch)
    db.session.commit()

    details = {'details': [detail]}
    return client.post(
        '/api/batch/{}/details/'.format(batch.id),
        json=details
    )
