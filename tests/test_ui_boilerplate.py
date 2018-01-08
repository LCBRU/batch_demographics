# -*- coding: utf-8 -*-

import pytest
from bs4 import BeautifulSoup


def test_missing_route(client):
    resp = client.get('/uihfihihf')
    assert resp.status_code == 404


@pytest.mark.parametrize("path", [
    ('/'),
    ('/static/css/main.css'),
    ('/static/css/bootstrap.min.css'),
    ('/static/fonts/glyphicons-halflings-regular.eot'),
    ('/static/fonts/glyphicons-halflings-regular.svg'),
    ('/static/fonts/glyphicons-halflings-regular.ttf'),
    ('/static/fonts/glyphicons-halflings-regular.woff'),
    ('/static/fonts/glyphicons-halflings-regular.woff2'),
    ('/static/img/nihr-logo.png'),
    ('/static/js/bootstrap.min.js'),
    ('/static/js/html5shiv.min.js'),
    ('/static/js/jquery-1.11.2.min.js'),
    ('/static/js/main.js'),
    ('/static/js/modernizr.min.js'),
    ('/static/js/respond.min.js'),
])
def test_url_exists(client, path):
    resp = client.get(path)

    assert resp.status_code == 200


@pytest.mark.parametrize("path", [
    ('/')
])
def test_html_boilerplate(client, path):
    resp = client.get(path)
    rsoup = BeautifulSoup(resp.data, 'html.parser')

    assert rsoup.find('html') is not None
    assert rsoup.find('html')['lang'] == "en"
    assert rsoup.find('head') is not None
    assert rsoup.find(
        lambda tag: tag.name == "meta" and
        tag.has_attr('charset') and
        tag['charset'] == "utf-8"
    ) is not None
    assert rsoup.title is not None
    assert rsoup.find('body') is not None
    assert rsoup.find('title') is not None
