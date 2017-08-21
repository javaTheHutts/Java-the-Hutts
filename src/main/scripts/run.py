"""
----------------------------------------------------------------------
Authors: Nicolai van Niekerk, Jan-Justin van Tonder
----------------------------------------------------------------------
Initialises logging and starts the server.
----------------------------------------------------------------------
"""

import argparse
from server import app
from flask import request
from server import hutts_logger


def init_logger(debug=False):
    """
    Disables flask's built-in logging handlers and initialises custom logger.
    """
    hutts_logger.disable_flask_logging(app)
    hutts_logger.setup_logger(app, debug=debug)


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

if __name__ == '__main__':
    # Parse args.
    parser = argparse.ArgumentParser(description='Start the application server.')
    parser.add_argument('-d', '--debug', action='store_true')
    args = vars(parser.parse_args())
    # Initialise logger.
    init_logger(debug=args['debug'])
    # Run the server.
    print('* Running server')
    app.run(debug=args['debug'])
