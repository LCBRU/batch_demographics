from flask import Blueprint, render_template, redirect, url_for
from flask_security import login_required
from batch_demographics.database import db
from batch_demographics.model import Batch
from batch_demographics.ui.forms import BatchForm
from batch_demographics.files import save_file


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


@blueprint.route('/upload', methods=['GET', 'POST'])
def upload():
    form = BatchForm()

    if form.validate_on_submit():

        batch = Batch(
            name=form.data['name'],
            filename=form.data['participant_file'].filename,
        )
        db.session.add(batch)
        db.session.commit()

        save_file(batch, form.data['participant_file'])

        return redirect(url_for('ui.index'))

    else:

        return render_template('edit.html', form=form)
