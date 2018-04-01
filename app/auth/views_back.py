# # -*- coding: utf-8 -*-
# from flask import render_template, redirect, url_for, flash, request, abort, current_app, session
# from flask_login import current_user, logout_user, login_user
# from . import auth
# from .. import config
# from ..models import User
# import pymysql
#
#
# @auth.route('/', methods=['GET', 'POST'])
# def index():
#     # return render_template('index.html')
#     return redirect(url_for('.auth_page'))
#
#
# @auth.route('/auth_page', methods=['GET', 'POST'])
# def auth_page():
#     if current_user.is_authenticated:
#         # name = session.get('username')
#         # print current_user.id
#         return render_template('auth.html', user_name=current_user.id)
#     else:
#         return render_template('auth.html')
#
#
# @auth.route('/login', methods=['GET', 'POST'])
# def login():
#     name = request.values.get("logname")
#     password = request.values.get("logpass")
#     db = pymysql.connect('localhost', 'root', config['MYSQL_PASSWORD'], 'net_lesson', charset='utf8')
#     cur = db.cursor()
#     # sql =  "select Student_id, Student_password from student where Student_id='%s'"%(str(name))
#     cur.execute("select Student_id, Student_password from student where Student_id=%s", (name))
#     results = cur.fetchall()
#     cur.close()
#     db.close()
#     if len(results) == 0:
#         flash(u"没有这个用户哦", 'info')
#         return redirect(url_for('.auth_page'))
#     elif results[0][1] != password:
#         # 需要提示密码错
#         flash(u"密码输错了...", 'warning')
#         return redirect(url_for('.auth_page'))
#     else:
#         # session['username'] = name
#         user = User(id=name)
#         login_user(user)
#         return redirect(url_for('.auth_page', ))
#
#
# @auth.route('/regist', methods=['GET', 'POST'])
# def regist():
#     regname = request.values.get("regname")
#     regemail = request.values.get("regemail")
#     regpass = request.values.get("regpass")
#     db = pymysql.connect('localhost', 'root', config['MYSQL_PASSWORD'], 'net_lesson', charset='utf8')
#     cur = db.cursor()
#     cur.execute("select Student_id from student where Student_id=%s", (regname))
#     results = cur.fetchall()
#     if len(results) > 0:
#         flash(u"这个ID已经被注册了噢，换一个吧", 'info')
#         return redirect(url_for('.auth_page'))
#     else:
#         cur.execute("insert into student VALUES (%s,%s,%s)", (regname, regpass, regemail))
#         flash(u"注册成功啦，现在可以登录啦", 'success')
#     cur.close()
#     db.commit()
#     db.close()
#     return redirect(url_for('.auth_page'))
#
#
# @auth.route('/log_off', methods=['GET', 'POST'])
# def log_off():
#     logout_user()
#     return redirect(url_for('.auth_page'))
#
#
# @auth.route('/find', methods=['GET', 'POST'])
# def find():
#     flogname = request.values.get("flogname")
#     flogemail = request.values.get("flogemail")
#     flogpass = request.values.get("flogpass")
#     db = pymysql.connect('localhost', 'root', config['MYSQL_PASSWORD'], 'net_lesson', charset='utf8')
#     cur = db.cursor()
#     # sql =  "select Student_id, Student_password from student where Student_id='%s'"%(str(name))
#     cur.execute("select Student_id, Email from student where Student_id=%s", (flogname))
#     results = cur.fetchall()
#     if len(results) == 0:
#         flash(u"没有这个用户哦", 'info')
#         return redirect(url_for('.auth_page'))
#     elif results[0][1] != flogemail:
#         # 需要提示密码错
#         flash(u"邮箱/手机号输错了...，再想想", 'warning')
#         return redirect(url_for('.auth_page'))
#     cur.execute("update student set Student_password=%s where Student_id=%s", (flogpass,flogname))
#     cur.close()
#     db.commit()
#     db.close()
#     flash(u"修改密码成功，可以登录啦", 'success')
#     return redirect(url_for('.auth_page'))