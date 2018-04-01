from flask_login import UserMixin
from . import login_mamager


class User(UserMixin):
    def __init__(self, **kwargs):
        self.id = kwargs['id']


@login_mamager.user_loader
def load_user(user_id):
    return User(id=user_id)
