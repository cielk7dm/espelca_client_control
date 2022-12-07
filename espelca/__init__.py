import os

from flask import Flask

def create_app(test_config=None):
    #Create and configure client
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE = os.path.join(app.instance_path, 'espelca.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from espelca import db
    db.init_app(app)

    from espelca import auth
    app.register_blueprint(auth.bp)

    from espelca import application
    app.register_blueprint(application.bp)
    app.add_url_rule('/', endpoint='index')

    from espelca import error_handler
    app.register_error_handler(404, error_handler.page_not_found)
    
    return app