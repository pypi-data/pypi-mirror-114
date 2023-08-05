from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension

# SQLAlchemy Database Extension
db = SQLAlchemy()

# SQLAlchemy Migration Extension
migrate = Migrate()

# Flask Debug Toolbar
toolbar = DebugToolbarExtension()


def create_app(config="{{project_name}}.config.TestConfig"):

    app = Flask(__name__)

    app.config.from_object(config)

    # Register Extenstions
    db.init_app(app)
    migrate.init_app(app, db)
    toolbar.init_app(app)

    # Import models
    import {{project_name}}.models

    # Registers all blueprints
    from .settings import register_blueprints
    register_blueprints(app)

    return app
