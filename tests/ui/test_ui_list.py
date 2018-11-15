# -*- coding: utf-8 -*-

import pytest
import urllib
from flask import current_app, url_for
from tests.ui.test_ui_security import assert__requires_login_get, assert__url_exists_without_login
from tests.ui.test_ui_boilerplate import assert__html_boilerplate, assert__html_menu, assert__paginator, assert__search
from tests.ui_tools import login
from tests.model_tools import create_batches, update_batch, create_user


@pytest.mark.parametrize("my_batches, other_user_batches", [
    (0, 0),
    (0, 10),
    (1, 1),
    (10, 10),
    (100, 100),
])
def test_ui_list__user_batch_list(client, faker, my_batches, other_user_batches):
    u = login(client, faker)
    u2 = create_user(faker)

    expected_data = create_batches(u, my_batches, faker)
    create_batches(u2, other_user_batches, faker)

    resp = client.get('/')

    page_size = current_app.config["PAGE_SIZE"]
    items_on_page = min(page_size, my_batches)

    _assert__boilerplate_html(resp, items_on_page, expected_data)

    pages = my_batches // page_size

    if pages > 1:
        assert__paginator(
            resp=resp,
            prev_page=None,
            next_page=2,
            active_page=1,
        )


@pytest.mark.parametrize("pages", [
    (2),
    (100),
])
def test_ui_list__user_batch_list_last_page(client, faker, pages):
    page_size = current_app.config["PAGE_SIZE"]

    u = login(client, faker)
    u2 = create_user(faker)

    batches = pages * page_size

    expected_data = create_batches(u, batches, faker)
    create_batches(u2, batches, faker)

    resp = client.get('/?page={}'.format(pages))

    _assert__boilerplate_html(resp, page_size, expected_data)

    assert__paginator(
        resp=resp,
        prev_page=pages - 1,
        next_page=None,
        active_page=pages,
    )


@pytest.mark.parametrize("pages", [
    (10),
    (20),
])
def test_ui_list__user_batch_list_middle_page(client, faker, pages):
    page_size = current_app.config["PAGE_SIZE"]

    u = login(client, faker)
    u2 = create_user(faker)

    batches = pages * page_size

    expected_data = create_batches(u, batches, faker)
    create_batches(u2, batches, faker)

    page = pages // 2

    resp = client.get('/?page={}'.format(page))

    _assert__boilerplate_html(resp, page_size, expected_data)

    assert__paginator(
        resp=resp,
        prev_page=page - 1,
        next_page=page + 1,
        active_page=page,
    )


def test_ui_list__user_batch_list_beyond_last_page(client, faker):
    page_size = current_app.config["PAGE_SIZE"]

    u = login(client, faker)
    u2 = create_user(faker)

    batches = page_size
    page = 2

    create_batches(u, batches, faker)
    create_batches(u2, batches, faker)

    resp = client.get('/?page={}'.format(page))

    assert resp.status_code == 200


def test_ui_list__deleted_batch_missing(client, faker):
    u = login(client, faker)

    batches = create_batches(u, 1, faker)
    batches[0].deleted = True
    update_batch(batches[0])

    resp = client.get('/')

    _assert__boilerplate_html(resp, 0, batches)


def test_ui_list__user_batch_list_search_found(client, faker):
    page_size = current_app.config["PAGE_SIZE"]
    batches = page_size

    u = login(client, faker)
    u2 = create_user(faker)

    expected_data = create_batches(u, batches, faker)
    create_batches(u2, batches, faker)

    expected_data[0].name = "Known Elephant"
    update_batch(expected_data[0])

    resp = client.get('/?search={}'.format("Elephant"))

    _assert__boilerplate_html(resp, 1, expected_data[0:1])


def _assert__boilerplate_html(resp, items_on_page, batches):
    assert resp.soup.find('a', href='/upload') is not None
    assert resp.soup.find('table') is not None
    assert "table" in resp.soup.find('table')['class']

    assert len(resp.soup.find('tbody').find_all('tr')) == items_on_page
    for tr in resp.soup.find('tbody').select('tr'):
        assert tr.select_one('td:nth-of-type(1)').string.strip() in [b.name for b in batches]
        assert tr.select_one('td:nth-of-type(2)').string.strip() in [b.created_date.strftime("%-d %b %Y") for b in batches]
        assert resp.soup.find(lambda tag: tag.name=="a" and 'Delete' in tag.text)


@pytest.mark.parametrize("path", [
    ('/'),
])
def test_ui_list__path_requires_login(client, path):
    assert__requires_login_get(client, path)


@pytest.mark.parametrize("path", [
    ('/'),
])
def test_ui_list__html_boilerplate(client, faker, path):
    assert__html_boilerplate(client, faker, path)


@pytest.mark.parametrize("path", [
    ('/'),
])
def test_ui_list__html_menu(client, faker, path):
    assert__html_menu(client, faker, path)

@pytest.mark.parametrize("path", [
    ('/'),
])
def test_ui_list__search(client, faker, path):
    assert__search(client, faker, path)

