"""Initialize Flask app."""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def page_not_found(e):
    """
    Displays 404 error html on invalid pages.
    """
    return render_template('404.html'), 404


def create_app(config="config.Config"):
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.register_error_handler(404, page_not_found)
    app.config.from_object(config)

    db.init_app(app)

    with app.app_context():
        # Import routes
        from . import routes
        from .models import User

        # Create database tables for our data models
        db.create_all()

        return app
