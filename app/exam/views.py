# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, flash, request, abort, session
from flask_login import current_user, login_required, current_app, login_user
from . import exam
import pymysql

'''
question_list——选择题
judge_list——判断题
fill_list——填空题

wrong_list——错误的选择题
wrong_judge_list——错误的判断题
wrong_fill_list——错误的填空题
'''

@exam.route('/', methods=['GET', 'POST'])
def index():
    # return render_template('index.html')
    id=1
    return redirect(url_for('.exam_page', id=id))

# 选出考试题目
@exam.route('/exam_page&id=<int:id>', methods=['GET'])
def exam_page(id):
    # id = 5
    db = pymysql.connect('localhost', 'root', '970306', 'net_lesson', charset='utf8')
    cur = db.cursor()
    sql_choice = 'SELECT Question, Choice_a, Choice_b, Choice_c, Choice_d, Answer ' \
                 'FROM choice_problems WHERE Lesson_id = %s ORDER BY rand() LIMIT 3;'
    sql_judge = 'SELECT Question, Answer FROM judge_problems ' \
                'WHERE Lesson_id = %s ORDER BY rand() LIMIT 2;'
    sql_fill = 'SELECT Question, Answer FROM fill_problems ' \
                'WHERE Lesson_id = %s ORDER BY rand() LIMIT 2;'

    cur.execute(sql_choice, (id))
    questions = cur.fetchall()

    question_list = []
    for question in questions:
        question_list.append(list(question))

    cur.execute(sql_judge, (id))
    questions = cur.fetchall()

    judge_list = []
    for question in questions:
        judge_list.append(list(question))

    cur.execute(sql_fill, (id))
    questions = cur.fetchall()

    fill_list = []
    for question in questions:
        fill_list.append(list(question))

    cur.close()
    db.close()
    session['question_list'] = question_list
    session['judge_list'] = judge_list
    session['fill_list'] = fill_list
    return render_template('exam.html', question_list=question_list,
                           judge_list=judge_list, fill_list=fill_list)

# 计算测试成绩
@exam.route('/answer', methods=['POST'])
def answer():
    if request.method == "POST":
        # reply_list = []
        # for i in range(4):
        #     reply_list.append(request.values.get('question' + str(i)))
        correct = 0 #计算正确的题目
        # 错误题目列表
        wrong_list = []
        wrong_judge_list = []
        wrong_fill_list = []

        # 选择题
        for i in range(len(session['question_list'])):
            # 判断单选题
            if len(session['question_list'][i][-1]) == 1:
                reply = request.values.get('question' + str(i))
            # 判断多选题正确与否
            else:
                reply_list = request.values.getlist('question' + str(i))
                reply = ''
                for re in reply_list:
                    reply += re
            if session['question_list'][i][-1] == reply:
                correct += 1
            else:
                session['question_list'][i].append(reply)
                wrong_list.append(session['question_list'][i])

        # 判断题
        for i in range(len(session['judge_list'])):
            reply = request.values.get('judge' + str(i))
            if session['judge_list'][i][-1] == reply:
                correct += 1
            else:
                session['judge_list'][i].append(reply)
                wrong_judge_list.append(session['judge_list'][i])


        for i in range(len(session['fill_list'])):
            reply = request.values.get('fill' + str(i))
            if session['fill_list'][i][-1] == reply:
                correct += 1
            else:
                session['fill_list'][i].append(reply)
                wrong_fill_list.append(session['fill_list'][i])


        # score = correct / 4.0 * 100.0
        score = 50
        session.pop('question_list', None)
        session.pop('judge_list', None)
        session.pop('fill_list', None)
        # session['wrong_list'] = wrong_list
        # session['wrong_judge_list'] = wrong_judge_list
        # session['wrong_fill_list'] = wrong_fill_list
        # return render_template('answer.html', score=score)
        return render_template('review.html', score=score, wrong_list=wrong_list,
                           wrong_judge_list=wrong_judge_list,
                           wrong_fill_list=wrong_fill_list)

# @exam.route('/review', methods=['POST'])
# def review():
#     return render_template('review.html', wrong_list=session['wrong_list'],
#                            wrong_judge_list=session['wrong_judge_list'],
#                            wrong_fill_list=session['wrong_fill_list'])
