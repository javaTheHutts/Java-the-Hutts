"""
----------------------------------------------------------------------
Authors: Nicolai van Niekerk, Jan-Justin van Tonder
----------------------------------------------------------------------
Initialises logging and starts the server.
----------------------------------------------------------------------
"""

import argparse
import ssl
from flask import Flask, request
from flask_cors import CORS
from hutts_verification.utils import hutts_logger
from hutts_verification.verification.controllers import verify
from hutts_verification.image_processing.controllers import extract

# Initialise flask application.
app = Flask(__name__)
CORS(app)
HOST = '0.0.0.0'
PORT = 5000

@app.before_request
def log_request():
    """
    This function is responsible for logging an incoming request to the server.
    """
    e = request.environ
    message_fmt = 'Request: %s %s %s'
    hutts_logger.logger.debug(
        message_fmt,
        e['REQUEST_METHOD'],
        e['PATH_INFO'],
        e['SERVER_PROTOCOL']
    )


@app.after_request
def log_response(response):
    """
    This function is responsible for logging the response to a request.
    """
    e = request.environ
    message_fmt = 'Response: %s %s %s %d'
    hutts_logger.logger.info(
        message_fmt,
        e['REQUEST_METHOD'],
        e['PATH_INFO'],
        e['SERVER_PROTOCOL'],
        response.status_code
    )
    return response


@app.errorhandler(Exception)
def error_handler(error):
    """
    A very general exception handler for unhandled exceptions.
    """
    return str(error), 500


if __name__ == '__main__':
    # Parse args.
    parser = argparse.ArgumentParser(description='Starts the application server.')
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('--secure', help='run the server with SSL enabled', action='store_true')
    args = vars(parser.parse_args())
    # Initialise blueprints
    app.register_blueprint(verify)
    app.register_blueprint(extract)
    # Run the server.
    hutts_logger.disable_flask_logging(app)
    hutts_logger.logger.info('* Running on https://%s:%d/', HOST, PORT)
    app.debug = args['debug']

    # This is only for remote server
    if args['secure']:
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain('/etc/ssl/certs/javathehutts/javathehutts_me.crt', '/etc/ssl/certs/javathehutts/javathehutts_me.key')
        hutts_logger.logger.info("Running server with SSL")
        app.run(host=HOST, port=PORT, threaded=True, ssl_context=context)
    else:
        hutts_logger.logger.warning("Running server without SSL")
        app.run(host=HOST, port=PORT, threaded=True)
