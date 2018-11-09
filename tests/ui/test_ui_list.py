# -*- coding: utf-8 -*-

import pytest
from batch_demographics.model import Batch
from batch_demographics.database import db
from tests.ui.test_ui_security import assert__requires_login_get, assert__url_exists_without_login
from tests.ui.test_ui_boilerplate import assert__html_boilerplate, assert__html_menu
from tests import login

@pytest.mark.parametrize("batches", [
    (0),
    (1),
    (10),
    (100),
])
def test_batch_list(client, faker, batches):
    login(client, faker)

    expected_names = []

    for i in range(batches):
        name = "batch_{}".format(i)
        expected_names.append(name)
        db.session.add(Batch(name=name))
        db.session.commit()

    resp = client.get('/')

    assert resp.soup.find('a', href='/upload') is not None
    assert resp.soup.find('table') is not None
    assert resp.soup.find('table')['class'] == ["table"]
    assert len(resp.soup.find('tbody').find_all('tr')) == batches
    assert all(
        tr.select_one('td:nth-of-type(1)').string.strip() in expected_names
        for tr in resp.soup.find('tbody').select('tr')
    )


@pytest.mark.parametrize("path", [
    ('/'),
])
def test_ui__path_requires_login(client, path):
    assert__requires_login_get(client, path)


@pytest.mark.parametrize("path", [
    ('/'),
])
def test_ui__html_boilerplate(client, faker, path):
    assert__html_boilerplate(client, faker, path)


@pytest.mark.parametrize("path", [
    ('/'),
])
def test_ui__html_menu(client, faker, path):
    assert__html_menu(client, faker, path)
