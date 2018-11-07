from flask import Blueprint, render_template, redirect, url_for
from flask_security import login_required
from batch_demographics.database import db
from batch_demographics.model import Batch
from batch_demographics.ui.forms import BatchForm


blueprint = Blueprint('ui', __name__, template_folder='templates')


@blueprint.record
def record(state):

    if db is None:
        raise Exception("This blueprint expects you to provide "
                        "database access through database")


# Login required for all views
@blueprint.before_request
@login_required
def before_request():
    pass


@blueprint.route('/')
@blueprint.route("/<int:page>")
def index(page=1):
    batches = Batch.query.all()

    return render_template('index.html', batches=batches)


@blueprint.route('/add', methods=['GET', 'POST'])
def add():
    form = BatchForm()

    if form.validate_on_submit():

        db.session.add(Batch(name=form.data['name']))
        db.session.commit()

        return redirect(url_for('ui.index'))

    else:

        return render_template('edit.html', form=form)
