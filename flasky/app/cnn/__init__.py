import os
import sys
base_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(base_dir)

from flask import Blueprint

cnn = Blueprint('cnn', __name__)

from . import views, errors
