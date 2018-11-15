# -*- coding: utf-8 -*-

import pytest
from flask import url_for
from batch_demographics.model import Batch
from tests.ui.test_ui_security import assert__requires_login_post
from tests.ui_tools import login
from tests.model_tools import create_batches, create_user

def test_ui_delete__path_requires_login(client):
    assert__requires_login_post(client, url_for('ui.delete'))


def test_ui_delete__batch_delete_not_exists(client, faker):
    login(client, faker)

    resp = client.post(url_for('ui.delete'), data=dict(id='1'))

    assert resp.status_code == 404


def test_ui_delete__batch_delete_not_correct_user(client, faker):
    login(client, faker)
    u2 = create_user(faker)

    batch = create_batches(u2, 1, faker)[0]

    resp = client.post(url_for('ui.delete'), data=dict(id=batch.id))

    assert resp.status_code == 403

    batch = Batch.query.filter(
        Batch.id == batch.id
    ).one()

    assert batch.deleted == False


def test_ui_delete__batch_delete_correct(client, faker):
    u = login(client, faker)

    batch = create_batches(u, 1, faker)[0]

    resp = client.post(url_for('ui.delete'), data=dict(id=batch.id))
    
    assert resp.status_code == 302
    assert resp.location == url_for('ui.index', _external=True)
    batch = Batch.query.filter(
        Batch.id == batch.id
    ).one()

    assert batch.deleted == True
