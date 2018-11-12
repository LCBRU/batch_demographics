# -*- coding: utf-8 -*-

import pytest
from batch_demographics.model import Batch
from batch_demographics.database import db
from tests.ui.test_ui_security import assert__requires_login_get
from tests.ui.test_ui_boilerplate import assert__forms_csrf_token, assert__html_boilerplate, assert__html_menu
from tests import login
from tests.ui_tools import assert_field_in_error_display

def test_ui_upload__batch_get(client, faker):
    login(client, faker)

    resp = client.get("/upload")

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
        'input',
        {'name': 'participant_file', 'type': 'file'}
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
def test_ui_upload__batch_post(client, faker, name):
    login(client, faker)

    file_details = faker.participant_file_details()

    data = dict(name=name, participant_file=file_details)

    resp = client.post("/upload", data=data)

    assert resp.status_code == 302
    assert resp.location == 'http://localhost/'
    assert Batch.query.count() == 1
    assert Batch.query.filter(
        Batch.name == name
    ).filter(
        Batch.filename == file_details[1]
    ).filter(
        Batch.created_date > resp.requested_time
    ).filter(
        Batch.created_date < resp.received_time
    ).count() == 1


@pytest.mark.parametrize("name", [
    (''),
    ('*' * 101),
])
def test_ui_upload__batch_post_name_incorrect_length(client, faker, name):
    login(client, faker)

    data = dict(name=name, participant_file=faker.participant_file_details())

    resp = client.post("/upload", data=data)

    assert resp.status_code == 200
    assert Batch.query.count() == 0

    assert_field_in_error_display(resp, 'Name')


def test_ui_upload__batch_post_file_missing(client, faker):
    login(client, faker)

    data = dict(name='frederick')

    resp = client.post("/upload", data=data)

    assert resp.status_code == 200
    assert Batch.query.count() == 0

    assert_field_in_error_display(resp, 'Participants File')


@pytest.mark.parametrize("path", [
    ('/upload'),
])
def test_ui__path_requires_login(client, path):
    assert__requires_login_get(client, path)


@pytest.mark.parametrize("path", [
    ('/upload')
])
def test_ui__forms_csrf_token(client_with_crsf, faker, path):
    assert__forms_csrf_token(client_with_crsf, faker, path)


@pytest.mark.parametrize("path", [
    ('/upload')
])
def test_ui__html_boilerplate(client, faker, path):
    assert__html_boilerplate(client, faker, path)


@pytest.mark.parametrize("path", [
    ('/upload')
])
def test_ui__html_menu(client, faker, path):
    assert__html_menu(client, faker, path)
