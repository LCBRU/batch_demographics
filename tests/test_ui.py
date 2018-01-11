# -*- coding: utf-8 -*-

import pytest
from bs4 import BeautifulSoup
from batch_demographics.model import Batch
from batch_demographics.database import db


@pytest.mark.parametrize("batches", [
    (0),
    (1),
    (10),
])
def test_batch_list_empty(client, batches):

    for _ in range(batches):
        db.session.add(Batch())
        db.session.commit()

    resp = client.get('/')
    rsoup = BeautifulSoup(resp.data, 'html.parser')

    assert rsoup.find('a', href='/add') is not None
    assert rsoup.find('table') is not None
    assert rsoup.find('table')['class'] == ["table"]
    assert len(rsoup.find('tbody').find_all('tr')) == batches


def test_add_batch(client):
    resp = client.get("/add", data={})

    assert resp.status_code == 302
    assert resp.location == 'http://localhost/'
    assert Batch.query.count() == 1
