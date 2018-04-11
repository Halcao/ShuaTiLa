# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, flash, request, abort, current_app, session
from flask_login import current_user, logout_user, login_user
from . import auth
from .. import config
from ..models import User
import pymysql
import hashlib,datetime
import jwt

JWT_SECRET = 'ksaj./*&&*%&^$d9ad80fa'
JWT_ALGORITHM = 'HS256'

@auth.route('/', methods=['GET', 'POST'])
def index():
    # return render_template('index.html')
    return redirect(url_for('.auth_page'))


@auth.route('/auth_page', methods=['GET', 'POST'])
def auth_page():
    if current_user.is_authenticated:
        # name = session.get('username')
        # print current_user.id
        return render_template('auth.html', user_name=current_user.id)
    else:
        return render_template('auth.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    ip = request.remote_addr
    browser = request.user_agent.browser
    platform = request.user_agent.platform
    print('login',ip,browser,platform)
    name = request.values.get("logname")
    password = request.values.get("logpass")
    password = hashlib.md5(password).hexdigest()
    db = pymysql.connect('localhost', 'root', config['MYSQL_PASSWORD'], 'net_lesson', charset='utf8')
    cur = db.cursor()
    # sql =  "select Student_id, Student_password from student where Student_id='%s'"%(str(name))
    cur.execute("select Student_id, Student_password, Email, If_admin from student where Student_name=%s", (name))
    results = cur.fetchall()
    cur.close()
    db.close()
    if len(results) == 0:
        flash(u"没有这个用户哦", 'info')
        return redirect(url_for('.auth_page'))
    elif results[0][1] != password:
        # 需要提示密码错
        flash(u"密码输错了...", 'warning')
        return redirect(url_for('.auth_page'))
    else:
        # session['username'] = name
        user = User(id=results[0][0], name=name, email=results[0][2], if_admin=results[0][3])
        login_user(user)
        payload = {
            'id': results[0][0],
            'name': name,
            'email': results[0][2]
        }
        jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
        response = redirect(url_for('.auth_page'))
        response.set_cookie('forum_token', jwt_token)
        db = pymysql.connect('localhost', 'root', config['MYSQL_PASSWORD'], 'net_lesson', charset='utf8')
        cur = db.cursor()
        i = datetime.datetime.now()
        # sql =  "select Student_id, Student_password from student where Student_id='%s'"%(str(name))
        cur.execute("insert into log_info(Student_id,Log_event,created_at,event_ip) values (%s,%s,%s,%s)", (results[0][0],'login',str(i),str(ip)))
        cur.close()
        db.commit()
        db.close()
        return response


@auth.route('/regist', methods=['GET', 'POST'])
def regist():
    regname = request.values.get("regname")
    regstudentid = request.values.get("regstudentid")
    regemail = request.values.get("regemail")
    # print regemail
    regpass = request.values.get("regpass")
    regpass = hashlib.md5(regpass).hexdigest()
    db = pymysql.connect('localhost', 'root', config['MYSQL_PASSWORD'], 'net_lesson', charset='utf8')
    cur = db.cursor()
    cur.execute("select Student_name from student where Student_name=%s", (regname))
    results = cur.fetchall()
    if len(results) > 0:
        flash(u"这个用户名已经被注册了噢，换一个吧", 'info')
        return redirect(url_for('.auth_page'))
    cur.execute("select Student_id from student where Student_id=%s", (regstudentid))
    results = cur.fetchall()
    if len(results) > 0:
        flash(u"这个学号已经被注册了噢，换一个吧", 'info')
        return redirect(url_for('.auth_page'))
    else:
        cur.execute("insert into student(Student_id, Student_name, Student_password, Email) VALUES (%s,%s,%s,%s)", (regstudentid, regname, regpass, regemail))
        flash(u"注册成功啦，现在可以登录啦", 'success')
    cur.close()
    db.commit()
    db.close()
    return redirect(url_for('.auth_page'))


@auth.route('/log_off', methods=['GET', 'POST'])
def log_off():
    ip = request.remote_addr
    browser = request.user_agent.browser
    platform = request.user_agent.platform
    print('log off',ip,browser,platform)
    id = current_user.id
    logout_user()
    response = redirect(url_for('.auth_page'))
    response.delete_cookie('forum_token')
    db = pymysql.connect('localhost', 'root', config['MYSQL_PASSWORD'], 'net_lesson', charset='utf8')
    cur = db.cursor()
    i = datetime.datetime.now()
    # sql =  "select Student_id, Student_password from student where Student_id='%s'"%(str(name))
    cur.execute("insert into log_info(Student_id,Log_event,created_at,event_ip) values (%s,%s,%s,%s)",(id, 'log off', str(i), str(ip)))
    cur.close()
    db.commit()
    db.close()
    return response


@auth.route('/find', methods=['GET', 'POST'])
def find():
    flogname = request.values.get("flogname")
    flogemail = request.values.get("flogemail")
    flogpass = request.values.get("flogpass")
    flogstudentid = request.values.get("flogstudentid")
    db = pymysql.connect('localhost', 'root', config['MYSQL_PASSWORD'], 'net_lesson', charset='utf8')
    cur = db.cursor()
    # sql =  "select Student_id, Student_password from student where Student_id='%s'"%(str(name))
    cur.execute("select Student_id,Email from student where Student_name=%s", (flogname))
    results = cur.fetchall()
    if len(results) == 0:
        flash(u"没有这个用户哦", 'info')
        return redirect(url_for('.auth_page'))
    elif results[0][0] != flogstudentid:
        # 需要提示密码错
        flash(u"学号输错了...，再想想", 'warning')
        return redirect(url_for('.auth_page'))
    elif results[0][1] != flogemail:
        # 需要提示密码错
        flash(u"邮箱输错了...，再想想", 'warning')
        return redirect(url_for('.auth_page'))
    cur.execute("update student set Student_password=%s where Student_id=%s", (flogpass, flogstudentid))
    cur.close()
    db.commit()
    db.close()
    flash(u"修改密码成功，可以登录啦", 'success')
    return redirect(url_for('.auth_page'))
