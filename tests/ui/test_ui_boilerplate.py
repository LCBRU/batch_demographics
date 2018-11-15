# -*- coding: utf-8 -*-

import re
from flask import url_for
from tests.ui_tools import login as login_user
import urllib
    

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


def assert__html_menu(client, faker, path):
    u = login_user(client, faker)

    resp = client.get(path)

    assert resp.soup.find("a", href=url_for("ui.index")) is not None
    assert resp.soup.find("a", string=" Upload Participant Details", href=url_for("ui.upload")) is not None
    assert resp.soup.find(lambda tag:tag.name=="a" and u.full_name in tag.text) is not None
    assert resp.soup.find("a", string="Change Password", href=url_for("security.change_password")) is not None
    assert resp.soup.find("a", string="Log Out", href=url_for("security.logout")) is not None


def assert__forms_csrf_token(client_with_crsf, faker, path, login=True):
    if login:
        login_user(client_with_crsf, faker)

    resp = client_with_crsf.get(path)

    assert resp.soup.find(
        'input',
        {'name': 'csrf_token'},
        type='hidden',
        id='csrf_token',
    ) is not None


def assert__search(client_with_crsf, faker, path, login=True):
    if login:
        login_user(client_with_crsf, faker)

    resp = client_with_crsf.get(path)

    assert resp.soup.find(
        'input',
        {'name': 'search'},
        type='text',
        id='search',
    ) is not None

    assert resp.soup.find(
        'button',
        type='submit',
        text='Search',
    ) is not None

    assert resp.soup.find(
        'a',
        href=path,
        text='Clear Search',
    ) is not None


def assert__paginator(resp, prev_page, next_page, active_page):

    assert__page_link(resp, page=prev_page, rel='prev', text='Previous')
    assert__page_link(resp, page=next_page, rel='next', text='Next')
    assert__page_link(resp, page=active_page, rel='', text=str(active_page), active=True)


def assert__page_link(resp, page, rel, text, active=False):

    link = resp.soup.find(
        'a',
        string=text,
    )

    assert link

    if active:
        assert 'active' in link.parent['class']
    elif page:
        assert rel in link['rel']
        qs = urllib.parse.urlparse(link['href']).query
        dqs = dict(urllib.parse.parse_qsl(qs))
        assert dqs['page'] == str(page)
    else:
        assert 'disabled' in link.parent['class']
