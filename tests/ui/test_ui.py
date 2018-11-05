# -*- coding: utf-8 -*-

import pytest
from bs4 import BeautifulSoup
from datetime import datetime, timezone
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

    resp = client.get('/')
    soup = BeautifulSoup(resp.data, 'html.parser')

    assert soup.find('a', href='/add') is not None
    assert soup.find('table') is not None
    assert soup.find('table')['class'] == ["table"]
    assert len(soup.find('tbody').find_all('tr')) == batches
    assert all(
        tr.select_one('td:nth-of-type(1)').string.strip() in expected_names
        for tr in soup.find('tbody').select('tr')
    )


def test_add_batch_get(client):
    resp = client.get("/add")
    soup = BeautifulSoup(resp.data, 'html.parser')

    assert resp.status_code == 200
    assert soup.find(
        'form',
        {'method': 'POST'}
    ) is not None
    assert soup.find(
        'input',
        {'name': 'name', 'type': 'text'}
    ) is not None
    assert soup.find(
        'a',
        href='/',
        text='Cancel'
    ) is not None
    assert soup.find(
        'button',
        type='submit',
        text='Save'
    ) is not None


@pytest.mark.parametrize("name", [
    ('test name'),
    ('*' * 100),
])
def test_add_batch_post(client, name):
    before_time = datetime.now(timezone.utc)

    resp = client.post("/add", data=dict(name=name))

    after_time = datetime.now(timezone.utc)

    assert resp.status_code == 302
    assert resp.location == 'http://localhost/'
    assert Batch.query.count() == 1
    assert Batch.query.filter(
        Batch.name == name
    ).filter(
        Batch.created_date > before_time
    ).filter(
        Batch.created_date < after_time
    ).count() == 1


@pytest.mark.parametrize("name", [
    (''),
    ('*' * 101),
])
def test_add_batch_post_name_incorrect_length(client, name):
    resp = client.post("/add", data=dict(name=name))

    assert resp.status_code == 200
    assert Batch.query.count() == 0
