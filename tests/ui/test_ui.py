# -*- coding: utf-8 -*-

import pytest
from tests.ui.test_ui_security import assert__url_exists_without_login

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
