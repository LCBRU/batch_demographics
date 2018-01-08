import random
import string
from batch_demographics.database import db


class Batch(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __init__(self):
        self.name = ''.join(
            random.choice(string.ascii_uppercase + string.digits)
            for _ in range(10)
        )
