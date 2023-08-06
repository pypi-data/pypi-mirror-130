import logging
from datetime import datetime

from flask import Flask
from flask_smorest import Api
from pyctuator.health.db_health_provider import DbHealthProvider
from pyctuator.pyctuator import Pyctuator
from apscheduler.schedulers.background import BackgroundScheduler
from .utils import pika_consumer
from .config import *
from .modules.rest.views import change_event
from .database import db

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

def call_pika():
    db.app = app
    pika_consumer.main()

def initialize_actuator(flask_app):
    actuator = Pyctuator(
        flask_app,
        app_name='change_event_service',
        app_description='Change Event Service API',
        app_url=f"http://{app.config['SERVER_NAME']}/",
        pyctuator_endpoint_url=flask_app.config.get("ACTUATOR_BASE_URI"),
        registration_url=None
    )
    actuator.set_build_info(
        name="change_event_service",
        version="1.0.0",
        time=datetime.fromisoformat("2021-10-12T00:00"),
    )

    db_engine = db.get_engine(flask_app)
    actuator.register_health_provider(DbHealthProvider(db_engine))




def initialize_app(flask_app):
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(call_pika, 'interval', minutes=1)
    sched.start()
    flask_app.config.from_mapping(API_CONFIG)
    flask_app.config.from_mapping(SQLALCHEMY_CONFIG)
    db.init_app(flask_app)
    db.create_all(app=flask_app)
    initialize_actuator(flask_app)
    api = Api(flask_app)
    Api.DEFAULT_ERROR_RESPONSE_NAME = None
    api.register_blueprint(change_event)


def main():
    initialize_app(app)
    log.info(f'>>>>> Starting server... <<<<<')
    app.run(debug=True)