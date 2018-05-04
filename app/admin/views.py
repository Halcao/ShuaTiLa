# -*- coding: utf-8 -*-
from flask import redirect, url_for, render_template, request
from flask_login import login_required
from . import admin
from .. import config
import pymysql


@admin.route('/', methods=['GET'])
@login_required
def index():
    return redirect(url_for('admin.admin_page'))


@admin.route('/admin_page', methods=['GET'])
@login_required
def admin_page():
    return render_template('admin.html')


@admin.route('/change_answer', methods=['GET', 'POST'])
@login_required
def change_answer():
    if request.method == "POST":
        lesson_id = request.values.get('lesson_id')
        problem_id = request.values.get('problem_id')
        problem_type = request.values.get('problem_type')
        answer = request.values.get('answer')

        db = pymysql.connect('shuatila.com', 'root', config['MYSQL_PASSWORD'], 'net_lesson', charset='utf8')
        cur = db.cursor()
        if problem_type == '1':
            sql = 'UPDATE choice_problems SET Answer = %s WHERE Problem_id = %s AND Lesson_id = %s'
            try:
                cur.execute(sql, (answer, problem_id, lesson_id))
            except:
                pass
        elif problem_type == '2':
            sql = 'UPDATE judge_problems SET Answer = %s WHERE Problem_id = %s AND Lesson_id = %s'
            try:
                cur.execute(sql, (int(answer), problem_id, lesson_id))
            except:
                pass
        elif problem_type == '3':
            sql = 'UPDATE fill_problems SET Answer = %s WHERE Problem_id = %s AND Lesson_id = %s'
            try:
                cur.execute(sql, (answer, problem_id, lesson_id))
            except:
                pass
        db.commit()
        cur.close()
        db.close()

    return render_template('change_answer.html')

@admin.route('/add_admin', methods=['GET', 'POST'])
@login_required
def add_admin():
    if request.method == "POST":
        student_id = request.values.get('student_id')

        db = pymysql.connect('shuatila.com', 'root', config['MYSQL_PASSWORD'], 'net_lesson', charset='utf8')
        cur = db.cursor()
        sql = 'UPDATE student SET If_admin = 1 WHERE Student_id = %s'
        try:
            cur.execute(sql, (student_id))
        except:
            pass
        db.commit()
        cur.close()
        db.close()

    return render_template('add_admin.html')
