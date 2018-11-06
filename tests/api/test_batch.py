# -*- coding: utf-8 -*-

import dateutil.parser
import pytest
from batch_demographics.model import Batch
from batch_demographics.database import db


@pytest.mark.parametrize("batches", [
    (0),
    (1),
    (10),
    (100),
])
def test_batch_list(client, batches):

    expected_names = []

    for i in range(batches):
        name = "batch_{}".format(i)
        expected_names.append(name)
        db.session.add(Batch(name=name))
        db.session.commit()

    resp = client.get('/api/batch/')

    assert resp is not None
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == batches
    assert all(b['name'] in expected_names for b in data)


@pytest.mark.parametrize("name", [
    ('test name'),
    ('*' * 100),
])
def test_add_batch(client, name):
    resp = client.post_json("/api/batch/", data=dict(name=name))

    assert resp.status_code == 200
    assert Batch.query.count() == 1

    assert Batch.query.filter(
        Batch.name == name
    ).filter(
        Batch.created_date > resp.requested_time
    ).filter(
        Batch.created_date < resp.received_time
    ).count() == 1

    data = resp.get_json()
    assert 'id' in data
    assert 'name' in data
    assert data['name'] == name
    assert dateutil.parser.parse(data['created_date']) > resp.requested_time
    assert dateutil.parser.parse(data['created_date']) < resp.received_time


@pytest.mark.parametrize("name", [
    (''),
    ('*' * 101),
])
def test_add_batch_name_incorrect_length(client, name):
    resp = client.post_json("/api/batch/", data=dict(name=name))

    assert resp.status_code == 400
    assert Batch.query.count() == 0
    data = resp.get_json()
    assert 'name' in data
    assert data['name'] == ['Length must be between 1 and 100.']
