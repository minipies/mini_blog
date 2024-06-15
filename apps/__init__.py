from flask import Flask
from .cfg import Development
from .exts import init_exts
from .user.models import *
from .article.models import *
from .user import views
from .article.views import article_bp


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(Development)
    init_exts(app)
    app.register_blueprint(views.user_bp)
    app.register_blueprint(article_bp)
    app.add_url_rule('/', endpoint='index', view_func=views.index)
    return app
