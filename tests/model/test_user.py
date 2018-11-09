# -*- coding: utf-8 -*-

def test_user__str(faker):
    u = faker.user_details()

    assert u.__str__() == u.email


def test_user__full_name(faker):
    u = faker.user_details()

    assert u.full_name == "{} {}".format(u.first_name, u.last_name)


def test_user__full_name__no_first_name(faker):
    u = faker.user_details()
    u.first_name = ""

    assert u.full_name == "{}".format(u.last_name)


def test_user__full_name__no_last_name(faker):
    u = faker.user_details()
    u.last_name = ""

    assert u.full_name == "{}".format(u.first_name)


def test_user__full_name__no_name(faker):
    u = faker.user_details()
    u.last_name = ""
    u.first_name = ""

    assert u.full_name == "{}".format(u.email)
