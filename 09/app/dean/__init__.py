from flask import Blueprint

dean = Blueprint('dean', __name__)

from . import views