# -*- coding: utf-8 -*-
from flask import redirect
from . import forum

@forum.route('/', methods=['GET'])
def index():
    return redirect('http://0.0.0.0:4567')
