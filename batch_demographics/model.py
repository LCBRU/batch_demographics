import string
import random

from datetime import datetime, date, timezone
from dateutil.relativedelta import relativedelta
from batch_demographics.database import db
from batch_demographics.marshmallow import ma
from marshmallow import ValidationError
from marshmallow_sqlalchemy import field_for
from marshmallow.validate import Length
from flask_security import UserMixin, RoleMixin


def random_password():
    return "".join(
        random.SystemRandom().choice(
            string.ascii_lowercase
            + string.ascii_uppercase
            + string.digits
            + string.punctuation
        )
        for _ in range(15)
    )


class Role(db.Model, RoleMixin):
    ADMIN_ROLENAME = "admin"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __str__(self):
        return self.name or ""


roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id")),
)

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), nullable=False, default=random_password)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(50))
    current_login_ip = db.Column(db.String(50))
    login_count = db.Column(db.Integer())
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    roles = db.relationship(
        "Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic")
    )

    def __str__(self):
        return self.email


class Batch(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)


class BatchSchema(ma.ModelSchema):

    name = field_for(Batch, 'name', validate=[Length(min=1, max=100)])

    class Meta:
        model = Batch


batch_schema = BatchSchema()
batch_list_schema = BatchSchema(many=True)


class Details(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    forename = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    dob = db.Column(db.Date())
    sex = db.Column(db.String(10))
    postcode = db.Column(db.String(10))
    nhs_number = db.Column(db.String(10))
    system_number = db.Column(db.String(10))
    address1 = db.Column(db.String(100))
    address2 = db.Column(db.String(100))
    address3 = db.Column(db.String(100))
    address4 = db.Column(db.String(100))
    address5 = db.Column(db.String(100))
    local_id = db.Column(db.String(100))

    batch_id = db.Column(db.Integer, db.ForeignKey('batch.id'))
    batch = db.relationship(
        "Batch",
        backref=db.backref(
            'details',
            order_by=id,
            cascade="all, delete-orphan",
        ))

    def __repr__(self):
        return "<Details nhs_number:%s>" % self.__dict__

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __lt__(self, other):
        return self.nhs_number < other.nhs_number

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)


def validate_dob(dob):

    if dob < (date.today() - relativedelta(years=120)):
        raise ValidationError("DOB too far in the past.")

    return dob


class DetailsSchema(ma.ModelSchema):

    dob = field_for(Details, 'dob', validate=[validate_dob])

    class Meta:
        model = Details


details_schema = DetailsSchema()
details_list_schema = DetailsSchema(many=True)
