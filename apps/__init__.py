from flask import Flask
import setting
from exts import db, bootstrap
from apps.user.views import user_bp
from apps.article.view import article_bp


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(setting.DevelopmentConfig)

    db.init_app(app=app)
    bootstrap.init_app(app=app)

    app.register_blueprint(user_bp)
    app.register_blueprint(article_bp)
    return app
