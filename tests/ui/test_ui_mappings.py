# -*- coding: utf-8 -*-

import pytest
from flask import url_for
from batch_demographics.model import Column
from tests.ui.test_ui_security import assert__requires_login_get, assert__requires_login_post
from tests.ui.test_ui_boilerplate import assert__forms_csrf_token, assert__html_boilerplate, assert__html_menu
from tests.ui_tools import assert_field_in_error_display, login
from tests.model_tools import create_batches, create_user, create_columns


def test_ui_mappings__batch_get(client, faker):
    COLUMNS = {'FORENAMES': 'FORENAMES', 'STRANGE': '', 'POSTCODE': 'POSTCODE'}
    u = login(client, faker)
    batch = create_batch_with_columns(faker, u)
    create_columns(batch, COLUMNS.keys())

    resp = client.get(url_for('ui.edit_mappings', batch_id=batch.id))

    assert resp.status_code == 200
    assert resp.soup.find(
        'form',
        {'method': 'POST'}
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

    for c, m in COLUMNS.items():
        col_name = resp.soup.find(
            'input',
            type='hidden',
            id=lambda x: x and x.endswith('column_name'),
            value=lambda x: x and x.endswith(c),
        )
        assert col_name

        prefix = col_name['id'][:len(col_name['id']) - len('column_name')]

        col_id = resp.soup.find(
            'input',
            type='hidden',
            id=lambda x: x and x == '{}column_id'.format(prefix),
        )
        assert col_id

        mapping = resp.soup.find(
            'select',
            id=lambda x: x and x == '{}mapping'.format(prefix),
        )
        assert mapping

        assert len(mapping.find_all('option')) == 14

        selected = mapping.find(
            'option',
            selected=True,
            value=m
        )
        assert selected


@pytest.mark.parametrize("columns", [
    ({'FORENAMES': 'FORENAMES'}),
    ({'FORENAMES': 'POSTCODE'}),
    ({'FORENAMES': ''}),
    ({'FORENAMES': 'POSTCODE', 'POSTCODE': 'SURNAME'}),
    ({'FORENAMES': '', 'POSTCODE': ''}),
])
def test_ui_mappings__batch_post_ok(client, faker, columns):
    u = login(client, faker)
    batch = create_batch_with_columns(faker, u)
    create_columns(batch, columns.keys())

    data = {}

    for i, c in enumerate(batch.columns):
        data['column_mappings-{}-column_id'.format(i)] = c.id
        data['column_mappings-{}-column_name'.format(i)] = c.name
        data['column_mappings-{}-mapping'.format(i)] = columns[c.name]

    resp = client.post(url_for('ui.edit_mappings', batch_id=batch.id), data=data)

    assert resp.status_code == 302

    assert Column.query.filter(Column.batch_id == batch.id).count() == len(columns)

    for name, mapping in columns.items():
        assert Column.query.filter(
            Column.batch_id == batch.id
        ).filter(
            Column.name == name            
        ).filter(
            Column.mapping == mapping
        ).count() == 1


@pytest.mark.parametrize("columns", [
    ({'FORENAMES': 'POSTCODE', 'SURNAME': 'POSTCODE'}),
])
def test_ui_mappings__batch_post_duplicate(client, faker, columns):
    u = login(client, faker)
    batch = create_batch_with_columns(faker, u)
    create_columns(batch, columns.keys())

    data = {}

    for i, c in enumerate(batch.columns):
        data['column_mappings-{}-column_id'.format(i)] = c.id
        data['column_mappings-{}-column_name'.format(i)] = c.name
        data['column_mappings-{}-mapping'.format(i)] = columns[c.name]

    resp = client.post(url_for('ui.edit_mappings', batch_id=batch.id), data=data)

    assert resp.status_code == 200

    assert_field_in_error_display(resp, 'POSTCODE')

    for name in columns.keys():
        assert_field_in_error_display(resp, name)

    assert Column.query.filter(Column.batch_id == batch.id).count() == len(columns)

    for name in columns.keys():
        assert Column.query.filter(
            Column.batch_id == batch.id
        ).filter(
            Column.name == name            
        ).filter(
            Column.mapping == name
        ).count() == 1


def test_ui_mappings__must_be_batch_user_get(client, faker):
    login(client, faker)
    u2 = create_user(faker)
    batch = create_batch_with_columns(faker, u2)

    resp = client.get(url_for('ui.edit_mappings', batch_id=batch.id))
    assert resp.status_code == 403


def test_ui_mappings__must_be_batch_user_post(client, faker):
    login(client, faker)
    u2 = create_user(faker)
    batch = create_batch_with_columns(faker, u2)

    resp = client.get(url_for('ui.edit_mappings', batch_id=batch.id))
    assert resp.status_code == 403


def test_ui_mappings__path_requires_login_get(client, faker):
    u = create_user(faker)
    batch = create_batch_with_columns(faker, u)
    assert__requires_login_get(client, url_for('ui.edit_mappings', batch_id=batch.id))


def test_ui_mappings__path_requires_login_post(client, faker):
    u = create_user(faker)
    batch = create_batch_with_columns(faker, u)
    assert__requires_login_post(client, url_for('ui.edit_mappings', batch_id=batch.id))


def test_ui_mappings__forms_csrf_token(client_with_crsf, faker):
    u = login(client_with_crsf, faker)
    batch = create_batch_with_columns(faker, u)
    assert__forms_csrf_token(client_with_crsf, faker, url_for('ui.edit_mappings', batch_id=batch.id), login=False)


def test_ui_mappings__html_boilerplate(client, faker):
    u = login(client, faker)
    batch = create_batch_with_columns(faker, u)
    assert__html_boilerplate(client, faker, url_for('ui.edit_mappings', batch_id=batch.id), login=False)


def test_ui_mappings__html_menu(client, faker):
    u = login(client, faker)
    batch = create_batch_with_columns(faker, u)
    assert__html_menu(client, faker, url_for('ui.edit_mappings', batch_id=batch.id), user=u)


def create_batch_with_columns(faker, user):
    batch = create_batches(user, 1, faker)[0]
    batch.automap_columns()
    return batch
