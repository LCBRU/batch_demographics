"""Aplication to manage Frostgrave wizards
"""
import traceback
from flask import Flask, render_template
from .ui import blueprint as ui_blueprint
from .api import blueprint as api_blueprint
from batch_demographics.database import db
from batch_demographics.marshmallow import ma
from batch_demographics.standard_views import init_standard_views
from batch_demographics.security import init_security
from batch_demographics.template_filters import init_template_filters

def create_app(config):
    """ Used to create flask application"""
    app = Flask(__name__)
    app.config.from_object(config)

    with app.app_context():
        db.init_app(app)
        ma.init_app(app)
        init_security(app)
        init_standard_views(app)
        init_template_filters(app)

    app.register_blueprint(ui_blueprint)
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
