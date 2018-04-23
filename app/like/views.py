# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, flash, request, abort, session
from flask_login import current_user, login_required, login_user
from . import like
from .. import config
import pymysql
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

@like.route('/', methods=['GET', 'POST'])
@login_required
def index():
    # return render_template('index.html')
    id = 1
    return redirect(url_for('.like_page', id=id))


@like.route('/like_page&id=<int:id>', methods=['GET'])
@login_required
def like_page(id):
    # id = 5
    # print current_user.name
    S_id=current_user.id
    db = pymysql.connect('localhost', 'root', config['MYSQL_PASSWORD'], 'net_lesson', charset='utf8')
    cur = db.cursor()
    sql_choice = 'SELECT Problem_id,Question, Choice_a, Choice_b, Choice_c, Choice_d, Answer ' \
                 'FROM choice_problems WHERE Lesson_id = %s AND Problem_id in (' \
                 'SELECT Problem_id FROM choice_collection WHERE Lesson_id=%s AND Student_id=%s);'
    sql_judge = 'SELECT Problem_id,Question, Answer FROM judge_problems ' \
                'WHERE Lesson_id = %s  AND Problem_id in (' \
                 'SELECT Problem_id FROM judge_collection WHERE Lesson_id=%s AND Student_id=%s);'
    sql_fill = 'SELECT Problem_id,Question, Answer FROM fill_problems ' \
               'WHERE Lesson_id = %s  AND Problem_id in (' \
                 'SELECT Problem_id FROM fill_collection WHERE Lesson_id=%s AND Student_id=%s);'
    cur.execute(sql_choice, (id,id,S_id))
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
    cur.execute(sql_judge, (id,id,S_id))
    questions = cur.fetchall()
    judge_dict = []
    for question in questions:
        question2 = ["questionId", "questionTitle", "questionItems", "questionAnswer"]
        question1 = list(question)
        question1 = [str(question1[0]), question1[1], " ; ", question1[2]]
        judge_dict.append(dict(zip(question2, question1)))
        all_dict.append(dict(zip(question2, question1)))
    cur.execute(sql_fill, (id,id,S_id))
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

    return render_template('like.html', id=json.dumps(id), question_dict=json.dumps(question_dict),
                           judge_dict=json.dumps(judge_dict), fill_dict=json.dumps(fill_dict),
                           all_dict=json.dumps(all_dict))
@like.route('/delheart_page',methods=['GET', 'POST'])
@login_required
def delheart_page():
    title = request.form.get('title')
    itemss = int ((request.form.get('itemss')))
    lessonid1= int ((request.form.get('lessonid1')))
    db = pymysql.connect('localhost', 'root', config['MYSQL_PASSWORD'], 'net_lesson', charset='utf8')
    cur = db.cursor()
    update_like = "aa"
    if itemss == 4:
        update_like = 'DELETE FROM choice_collection WHERE ' \
                      'Lesson_id=%s AND Student_id=%s' \
                      ' AND Problem_id = (SELECT Problem_id FROM choice_problems' \
                      ' WHERE choice_problems.Question=%s ' \
                      'AND choice_collection.Problem_id=choice_problems.Problem_id ' \
                      'AND choice_collection.Lesson_id=choice_problems.Lesson_id)'

    if itemss == 2:
        update_like ='DELETE FROM judge_collection WHERE ' \
                      'Lesson_id=%s AND Student_id=%s' \
                      ' AND Problem_id = (SELECT Problem_id FROM judge_problems' \
                      ' WHERE judge_problems.Question=%s ' \
                      'AND judge_collection.Problem_id=judge_problems.Problem_id ' \
                      'AND judge_collection.Lesson_id=judge_problems.Lesson_id)'
    if itemss == 1:
        update_like = 'DELETE FROM fill_collection WHERE ' \
                      'Lesson_id=%s AND Student_id=%s' \
                      ' AND Problem_id = (SELECT Problem_id FROM fill_problems' \
                      ' WHERE fill_problems.Question=%s ' \
                      'AND fill_collection.Problem_id=fill_problems.Problem_id ' \
                      'AND fill_collection.Lesson_id=fill_problems.Lesson_id)'
    try:
        cur.execute(update_like, (lessonid1, current_user.id,title))
    except:
        pass
    db.commit()
    db.close()
    return ''


@like.route('/oheart_page',methods=['GET', 'POST'])
@login_required
def oheart_page():
    title = request.form.get('title')
    itemss = int ((request.form.get('itemss')))
    lessonid1= int ((request.form.get('lessonid1')))
    db = pymysql.connect('localhost', 'root', config['MYSQL_PASSWORD'], 'net_lesson', charset='utf8')
    cur = db.cursor()
    update_like="aa"
    again_like="aa"
    laji= int (1)
    if itemss == 4:
        update_like = 'INSERT INTO choice_collection VALUES (%s,%s,%s) '
        again_like = 'UPDATE choice_collection SET Problem_id=(SELECT Problem_id FROM choice_problems' \
                      ' WHERE choice_problems.Question=%s )'

    if itemss == 2:
        update_like = 'INSERT INTO judge_collection VALUES (%s,%s,%s) '
        again_like = 'UPDATE judge_collection SET Problem_id=(SELECT Problem_id FROM judge_problems' \
                             ' WHERE judge_problems.Question=%s )'
    if itemss == 1:
        update_like = 'INSERT INTO fill_collection VALUES (%s,%s,%s) '
        again_like = 'UPDATE fill_collection SET Problem_id=(SELECT Problem_id FROM fill_problems' \
                             ' WHERE fill_problems.Question=%s )'
    try:


        cur.execute(update_like, (laji,lessonid1, current_user.id))
        cur.execute(again_like, (title))
    except:
        pass
    db.commit()
    db.close()
    return ''