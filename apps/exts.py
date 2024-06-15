from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from flask_mail import Mail

sess = Session()
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()


def init_exts(app):
    sess.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
