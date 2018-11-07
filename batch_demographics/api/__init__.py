from flask import Blueprint, request
from flask.json import jsonify
from flask_marshmallow import Marshmallow
from batch_demographics.database import db
from batch_demographics.model import (
    Batch,
    batch_schema,
    batch_list_schema,
    Details,
    details_list_schema,
)

blueprint = Blueprint('apim', __name__)
ma = Marshmallow(blueprint)


@blueprint.record
def record(state):

    if db is None:
        raise Exception("This blueprint expects you to provide "
                        "database access through database")


@blueprint.route('/batch/')
def batches():
    batches = Batch.query.all()
    return batch_list_schema.jsonify(batches)


@blueprint.route('/batch/', methods=['POST'])
def batch_post():

    result, errors = batch_schema.load(request.get_json())

    if errors:
        return jsonify(errors), 400

    db.session.add(result)
    db.session.commit()

    return batch_schema.jsonify(result)


@blueprint.route('/batch/<int:batch_id>/details/')
def batch_details(batch_id):
    details = Details.query.filter(Details.batch_id == batch_id).all()
    return details_list_schema.jsonify(details)


@blueprint.route('/batch/<int:batch_id>/details/', methods=['POST'])
def batch_details_post(batch_id):
    batch = Batch.query.get(batch_id)

    result, errors = details_list_schema.load(request.get_json()['details'])

    if errors:
        return jsonify(errors), 400

    for d in result:
        d.batch = batch
        db.session.add(d)

    db.session.commit()

    return details_list_schema.jsonify(result)
