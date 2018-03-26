# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, flash, request, abort,current_app,session
from flask_login import current_user, login_required
from . import auth


@auth.route('/', methods=['GET', 'POST'])
def index():
    # return render_template('index.html')
    return redirect(url_for('.auth_page'))
@auth.route('/auth_page', methods=['GET', 'POST'])
def auth_page():
    if session:
        name = session.get('username')
        return render_template('auth.html',user_name=name)
    else:
        return render_template('auth.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    name = request.values.get("logname")
    password = request.values.get("logpass")
    if password != 'sss':
        #需要提示密码错
        flash("wrong password")
        return redirect(url_for('.auth_page'))
    else:
        session['username']= name
        return redirect(url_for('.auth_page'))

# @auth.route('/regist', methods=['GET', 'POST'])
# def login():
#     name = request.values.get("regname")
#     password = request.values.get("regpass")
#     if password!='sss':
#         #需要提示是否已经被注册
#         return redirect(url_for('.auth_page'))
#     else:
#         return redirect(url_for('.auth_page'))
# @auth.route('/regist', methods=['GET', 'POST'])
# def login():
#     return render_template('regist.html')

