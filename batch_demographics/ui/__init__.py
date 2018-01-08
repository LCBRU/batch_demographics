from flask import Blueprint, render_template, redirect, url_for
from batch_demographics.database import db
from batch_demographics.model import Batch


blueprint = Blueprint('ui', __name__, template_folder='templates')


@blueprint.record
def record(state):

    if db is None:
        raise Exception("This blueprint expects you to provide "
                        "database access through database")


@blueprint.route('/')
@blueprint.route("/<int:page>")
def index(page=1):
    batches = Batch.query.all()

    return render_template('index.html', batches=batches)


@blueprint.route('/add')
def add():
    db.session.add(Batch())
    db.session.commit()

    return redirect(url_for('ui.index'))
