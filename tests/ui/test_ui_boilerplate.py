# -*- coding: utf-8 -*-

import pytest
from bs4 import BeautifulSoup


def test_missing_route(client):
    resp = client.get('/uihfihihf')
    assert resp.status_code == 404


@pytest.mark.parametrize("path", [
    ('/'),
    ('/favicon.ico'),
    ('/add'),
    ('/static/css/main.css'),
    ('/static/img/nihr-logo-70.png'),
    ('/static/img/cropped-favicon-32x32.png'),
    ('/static/img/cropped-favicon-192x192.png'),
    ('/static/img/cropped-favicon-180x180.png'),
    ('/static/img/cropped-favicon-270x270.png'),
    ('/static/js/main.js'),
])
def test_url_exists(client, path):
    resp = client.get(path)

    assert resp.status_code == 200


@pytest.mark.parametrize("path", [
    ('/'),
    ('/add')
])
def test_html_boilerplate(client, path):
    resp = client.get(path)
    soup = BeautifulSoup(resp.data, 'html.parser')

    assert soup.html is not None
    assert soup.html['lang'] == "en"
    assert soup.head is not None
    assert soup.find(
        lambda tag: tag.name == "meta" and
        tag.has_attr('charset') and
        tag['charset'] == "utf-8"
    ) is not None
    assert soup.title is not None
    assert soup.body is not None


@pytest.mark.parametrize("path", [
    ('/add')
])
def test_forms_csrf_token(client_with_crsf, path):
    resp = client_with_crsf.get(path)
    soup = BeautifulSoup(resp.data, 'html.parser')

    assert soup.find(
        'input',
        {'name': 'csrf_token'},
        type='hidden',
        id='csrf_token',
    ) is not None
