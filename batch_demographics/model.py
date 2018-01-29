from datetime import datetime
from batch_demographics.database import db


class Batch(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    date_created = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.date_created = datetime.now()


class Details(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
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
