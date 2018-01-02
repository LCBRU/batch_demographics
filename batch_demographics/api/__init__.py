from flask import Blueprint
from flask_restplus import Api, Resource
from batch_demographics.database import db


blueprint = Blueprint('api', __name__)
api = Api(
    blueprint,
    version='1.0',
    title='Batch Demographics API',
    description='API to submit and track requests to '
                'the UHL NHS Spine Demographics Batch Service',
)


@blueprint.record
def record(state):

    if db is None:
        raise Exception("This blueprint expects you to provide "
                        "database access through database")


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}
