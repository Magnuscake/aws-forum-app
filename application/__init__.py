from flask import Flask
from .decorators import set_global_exception_handler

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "b'\xc3k\x912\xa5<F\xb8c\xfbV\xbf\x0c\x9e\xb8:'"

    set_global_exception_handler(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')

    return app
