# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, flash, request, abort, session
from flask_login import current_user, login_required, login_user
from . import test
from .. import config
import pymysql
import json

@test.route('/', methods=['GET', 'POST'])
def index():
    # return render_template('index.html')
    id = 1
    return redirect(url_for('.test_page', id=id))


@test.route('/test_page&id=<int:id>', methods=['GET', 'POST'])
def test_page(id):
    # id = 5
    S_id = current_user.id
    db = pymysql.connect('localhost', 'root', config['MYSQL_PASSWORD'], 'net_lesson', charset='utf8')
    cur = db.cursor()

    insert_user = 'INSERT INTO lesson_info(Student_id,Lesson_id) VALUES(%s,%s)'
    try:
        cur.execute(insert_user,(S_id,id))
        db.commit()
    except:
        pass

    sql_choice = 'SELECT Problem_id,Question, Choice_a, Choice_b, Choice_c, Choice_d, Answer ' \
                 'FROM choice_problems WHERE Lesson_id = %s ;'
    sql_judge = 'SELECT Problem_id,Question, Answer FROM judge_problems ' \
                'WHERE Lesson_id = %s ;'
    sql_fill = 'SELECT Problem_id,Question, Answer FROM fill_problems ' \
               'WHERE Lesson_id = %s ;'
    sql_last = 'SELECT Last_index FROM lesson_info ' \
               'WHERE Lesson_id = %s AND Student_id = %s;'

    sql_choice_like = 'SELECT Problem_id ' \
                 'FROM choice_collection WHERE Lesson_id = %s AND Student_id=%s;'
    sql_judge_like = 'SELECT Problem_id ' \
                 'FROM judge_collection WHERE Lesson_id = %s AND Student_id=%s;'
    sql_fill_like = 'SELECT Problem_id ' \
                 'FROM fill_collection WHERE Lesson_id = %s AND Student_id=%s;'


    cur.execute(sql_choice_like, (id,current_user.id))
    questions = cur.fetchall()
    all_like = []
    for question in questions:
        question1 = int(question[0]);
        all_like.append(question1)

    cur.execute(sql_judge_like, (id, current_user.id))
    questions = cur.fetchall()
    for question in questions:
        question1 = int(question[0]);
        all_like.append(question1)

    cur.execute(sql_fill_like, (id, current_user.id))
    questions = cur.fetchall()
    for question in questions:
        question1 = int(question[0]);
        all_like.append(question1)

    cur.execute(sql_last, (id,S_id))
    last = cur.fetchone()
    if last is None:
        last=0
    cur.execute(sql_choice, (id))
    questions = cur.fetchall()
    question_dict = []
    all_dict = []

    for question in questions:
        question2 = ["questionId", "questionTitle", "questionItems", "questionAnswer"]
        question1 = list(question)
        question1 = [str(question1[0]), question1[1],
                     question1[2] + ';' + question1[3] + ';' + question1[4] + ';' + question1[5], question1[6]]
        question_dict.append(dict(zip(question2, question1)))
        all_dict.append(dict(zip(question2, question1)))
        # question_dict.append(list(question))
    cur.execute(sql_judge, (id))
    questions = cur.fetchall()
    judge_dict = []
    for question in questions:
        question2 = ["questionId", "questionTitle", "questionItems", "questionAnswer"]
        question1 = list(question)
        question1 = [str(question1[0]), question1[1], " ; ", question1[2]]
        judge_dict.append(dict(zip(question2, question1)))
        all_dict.append(dict(zip(question2, question1)))
    cur.execute(sql_fill, (id))
    questions = cur.fetchall()
    fill_dict = []

    for question in questions:
        question2 = ["questionId", "questionTitle", "questionItems", "questionAnswer"]
        question1 = list(question)
        question1 = [str(question1[0]), question1[1], " ", question1[2]]
        fill_dict.append(dict(zip(question2, question1)))
        all_dict.append(dict(zip(question2, question1)))
    cur.close()
    db.close()
    return render_template('test.html', id=json.dumps(id), question_dict=json.dumps(question_dict),
                           judge_dict=json.dumps(judge_dict), fill_dict=json.dumps(fill_dict),
                           all_dict=json.dumps(all_dict),last=json.dumps(last),all_like=json.dumps(all_like))


@test.route('/save_page',methods=['GET', 'POST'])
def save_last():
    userlast = request.form.get('last')
    lessonid = request.form.get('lessonid')
    db = pymysql.connect('localhost', 'root', config['MYSQL_PASSWORD'], 'net_lesson', charset='utf8')
    cur=db.cursor()
    update_last = 'UPDATE lesson_info SET Last_index = %s WHERE Lesson_id = %s AND Student_id = %s'
    cur.execute(update_last, (userlast,lessonid,current_user.id))
    db.commit()
    db.close()
    return ''

@test.route('/like_page',methods=['GET', 'POST'])
def save_like():
    likeid = request.form.get('likeid')
    likeid=int(likeid)+1
    lessonid = request.form.get('lessonid')
    problemtype = int(request.form.get('problemtype'))
    j_l=int(request.form.get('j_l'))
    c_l = int(request.form.get('c_l'))
    print "problemtype=",problemtype
    db = pymysql.connect('localhost', 'root', config['MYSQL_PASSWORD'], 'net_lesson', charset='utf8')
    cur = db.cursor()
    if problemtype == 1:
        update_like = 'INSERT INTO choice_collection VALUES (%s,%s,%s)'
    if problemtype == 2:
        likeid=likeid-c_l;
        update_like = 'INSERT INTO judge_collection VALUES (%s,%s,%s)'
    if problemtype == 3:
        likeid = likeid - c_l-j_l;
        update_like = 'INSERT INTO fill_collection VALUES (%s,%s,%s)'
    cur.execute(update_like, (likeid, lessonid, current_user.id))
    db.commit()
    db.close()
    return ''

@test.route('/dislike_page',methods=['GET', 'POST'])
def save_dislike():
    dislikeid = request.form.get('dislikeid')
    dislikeid = int(dislikeid) + 1
    lessonid = request.form.get('lessonid')
    problemtype = int(request.form.get('problemtype'))
    j_l = int(request.form.get('j_l'))
    c_l = int(request.form.get('c_l'))
    db = pymysql.connect('localhost', 'root', config['MYSQL_PASSWORD'], 'net_lesson', charset='utf8')
    cur = db.cursor()
    if problemtype == 1:
        update_dislike = 'DELETE FROM choice_collection WHERE Problem_id=%s AND Lesson_id=%s AND Student_id=%s'
    if problemtype == 2:
        dislikeid = dislikeid - c_l;
        update_dislike = 'DELETE FROM judge_collection WHERE Problem_id=%s AND Lesson_id=%s AND Student_id=%s'
    if problemtype == 3:
        dislikeid = dislikeid - c_l - j_l;
        update_dislike = 'DELETE FROM fill_collection WHERE Problem_id=%s AND Lesson_id=%s AND Student_id=%s'
    cur.execute(update_dislike, (dislikeid, lessonid, current_user.id))
    db.commit()
    db.close()
    return ''