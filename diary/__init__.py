from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()
migrate = Migrate()

class Diary(db.Model):
    date = db.Column(db.Date(), nullable=False, primary_key=True)
    content = db.Column(db.Text(), nullable=False)

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)

    from . import views
    app.register_blueprint(views.bp)
    
    return app
    