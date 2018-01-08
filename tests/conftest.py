# -*- coding: utf-8 -*-

import pytest
import batch_demographics
from batch_demographics.database import db
from config import TestConfig, TestConfigCRSF


@pytest.yield_fixture(scope='function')
def app(request):
    app = batch_demographics.create_app(TestConfig)
    app.app_context().push()
    db.create_all()

    yield app


@pytest.yield_fixture(scope='function')
def client(app):
    client = app.test_client()

    yield client


@pytest.yield_fixture(scope='function')
def client_with_crsf(app):
    app = batch_demographics.create_app(TestConfigCRSF)
    app.app_context().push()
    client = app.test_client()

    yield client
