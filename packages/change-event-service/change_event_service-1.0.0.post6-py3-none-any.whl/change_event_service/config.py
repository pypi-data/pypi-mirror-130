import os

SQLALCHEMY_CONFIG={
    "SQLALCHEMY_DATABASE_URI":os.environ.get('DB_URL','postgresql+psycopg2://sa:12345@localhost/change_event_db'),
    "SQLALCHEMY_TRACK_MODIFICATIONS": bool(os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS','False')),
}
API_CONFIG={
    # API/Swagger Configurations
    "API_TITLE" : os.environ.get('API_TITLE','Change Event Service'),
    "API_VERSION" : 'v1',
    "OPENAPI_VERSION": "3.0.2",
    "OPENAPI_URL_PREFIX": os.environ.get('OPENAPI_URL_PREFIX','/'),
    "OPENAPI_SWAGGER_UI_PATH": os.environ.get('OPENAPI_SWAGGER_UI_PATH','/swagger-ui'),
    "OPENAPI_JSON_PATH": os.environ.get('OPENAPI_JSON_PATH','/v3/api-docs'),
    "OPENAPI_SWAGGER_UI_URL": os.environ.get('OPENAPI_SWAGGER_UI_URL','https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.0.0-rc.4/'),
    # Actuator Settings
    "ACTUATOR_BASE_URI": os.environ.get('ACTUATOR_BASE_URI','http://localhost:8800/actuator'),
}
AMQP_CONFIG={
    "AMQP_HOST" : os.environ.get('AMQP_HOST','localhost'),
    "AMQP_VIRTUAL_HOST" : os.environ.get('AMQP_VIRTUAL_HOST','/'),
    "AMQP_QUEUE" : os.environ.get('AMQP_QUEUE','change_event'),
    "AMQP_USER" :  os.environ.get('AMQP_USER','guest'),
    "AMQP_PASSWORD":  os.environ.get('AMQP_PASSWORD','guest'),
    "AMQP_EXCHANGE": os.environ.get('AMQP_EXCHANGE','change_event'),
    "AMQP_ROUTING_KEY": os.environ.get('AMQP_ROUTING_KEY','event'),
}


