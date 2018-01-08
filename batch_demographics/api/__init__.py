from flask import Blueprint
from flask_marshmallow import Marshmallow
from batch_demographics.database import db
from batch_demographics.model import Batch


blueprint = Blueprint('apim', __name__)
ma = Marshmallow(blueprint)


@blueprint.record
def record(state):

    if db is None:
        raise Exception("This blueprint expects you to provide "
                        "database access through database")


class BatchSchema(ma.ModelSchema):
    class Meta:
        model = Batch


batch_schema = BatchSchema()
batches_schema = BatchSchema(many=True)


@blueprint.route('/batch/')
def batches():
    batches = Batch.query.all()
    return batches_schema.jsonify(batches)
