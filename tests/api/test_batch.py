# -*- coding: utf-8 -*-

from datetime import datetime, timezone
import dateutil.parser
import pytest
from batch_demographics.model import Batch
from batch_demographics.database import db


@pytest.mark.parametrize("batches", [
    (0),
    (1),
    (10),
])
def test_batch_list(client, batches):

    for _ in range(batches):
        db.session.add(Batch(name=''))
        db.session.commit()

    resp = client.get('/api/batch/')

    assert resp is not None
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == batches


@pytest.mark.parametrize("name", [
    ('test name'),
    ('*' * 100),
])
def test_add_batch(client, name):
    before_time = datetime.now(timezone.utc)

    resp = client.post_json("/api/batch/", data=dict(name=name))

    after_time = datetime.now(timezone.utc)

    assert resp.status_code == 200
    assert Batch.query.count() == 1

    assert Batch.query.filter(
        Batch.name == name
    ).filter(
        Batch.date_created > before_time
    ).filter(
        Batch.date_created < after_time
    ).count() == 1

    data = resp.get_json()
    assert 'id' in data
    assert 'name' in data
    assert data['name'] == name
    assert dateutil.parser.parse(data['date_created']) > before_time
    assert dateutil.parser.parse(data['date_created']) < after_time


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
