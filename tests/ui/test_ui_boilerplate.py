# -*- coding: utf-8 -*-

import pytest
from tests import login as login_user


def assert__html_boilerplate(client, faker, path, login=True):
    if login:
        login_user(client, faker)

    resp = client.get(path)

    assert resp.soup.html is not None
    assert resp.soup.html['lang'] == "en"
    assert resp.soup.head is not None
    assert resp.soup.find(
        lambda tag: tag.name == "meta" and
        tag.has_attr('charset') and
        tag['charset'] == "utf-8"
    ) is not None
    assert resp.soup.title is not None
    assert resp.soup.body is not None


def assert__forms_csrf_token(client_with_crsf, faker, path, login=True):
    if login:
        login_user(client_with_crsf, faker)

    resp = client_with_crsf.get(path)

    print(resp.soup.prettify())

    assert resp.soup.find(
        'input',
        {'name': 'csrf_token'},
        type='hidden',
        id='csrf_token',
    ) is not None
