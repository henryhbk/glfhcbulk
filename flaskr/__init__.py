import os
from flask import Flask, url_for
from . import db
from . import auth
import logging
from flask_wtf.csrf import CSRFProtect

logging.basicConfig(filename='glfhc_bulk_app.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


def create_app(test_config=None):
    """
    Create and configure the Flask application.

    :param test_config: Optional. The configuration to use for testing.
    :type test_config: dict
    :return: The Flask application.
    :rtype: Flask
    """

    logging.info('+------------------------------------------------------------------+')
    logging.info('|                       APP STARTUP                                |')
    logging.info('+------------------------------------------------------------------+')

    app: Flask = Flask(__name__, template_folder='/templates', instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    csrf_protect = CSRFProtect()
    app.config['WTF_CSRF_ENABLED'] = False

    db.init_app(app)
    app.register_blueprint(auth.blueprint)

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
    print('Site Map:')
    for rule in app.url_map.iter_rules():
        print('\t* Rule: ' + rule.endpoint)

    @app.route("/site-map")
    def site_map():
        links = []
        linkStr = " "
        for rule in create_app().url_map.iter_rules():
            # Filter out rules we can't navigate to in a browser
            # and rules that require parameters
            if "GET" in rule.methods and has_no_empty_params(rule):
                url = url_for(rule.endpoint, **(rule.defaults or {}))
                links.append((url, rule.endpoint))
                linkStr.join(rule.endpoint+" "+url)
                print(rule.endpoint+" "+url)
        # links is now a list of url, endpoint tuples
        return "Site Map:" + linkStr

    @app.route('/')
    def hello():
        # a simple test web page that says hello
        return 'GLFHC Bulk Update Utility'

    def has_no_empty_params(rule):
        defaults = rule.defaults if rule.defaults is not None else ()
        arguments = rule.arguments if rule.arguments is not None else ()
        return len(defaults) >= len(arguments)

    return app

