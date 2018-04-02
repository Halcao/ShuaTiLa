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


@test.route('/test_page&id=<int:id>', methods=['GET'])
def test_page(id):
    # id = 5
    db = pymysql.connect('localhost', 'root', config['MYSQL_PASSWORD'], 'net_lesson', charset='utf8')
    cur = db.cursor()
    sql_choice = 'SELECT Problem_id,Question, Choice_a, Choice_b, Choice_c, Choice_d, Answer ' \
                 'FROM choice_problems WHERE Lesson_id = %s ;'
    sql_judge = 'SELECT Problem_id,Question, Answer FROM judge_problems ' \
                'WHERE Lesson_id = %s ;'
    sql_fill = 'SELECT Problem_id,Question, Answer FROM fill_problems ' \
               'WHERE Lesson_id = %s ;'
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

    return render_template('test.html', id=id, question_dict=json.dumps(question_dict),
                           judge_dict=json.dumps(judge_dict), fill_dict=json.dumps(fill_dict),
                           all_dict=json.dumps(all_dict))
