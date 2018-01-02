from batch_demographics.database import db


class Batch(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
