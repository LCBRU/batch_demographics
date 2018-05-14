# -*- coding: utf-8 -*-

import pytest
import dateutil.parser

from batch_demographics.model import (
    Batch,
    details_list_schema,
    Details,
)
from batch_demographics.database import db


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

    actuals = details_list_schema.load(data, session=db.session)

    assert sorted(actuals.data) == sorted(expected_details)
    assert len(actuals.errors) == 0


@pytest.mark.parametrize("num_of_details", [
    (0),
    (1),
    (10),
])
def test_details_add(client, faker, num_of_details):

    batch = Batch(name='')
    db.session.add(batch)
    db.session.commit()

    expected_details = []

    for _ in range(num_of_details):
        expected_details.append(faker.daps_details())

    resp = client.post_json(
        '/api/batch/{}/details/'.format(batch.id),
        data=expected_details
    )

    for expected in expected_details:
        actual = Details.query.filter(
            Details.nhs_number == expected['nhs_number']
        ).one()

        assert actual.forename == expected['forename']
        assert actual.surname == expected['surname']
        assert actual.dob == expected['dob']
        assert actual.sex == expected['sex']
        assert actual.postcode == expected['postcode']
        assert actual.nhs_number == expected['nhs_number']
        assert actual.system_number == expected['system_number']
        assert actual.address1 == expected['address1']
        assert actual.address2 == expected['address2']
        assert actual.address3 == expected['address3']
        assert actual.address4 == expected['address4']
        assert actual.address5 == expected['address5']
        assert actual.local_id == expected['local_id']
        assert actual.batch_id == batch.id
        expected['id'] = actual.id

    assert resp is not None
    assert resp.status_code == 200
    data = resp.get_json()

    assert len(data) == num_of_details

    for expected, actual in zip(expected_details, data):
        assert actual['id'] == expected['id']
        assert actual['forename'] == expected['forename']
        assert actual['surname'] == expected['surname']
        assert dateutil.parser.parse(actual['dob']).date() == expected['dob']
        assert actual['sex'] == expected['sex']
        assert actual['postcode'] == expected['postcode']
        assert actual['nhs_number'] == expected['nhs_number']
        assert actual['system_number'] == expected['system_number']
        assert actual['address1'] == expected['address1']
        assert actual['address2'] == expected['address2']
        assert actual['address3'] == expected['address3']
        assert actual['address4'] == expected['address4']
        assert actual['address5'] == expected['address5']
        assert actual['local_id'] == expected['local_id']
        assert actual['batch'] == batch.id


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


@pytest.mark.parametrize("date_string", [
    ('oijeoirjfeoijre'),
    ('30-Feb-2010'),
    ('30-30-2010'),
    ('30-01-1010'),
])
def test_details_add_invalid_date(client, faker, date_string):

    detail = faker.daps_details()
    detail['dob'] = date_string

    resp = save_single_detail(client, detail)

    assert resp.status_code == 400
    assert Details.query.count() == 0
    data = resp.get_json()
    assert 'dob' in data['0']
    assert data['0']['dob'] == ['Not a valid date.']


def save_single_detail(client, detail):
    batch = Batch(name='')
    db.session.add(batch)
    db.session.commit()

    details = []

    details.append(detail)

    return client.post_json(
        '/api/batch/{}/details/'.format(batch.id),
        data=details
    )
