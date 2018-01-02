import random
import string
from flask import Blueprint, render_template, redirect, url_for
from batch_demographics.database import db
from batch_demographics.core.model import Batch


core = Blueprint('core', __name__, template_folder='templates')


@core.record
def record(state):

    if db is None:
        raise Exception("This blueprint expects you to provide "
                        "database access through database")


@core.route('/')
@core.route("/<int:page>")
def index(page=1):
    batches = Batch.query.all()

    return render_template('index.html', batches=batches)


@core.route('/add')
def add():
    b = Batch()
    b.name = ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(10)
    )

    db.session.add(b)
    db.session.commit()

    return redirect(url_for('core.index'))
