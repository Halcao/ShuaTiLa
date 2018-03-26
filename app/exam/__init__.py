from flask import Blueprint


exam = Blueprint('exam', __name__)


from . import views, errors
