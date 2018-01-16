from flask import Blueprint, request
from flask.json import jsonify
from flask_marshmallow import Marshmallow
from batch_demographics.database import db
from batch_demographics.model import Batch, Details
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


class DetailsSchema(ma.ModelSchema):

    class Meta:
        model = Details


details_schema = DetailsSchema()
details_list_schema = DetailsSchema(many=True)


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


@blueprint.route('/batch/<int:batch_id>/details/')
def batch_details(batch_id):
    details = Details.query.filter(Details.batch_id == batch_id).all()
    return details_list_schema.jsonify(details)
