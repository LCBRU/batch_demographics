# -*- coding: utf-8 -*-

import pytest
from batch_demographics.model import Batch
from batch_demographics.database import db
from tests.ui.test_ui_security import assert__requires_login_get, assert__url_exists_without_login
from tests.ui.test_ui_boilerplate import assert__html_boilerplate, assert__html_menu
from tests import login, create_user

@pytest.mark.parametrize("my_batches, other_user_batches", [
    (0, 0),
    (0, 10),
    (1, 1),
    (10, 10),
    (100, 100),
])
def test_batch_list(client, faker, my_batches, other_user_batches):
    u = login(client, faker)
    u2 = create_user(faker)

    expected_data = []

    for _ in range(my_batches):
        b = faker.batch_details()
        b.user = u
        expected_data.append(b)
        db.session.add(b)
        db.session.commit()

    for _ in range(other_user_batches):
        b = faker.batch_details()
        b.user = u2
        db.session.add(b)
        db.session.commit()

    resp = client.get('/')

    assert resp.soup.find('a', href='/upload') is not None
    assert resp.soup.find('table') is not None
    assert resp.soup.find('table')['class'] == ["table"]
    assert len(resp.soup.find('tbody').find_all('tr')) == my_batches
    assert all(
        tr.select_one('td:nth-of-type(1)').string.strip() in [b.name for b in expected_data]
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
