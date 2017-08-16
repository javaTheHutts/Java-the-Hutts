from flask import Flask, request
from verification.controllers import verify
from image_processing.controllers import extract
from server import hutts_logger
"""
----------------------------------------------------------------------
Author: Nicolai van Niekerk, Jan-Justin van Tonder
----------------------------------------------------------------------
Initialises the 'app' object to a flask instance and registers relevant
blueprints. Additionally, it sets up the custom logger.
----------------------------------------------------------------------
"""

app = Flask(__name__)

app.register_blueprint(verify)
app.register_blueprint(extract)


@app.before_first_request
def setup_logger():
    hutts_logger.disable_flask_logging(app)
    hutts_logger.setup_logger()


@app.before_request
def log_request():
    e = request.environ
    message_fmt = 'Request: %s %s %s'
    hutts_logger.logger.debug(message_fmt, e['REQUEST_METHOD'], e['PATH_INFO'], e['SERVER_PROTOCOL'])


@app.after_request
def log_response(response):
    e = request.environ
    message_fmt = 'Response: %s %s %s %d'
    hutts_logger.logger.info(message_fmt, e['REQUEST_METHOD'], e['PATH_INFO'], e['SERVER_PROTOCOL'],
                             response.status_code)
    return response
