# -*- coding: utf-8 -*-

import pytest
from io import BytesIO
from flask import url_for
from batch_demographics.model import Batch
from tests.ui.test_ui_security import assert__requires_login_get, assert__requires_login_post
from tests.ui.test_ui_boilerplate import assert__forms_csrf_token, assert__html_boilerplate, assert__html_menu
from tests.ui_tools import assert_field_in_error_display, login


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
def test_ui_upload__batch_post(client, faker, upload_files, name):

    HEADERS = "FORENAMES,SURNAME,DOB,SEX,POSTCODE,NHS_NUMBER,SYSTEM_NUMBER,ADDRESS1,ADDRESS2,ADDRESS3,ADDRESS4,ADDRESS5,LOCAL_ID"
    filename = "text.csv"

    u = login(client, faker)

    data = dict(name=name, participant_file=(
        BytesIO(HEADERS.encode('utf-8')),
        filename,
    ))

    resp = client.post("/upload", data=data)

    assert resp.status_code == 302
    assert resp.location == 'http://localhost/'
    assert Batch.query.count() == 1
    batch = Batch.query.filter(
        Batch.name == name
    ).filter(
        Batch.user == u
    ).filter(
        Batch.filename == filename
    ).filter(
        Batch.created_date > resp.requested_time
    ).filter(
        Batch.created_date < resp.received_time
    ).one()

    assert batch

    upload_files.assert_file_created(batch, HEADERS)
    assert {c.column_index: c.name for c in batch.columns} == {i: c for i, c in enumerate(HEADERS.split(','))}
    assert {c.column_index: c.mapping for c in batch.columns} == {i: c for i, c in enumerate(HEADERS.split(','))}


@pytest.mark.parametrize("name", [
    (''),
    ('*' * 101),
])
def test_ui_upload__batch_post_name_incorrect_length(client, faker, name):
    login(client, faker)

    data = dict(name=name, participant_file=faker.participant_file_details()['attachment'])

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


def test_ui__path_requires_login_get(client):
    assert__requires_login_get(client, url_for('ui.upload'))

def test_ui__path_requires_login_post(client):
    assert__requires_login_post(client, url_for('ui.upload'))

def test_ui__forms_csrf_token(client_with_crsf, faker):
    assert__forms_csrf_token(client_with_crsf, faker, url_for('ui.upload'))

def test_ui__html_boilerplate(client, faker):
    assert__html_boilerplate(client, faker, url_for('ui.upload'))

def test_ui__html_menu(client, faker):
    assert__html_menu(client, faker, url_for('ui.upload'))
