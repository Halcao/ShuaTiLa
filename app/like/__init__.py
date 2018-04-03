from flask import Blueprint


like = Blueprint('like', __name__)


from . import views, errors
