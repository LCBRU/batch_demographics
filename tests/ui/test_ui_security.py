# -*- coding: utf-8 -*-

from batch_demographics.model import User, Role
from batch_demographics.database import db


def assert__url_exists_without_login(client, path):
    resp = client.get(path)

    assert resp.status_code == 200


def test_ui_security__admin_role_created(client):
    resp = client.get('/')

    print(resp.requested_time)
    print(resp.received_time)
    assert Role.query.count() == 1
    assert Role.query.filter(
        Role.name == 'admin'
    ).filter(
        Role.created_date > resp.requested_time
    ).filter(
        Role.created_date < resp.received_time
    ).count() == 1


def test_ui_security__admin_users_created(client):
    resp = client.get('/')

    assert User.query.count() == 2
    
    rab = User.query.filter(
        User.email == 'rab63@le.ac.uk'
    ).filter(
        Role.created_date > resp.requested_time
    ).filter(
        Role.created_date < resp.received_time
    ).one()
    assert rab
    assert rab.password
    assert "admin" in rab.roles

    richard = User.query.filter(
        User.email == 'richard.a.bramley@uhl-tr.nhs.uk'
    ).filter(
        Role.created_date > resp.requested_time
    ).filter(
        Role.created_date < resp.received_time
    ).one()
    assert richard
    assert richard.password
    assert "admin" in richard.roles


def assert__requires_login_get(client, path):
    resp = client.get(path)
    assert resp.status_code == 302
