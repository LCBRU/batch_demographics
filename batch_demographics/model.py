from batch_demographics.database import db


class Batch(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)

    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name')
