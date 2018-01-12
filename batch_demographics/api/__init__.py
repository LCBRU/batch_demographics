from flask import Blueprint, request
from flask.json import jsonify
from flask_marshmallow import Marshmallow
from batch_demographics.database import db
from batch_demographics.model import Batch
from marshmallow_sqlalchemy import field_for
from marshmallow.validate import Length

blueprint = Blueprint('apim', __name__)
ma = Marshmallow(blueprint)


@blueprint.record
def record(state):

    if db is None:
        raise Exception("This blueprint expects you to provide "
                        "database access through database")


class BatchSchema(ma.ModelSchema):

    name = field_for(Batch, 'name', validate=[Length(min=1, max=100)])

    class Meta:
        model = Batch


batch_schema = BatchSchema()
batches_schema = BatchSchema(many=True)


@blueprint.route('/batch/')
def batches():
    batches = Batch.query.all()
    return batches_schema.jsonify(batches)


@blueprint.route('/batch/', methods=['POST'])
def batch_post():

    result, errors = batch_schema.load(request.get_json())

    if errors:
        return jsonify(errors), 400

    db.session.add(result)
    db.session.commit()

    return batch_schema.jsonify(result)
