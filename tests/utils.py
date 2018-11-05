import datetime
import dateutil.parser
import pytz

from batch_demographics.database import db


def assert_objects_equals_dictionaries(objs, dics):
    for ob, dic in zip(objs, dics):
        assert_object_equals_dictionary(obj=ob, dic=dic)


def assert_object_equals_dictionary(obj, dic):
    for field_name, dic_value in dic.items():
        obj_value = getattr(obj, field_name)

        if isinstance(obj_value, db.Model):
            assert dic_value == obj_value.id
        elif isinstance(obj_value, datetime.datetime):
            tz_obj_value = pytz.utc.localize(obj_value)

            if isinstance(dic_value, datetime.datetime):
                assert dic_value == tz_obj_value
            else:
                assert dateutil.parser.parse(dic_value) == tz_obj_value
        elif isinstance(obj_value, datetime.date):
            if isinstance(dic_value, datetime.date):
                assert dic_value == obj_value
            else:
                assert dateutil.parser.parse(dic_value).date() == obj_value
        else:
            assert dic_value == obj_value
