import os
from flask import Flask, redirect, url_for

from flaskr.error import access_denied

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def hello():
        return redirect(url_for("auth.login"))
    
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import forum
    app.register_blueprint(forum.bp)
    app.add_url_rule('/', endpoint='index')
    
    from . import profile
    app.register_blueprint(profile.bp)
    app.add_url_rule('/', endpoint='profile')

   
    # error sayfaları
    app.register_error_handler(403,access_denied)

    return app