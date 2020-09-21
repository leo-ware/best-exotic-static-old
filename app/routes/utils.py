import json
from flask import flash, get_flashed_messages
from flask_login import current_user

from app import app


# define default success and failure responses for ajax requests
def success_response(msg=""):
    return json.dumps({'success': True, 'message': msg})


def failure_response(msg=""):
    return json.dumps({'success': False, 'message': msg})


@app.context_processor
def inject_globals():
    return {
        'user': current_user,
        'get_flashed_messages': get_flashed_messages
    }
