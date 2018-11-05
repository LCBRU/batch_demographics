from datetime import datetime, date, timezone
from dateutil.relativedelta import relativedelta
from batch_demographics.database import db
from batch_demographics.marshmallow import ma
from marshmallow import ValidationError
from marshmallow_sqlalchemy import field_for
from marshmallow.validate import Length


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
