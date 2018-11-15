# -*- coding: utf-8 -*-

import pytest
from flask import url_for
from tests.ui_tools import login
from batch_demographics.model import User
from batch_demographics.database import db
from tests.ui.test_ui_security import assert__requires_login_get, assert__url_exists_without_login
from tests.ui.test_ui_boilerplate import assert__forms_csrf_token, assert__html_boilerplate


@pytest.mark.parametrize("path", [
    ('/'),
    ('/upload'),
])
def test_ui__path_requires_login(client, path):
    assert__requires_login_get(client, path)


@pytest.mark.parametrize("path", [
    ('/login'),
    ('/reset'),
])
def test_ui__forms_csrf_token(client_with_crsf, faker, path):
    assert__forms_csrf_token(client_with_crsf, faker, path, login=False)


@pytest.mark.parametrize("path", [
    ('/login'),
    ('/reset'),
])
def test_ui__html_boilerplate(client, faker, path):
    assert__html_boilerplate(client, faker, path, login=False)


@pytest.mark.parametrize("path", [
    ('/login'),
    ('/reset'),
])
def test_ui__url_exists_without_login(client, path):
    assert__url_exists_without_login(client, path)


@pytest.mark.parametrize(
    ["new_password", "valid"],
    [
        ("@Margaret", True),
        ("Margaret", False),
        ("@argaret", False),
        ("@MARGARET", False),
        ("@Ma", False),
    ],
)
def test__passwords__change(client, faker, new_password, valid):
    user = login(client, faker)

    password = "fred"

    user.password = password
    db.session.add(user)
    db.session.commit()

    resp = client.post(
        url_for("security.change_password"),
        data={
            "password": password,
            "new_password": new_password,
            "new_password_confirm": new_password,
        },
    )

    if valid:
        assert resp.status_code == 302
        assert resp.soup.find("div", "errors") is None
    else:
        assert resp.status_code == 200
        assert len(resp.soup.find("div", "errors").find_all("div")) > 0


def test__passwords__change_wrong_old_password(client, faker):
    user = login(client, faker)

    password = "fred"
    wrong_password = "freddy"
    new_password = "@Margaret"

    user.password = password
    db.session.add(user)
    db.session.commit()

    resp = client.post(
        url_for("security.change_password"),
        data={
            "password": wrong_password,
            "new_password": new_password,
            "new_password_confirm": new_password,
        },
    )

    assert resp.status_code == 200
    assert len(resp.soup.find("div", "errors").find_all("div")) > 0


def test__passwords__change_passwords_do_not_match(client, faker):
    user = login(client, faker)

    password = "fred"
    new_password = "@Margaret"
    wrong_new_password = "@Margare"

    user.password = password
    db.session.add(user)
    db.session.commit()

    resp = client.post(
        url_for("security.change_password"),
        data={
            "password": password,
            "new_password": new_password,
            "new_password_confirm": wrong_new_password,
        },
    )

    assert resp.status_code == 200
    assert len(resp.soup.find("div", "errors").find_all("div")) > 0
