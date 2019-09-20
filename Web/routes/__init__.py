from flask import Blueprint


main = Blueprint('routes', __name__)

from . import routes

def init_app(app):
    pass
