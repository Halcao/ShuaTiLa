# -*- coding: utf-8 -*-
from flask import redirect, url_for
from . import admin

@admin.route('/', methods=['GET'])
def index():
    return redirect(url_for('admin.admin_page'))
