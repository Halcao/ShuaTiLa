from flask import Blueprint


forum = Blueprint('forum', __name__)


from . import views, errors
