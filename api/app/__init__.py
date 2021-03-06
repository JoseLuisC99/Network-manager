import os
from flask import Flask, jsonify
from flask_mongoengine import MongoEngine
from flask_cors import CORS

import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from scripts.router import RouterInfo

MongoDB = MongoEngine()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config['MONGODB_DB'] = 'network_database'
    app.config['MONGODB_HOST'] = 'localhost'
    app.config['MONGODB_PORT'] = 27017
    # app.config['MONGODB_USERNAME'] = 'network-admin'
    # app.config['MONGODB_PASSWORD'] = 'pass1234'
    app.config['JWT_KEY'] = '_wxY@g7#8M28=j3b'

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    os.makedirs(app.instance_path, exist_ok=True)

    @app.after_request
    def add_header(resp):
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Methods'] = '*'
        resp.headers['Access-Control-Allow-Headers'] = '*'
        resp.headers['Access-Control-Request-Method'] = '*'
        resp.headers['Access-Control-Request-Headers'] = '*'
        return resp
    
    from . import tasks

    @app.before_first_request
    def init_tasks():
        main_router = RouterInfo('R1', '192.168.1.1')
        # First call to the functions
        tasks.getTopology(main_router)

        # Scheduler
        scheduler = BackgroundScheduler()
        scheduler.add_job(tasks.updateNetworkInfo, 'interval', [main_router], seconds=120)
        # scheduler.add_job(tasks.getTopology, 'interval', [main_router], seconds=300)
        # scheduler.add_job(tasks.getInterfacesInfo, 'interval', seconds=240)
        # scheduler.add_job(tasks.updateSystemInfo, 'interval', seconds=120)
        scheduler.start()
        atexit.register(lambda: scheduler.shutdown())
    
    @app.route('/')
    def index():
        return jsonify({'status': 'ok', 'info': {'api_version': '1.0.0'}})
    
    MongoDB.init_app(app)

    from . import auth
    from . import network
    from . import info

    app.register_blueprint(auth.bp)
    app.register_blueprint(network.bp)
    app.register_blueprint(info.bp)
    
    return app