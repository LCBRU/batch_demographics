# -*- coding: utf-8 -*-

import json
import pytest
import datetime
import batch_demographics
from faker import Faker
from faker.providers import BaseProvider
from bs4 import BeautifulSoup
from flask import Response
from flask.testing import FlaskClient
from batch_demographics.database import db
from config import TestConfig, TestConfigCRSF
from batch_demographics.model import User


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime) or isinstance(o, datetime.date):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


class CustomResponse(Response):
    def __init__(self, baseObject, requested_time, received_time):
        self.__class__ = type(baseObject.__class__.__name__,
                              (self.__class__, baseObject.__class__),
                              {})
        self.__dict__ = baseObject.__dict__
        self.requested_time = requested_time
        self.received_time = received_time
        self._soup = None

    @property
    def soup(self):
        if not self._soup:
            self._soup = BeautifulSoup(self.data, "html.parser")

        return self._soup


class CustomClient(FlaskClient):
    def __init__(self, *args, **kwargs):
        super(CustomClient, self).__init__(*args, **kwargs)

    def get(self, *args, **kwargs):
        requested_time = datetime.datetime.now(datetime.timezone.utc)
        response = super(CustomClient, self).get(*args, **kwargs)
        received_time = datetime.datetime.now(datetime.timezone.utc)
        return CustomResponse(response, requested_time, received_time)

    def post(self, *args, **kwargs):
        requested_time = datetime.datetime.now(datetime.timezone.utc)
        response = super(CustomClient, self).post(*args, **kwargs)
        received_time = datetime.datetime.now(datetime.timezone.utc)
        return CustomResponse(response, requested_time, received_time)


@pytest.yield_fixture(scope='function')
def app(request):
    app = batch_demographics.create_app(TestConfig)
    app.test_client_class = CustomClient
    context = app.app_context()
    context.push()

    db.create_all()

    yield app

    context.pop()


@pytest.yield_fixture(scope='function')
def client(app):
    client = app.test_client()

    yield client


@pytest.yield_fixture(scope='function')
def client_with_crsf(app):
    app = batch_demographics.create_app(TestConfigCRSF)
    app.test_client_class = CustomClient
    context = app.app_context()
    context.push()
    client = app.test_client()

    db.create_all()

    yield client

    context.pop()


class NhsFakerProvider(BaseProvider):
    def user_details(self):
        u = User(
            first_name=self.generator.first_name(),
            last_name=self.generator.last_name(),
            email=self.generator.email(),
            active=True,
        )
        return u
        
    def nhs_number(self):
        prefix = self.generator.random.randint(100000000, 999999999)

        weighted_prefix_values = [
            int(j) * (10 - (i + 1)) for i, j in enumerate(str(prefix))
        ]

        checksum = 11 - (sum(weighted_prefix_values) % 11)

        if checksum == 11:
            checksum = 0

        return str((prefix * 10) + checksum)

    def uhl_system_number(self):
        number = self.generator.random.randint(1, 9999999)

        return 'S' + str(number)

    def gender(self):
        return self.generator.random.choice(['F', 'M'])

    def adult_birthdate(self):
        return self.generator.date_time_between(
            start_date="-90y",
            end_date="-16y").date()

    def ethnicity(self):
        return self.generator.random.choice([
            'A',
            'B',
            'C',
            'D',
            'E',
            'F',
            'G',
            'H',
            'J',
            'K',
            'L',
            'M',
            'N',
            'P',
            'R',
            'S',
            'Z',
        ])

    def daps_details(self):
        address1, address2, address3, address4, address5 = (
            self.generator.address().split('\n') + [''] * 5)[:5]

        return {
            'forename': self.generator.first_name(),
            'surname': self.generator.last_name(),
            'dob': self.generator.adult_birthdate(),
            'sex': self.generator.gender(),
            'postcode': self.generator.postcode(),
            'nhs_number': self.generator.nhs_number(),
            'system_number': self.generator.uhl_system_number(),
            'address1': address1,
            'address2': address2,
            'address3': address3,
            'address4': address4,
            'address5': address5,
            'local_id': self.generator.pystr(min_chars=10, max_chars=10),
        }


@pytest.yield_fixture(scope='function')
def faker():
    result = Faker('en_GB')
    result.add_provider(NhsFakerProvider)

    yield result
