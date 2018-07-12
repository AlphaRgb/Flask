from flask import Blueprint

resume = Blueprint('resume', __name__)

from . import views, errors