from flask import Flask
from flask_login import LoginManager
from config import config
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()
login_mamager = LoginManager()
login_mamager.session_protection = 'strong'
login_mamager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    login_mamager.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .exam import exam as exam_blueprint
    app.register_blueprint(exam_blueprint, url_prefix='/exam')

    from .forum import forum as forum_blueprint
    app.register_blueprint(forum_blueprint, url_prefix='/forum')

    from .test import test as test_blueprint
    app.register_blueprint(test_blueprint, url_prefix='/test')

    from .like import like as like_blueprint
    app.register_blueprint(like_blueprint, url_prefix='/like')

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    # from .auth import auth as auth_blueprint
    # app.register_blueprint(auth_blueprint, url_prefix = '/auth')

    return app
