from flask import Blueprint, render_template, redirect, url_for, request, current_app, abort
from flask_security import login_required, current_user
from batch_demographics.database import db
from batch_demographics.model import Batch, Column
from batch_demographics.ui.forms import BatchForm, SearchForm, ConfirmForm, MappingsForm
from batch_demographics.files import save_file
from batch_demographics.services.upload import extract_batch_column_headers


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
def index():
    search_form = SearchForm(formdata=request.args)

    q = Batch.query.filter(
        Batch.user == current_user
    ).filter(
        Batch.deleted == False
    )
    
    if search_form.search.data:
        q = q.filter(Batch.name.ilike('%{}%'.format(search_form.search.data)))

    batches = q.paginate(
        page=search_form.page.data,
        per_page=current_app.config["PAGE_SIZE"],
        error_out=False,
    )

    return render_template(
        'index.html',
        batches=batches,
        searchForm=search_form,
        confirm_form=ConfirmForm(),
    )


@blueprint.route('/upload', methods=['GET', 'POST'])
def upload():
    form = BatchForm()

    if form.validate_on_submit():

        batch = Batch(
            name=form.data['name'],
            filename=form.data['participant_file'].filename,
            user=current_user,
        )

        db.session.add(batch)
        db.session.commit()

        save_file(batch, form.data['participant_file'])
        extract_batch_column_headers(batch)
        batch.automap_columns()

        db.session.add(batch)
        db.session.commit()

        return redirect(url_for('ui.index'))

    else:

        return render_template('upload.html', form=form)


@blueprint.route('/delete', methods=['POST'])
def delete():
    form = ConfirmForm()

    if form.validate_on_submit():
        batch = Batch.query.get_or_404(form.id.data)

        if batch.user != current_user:
            abort(403)

        batch.deleted = 1

        db.session.commit()

    return redirect(request.referrer or url_for('ui.index'))


@blueprint.route('/batch/<int:batch_id>/edit', methods=['GET', 'POST'])
def edit_mappings(batch_id):
    batch = Batch.query.get_or_404(batch_id)

    if batch.user != current_user:
        abort(403)

    form = MappingsForm(column_mappings=[{
        'column_id': c.id,
        'column_name': c.full_name,
        'mapping': c.mapping,
    } for c in batch.columns])

    if form.validate_on_submit():
        for cm in form.column_mappings.entries:
            c = Column.query.get_or_404(cm.column_id.data)
            c.mapping = cm.mapping.data

            db.session.add(c)

        db.session.commit()

        return redirect(url_for('ui.index'))

    return render_template('mappings.html', form=form)
