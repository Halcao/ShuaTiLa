# -*- coding: utf-8 -*-
from flask import redirect
from flask_login import login_required
from . import forum

@forum.route('/', methods=['GET'])
@login_required
def index():
    return redirect('http://0.0.0.0:4567')
