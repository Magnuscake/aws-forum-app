from functools import wraps
import traceback

from flask import session, redirect

def set_global_exception_handler(app):
    @app.errorhandler(Exception)
    def unhandled_exception(e):
        response = dict()
        error_message = traceback.format_exc()
        app.logger.error("Caught Exception: {}".format(error_message)) #or whatever logger you use
        response["errorMessage"] = error_message
        return response, 500

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')

    return wrap
