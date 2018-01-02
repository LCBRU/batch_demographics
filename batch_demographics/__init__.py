"""Aplication to manage Frostgrave wizards
"""
import traceback
from flask import Flask, render_template
from flask_migrate import Migrate
from .ui import blueprint as ui_blueprint
from .api import blueprint as api_blueprint
from batch_demographics.database import db


def create_app(config):
    """ Used to create flask application"""
    app = Flask(__name__)
    app.config.from_object(config)

    with app.app_context():
        db.init_app(app)
        Migrate(app, db)

    app.register_blueprint(ui_blueprint)
    app.register_blueprint(api_blueprint, url_prefix='/api')

    @app.errorhandler(500)
    @app.errorhandler(Exception)
    def internal_error(exception):
        """Catch internal exceptions and 500 errors, display
            a nice error page and log the error.
        """
        print(traceback.format_exc())
        app.logger.error(traceback.format_exc())
        return render_template('500.html'), 500

    return app
