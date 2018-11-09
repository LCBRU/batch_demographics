# -*- coding: utf-8 -*-

import pytest
from batch_demographics.model import Batch
from batch_demographics.database import db
from tests.ui.test_ui_security import assert__requires_login_get, assert__url_exists_without_login
from tests.ui.test_ui_boilerplate import assert__forms_csrf_token, assert__html_boilerplate
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

    assert resp.soup.find('a', href='/add') is not None
    assert resp.soup.find('table') is not None
    assert resp.soup.find('table')['class'] == ["table"]
    assert len(resp.soup.find('tbody').find_all('tr')) == batches
    assert all(
        tr.select_one('td:nth-of-type(1)').string.strip() in expected_names
        for tr in resp.soup.find('tbody').select('tr')
    )


def test_add_batch_get(client, faker):
    login(client, faker)

    resp = client.get("/add")

    assert resp.status_code == 200
    assert resp.soup.find(
        'form',
        {'method': 'POST'}
    ) is not None
    assert resp.soup.find(
        'input',
        {'name': 'name', 'type': 'text'}
    ) is not None
    assert resp.soup.find(
        'a',
        href='/',
        text='Cancel'
    ) is not None
    assert resp.soup.find(
        'button',
        type='submit',
        text='Save'
    ) is not None


@pytest.mark.parametrize("name", [
    ('test name'),
    ('*' * 100),
])
def test_add_batch_post(client, faker, name):
    login(client, faker)

    resp = client.post("/add", data=dict(name=name))

    assert resp.status_code == 302
    assert resp.location == 'http://localhost/'
    assert Batch.query.count() == 1
    assert Batch.query.filter(
        Batch.name == name
    ).filter(
        Batch.created_date > resp.requested_time
    ).filter(
        Batch.created_date < resp.received_time
    ).count() == 1


@pytest.mark.parametrize("name", [
    (''),
    ('*' * 101),
])
def test_add_batch_post_name_incorrect_length(client, faker, name):
    login(client, faker)

    resp = client.post("/add", data=dict(name=name))

    assert resp.status_code == 200
    assert Batch.query.count() == 0


@pytest.mark.parametrize("path", [
    ('/'),
    ('/add'),
])
def test_ui__path_requires_login(client, path):
    assert__requires_login_get(client, path)


@pytest.mark.parametrize("path", [
    ('/add')
])
def test_ui__forms_csrf_token(client_with_crsf, faker, path):
    assert__forms_csrf_token(client_with_crsf, faker, path)


@pytest.mark.parametrize("path", [
    ('/'),
    ('/add')
])
def test_ui__html_boilerplate(client, faker, path):
    assert__html_boilerplate(client, faker, path)


def test_ui__missing_route(client):
    resp = client.get('/uihfihihf')
    assert resp.status_code == 404


@pytest.mark.parametrize("path", [
    ('/favicon.ico'),
    ('/static/css/main.css'),
    ('/static/img/nihr-logo-70.png'),
    ('/static/img/cropped-favicon-32x32.png'),
    ('/static/img/cropped-favicon-192x192.png'),
    ('/static/img/cropped-favicon-180x180.png'),
    ('/static/img/cropped-favicon-270x270.png'),
    ('/static/js/main.js'),
])
def test_ui__url_exists_without_login(client, path):
    assert__url_exists_without_login(client, path)
