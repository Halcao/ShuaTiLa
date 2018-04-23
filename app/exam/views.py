# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, flash, request, abort, session, jsonify
from flask_login import current_user, login_required, login_user
from . import exam
from .. import config
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
@login_required
def index():
    lesson_id = 1
    return redirect(url_for('.exam_page', lesson_id=lesson_id))


# 选出考试题目
@exam.route('/exam_page&lesson_id=<int:lesson_id>', methods=['GET'])
@login_required
def exam_page(lesson_id):
    # id = 5
    db = pymysql.connect('localhost', 'root', config['MYSQL_PASSWORD'], 'net_lesson', charset='utf8')
    cur = db.cursor()
    sql_choice = 'SELECT Problem_id, Question, Choice_a, Choice_b, Choice_c, Choice_d, Answer ' \
                 'FROM choice_problems WHERE Lesson_id = %s ORDER BY rand() LIMIT 50;'
    if lesson_id in (1, 4, 8, 10, 14, 15):
        sql_judge = 'SELECT Problem_id, Question, Answer FROM judge_problems ' \
                    'WHERE Lesson_id = %s ORDER BY rand() LIMIT 30;'
    else:
        sql_judge = 'SELECT Problem_id, Question, Answer FROM judge_problems ' \
                    'WHERE Lesson_id = %s ORDER BY rand() LIMIT 50;'
    sql_fill = 'SELECT Problem_id, Question, Answer FROM fill_problems ' \
               'WHERE Lesson_id = %s ORDER BY rand() LIMIT 10;'

    cur.execute(sql_choice, (lesson_id))
    questions = cur.fetchall()

    question_list = []
    question_list_index = []
    for question in questions:
        question_list.append(list(question))
        question_list_index.append(list(question)[0])

    cur.execute(sql_judge, (lesson_id))
    questions = cur.fetchall()

    judge_list = []
    judge_list_index = []
    for question in questions:
        judge_list.append(list(question))
        judge_list_index.append(list(question)[0])

    cur.execute(sql_fill, (lesson_id))
    questions = cur.fetchall()

    fill_list = []
    fill_list_index = []
    for question in questions:
        fill_list.append(list(question))
        fill_list_index.append(list(question)[0])

    cur.close()
    db.close()
    session['question_list_index'] = question_list_index
    session['judge_list_index'] = judge_list_index
    if lesson_id != 15:
        session['fill_list_index'] = fill_list_index
    return render_template('exam.html', lesson_id=lesson_id, question_list=question_list,
                           judge_list=judge_list, fill_list=fill_list)


# 计算测试成绩
@exam.route('/answer&lesson_id=<int:lesson_id>', methods=['POST'])
@login_required
def answer(lesson_id):
    if request.method == "POST":
        try:
            session['question_list_index']
        except:
            return redirect(url_for('auth.auth_page'))

        score = 0  # 计算分数
        # 错误题目列表
        wrong_list = []
        wrong_judge_list = []
        wrong_fill_list = []

        db = pymysql.connect('localhost', 'root', config['MYSQL_PASSWORD'], 'net_lesson', charset='utf8')
        cur = db.cursor()
        # 选择题
        for i in range(len(session['question_list_index'])):
            sql_choice = 'SELECT Problem_id, Question, Choice_a, Choice_b, Choice_c, Choice_d, Answer ' \
                         'FROM choice_problems WHERE Lesson_id = %s AND Problem_id = %s;'
            cur.execute(sql_choice, (lesson_id, session['question_list_index'][i]))
            question = cur.fetchall()
            q = list(question[0])
            # 判断单选题
            if len(q[-1]) == 1:
                reply = request.values.get('question' + str(i))
            # 判断多选题正确与否
            else:
                reply_list = request.values.getlist('question' + str(i))
                reply = ''
                for re in reply_list:
                    reply += re
            if q[-1] == reply:
                score += 1
            else:
                q.append(reply)
                wrong_list.append(q)

        # 判断题
        for i in range(len(session['judge_list_index'])):
            sql_judge = 'SELECT Problem_id, Question, Answer FROM judge_problems ' \
                        'WHERE Lesson_id = %s AND Problem_id = %s;'
            cur.execute(sql_judge, (lesson_id, session['judge_list_index'][i]))
            question = cur.fetchall()
            q = list(question[0])
            reply = request.values.get('judge' + str(i))
            if q[-1] == reply:
                score += 1
            else:
                q.append(reply)
                wrong_judge_list.append(q)

        if lesson_id != 15:
            for i in range(len(session['fill_list_index'])):
                sql_fill = 'SELECT Problem_id, Question, Answer FROM fill_problems ' \
                           'WHERE Lesson_id = %s AND Problem_id = %s;'
                cur.execute(sql_fill, (lesson_id, session['fill_list_index'][i]))
                question = cur.fetchall()
                q = list(question[0])
                reply = request.values.get('fill' + str(i))
                if q[-1] == reply:
                    score += 1
                else:
                    q.append(reply)
                    wrong_fill_list.append(q)
        else:
            score += 20

        session.pop('question_list_index', None)
        session.pop('judge_list_index', None)
        session.pop('fill_list_index', None)

        sql_score = 'SELECT History_score FROM lesson_info WHERE Student_id = %s AND Lesson_id = %s'
        cur.execute(sql_score, (current_user.id, lesson_id))
        if score < 10:
            history_score = list(cur.fetchall()[0])[0] + '00' + str(score) + ';'
        elif score < 100:
            history_score = list(cur.fetchall()[0])[0] + '0' + str(score) + ';'
        else:
            history_score = list(cur.fetchall()[0])[0] + str(score) + ';'

        if len(history_score) > 41:
            history_score = history_score[4:]
        score_list = history_score.split(';')
        sum = 0
        for i in range(1, len(score_list) - 1):
            sum += int(score_list[i])

        avg_score = sum * 1.0 / (len(score_list) - 2)

        sql_update_score = 'UPDATE lesson_info SET History_score = %s WHERE Student_id = %s AND Lesson_id = %s'
        cur.execute(sql_update_score, (history_score, current_user.id, lesson_id))
        db.commit()
        cur.close()
        db.close()
        return render_template('review.html', score=score, avg_score=avg_score,
                               wrong_list=wrong_list,wrong_judge_list=wrong_judge_list,
                               wrong_fill_list=wrong_fill_list, lesson_id=lesson_id)


'''
examId:qu_题目类型_题号
题目类型：
0——选择题
1——判断题
2——填空题
'''


@exam.route('/add_collect', methods=['POST'])
@login_required
def add_collect():
    # the method in flask document
    examId = str(request.form.get('examId'))
    lesson_id = int(request.form.get('lesson_id'))
    # the ordinary method of ajax
    # examId = str(request.data)
    info = examId.split('_')
    question_type = int(info[1])
    question_id = int(info[2])
    db = pymysql.connect('localhost', 'root', config['MYSQL_PASSWORD'], 'net_lesson', charset='utf8')
    cur = db.cursor()

    if question_type == 0:
        sql = 'INSERT INTO choice_collection VALUES (%s, %s, %s)'
    elif question_type == 1:
        sql = 'INSERT INTO judge_collection VALUES (%s, %s, %s)'
    elif question_type == 2:
        sql = 'INSERT INTO fill_collection VALUES (%s, %s, %s)'

    try:
        cur.execute(sql, (question_id, lesson_id, current_user.id))
    except:
        pass
    db.commit()
    cur.close()
    db.close()
    return ''


@exam.route('/delete_collect', methods=['POST'])
@login_required
def delete_collect():
    # the method in flask document
    examId = str(request.form.get('examId'))
    lesson_id = int(request.form.get('lesson_id'))
    # the ordinary method of ajax
    # examId = str(request.data)
    info = examId.split('_')
    question_type = int(info[1])
    question_id = int(info[2])
    db = pymysql.connect('localhost', 'root', config['MYSQL_PASSWORD'], 'net_lesson', charset='utf8')
    cur = db.cursor()

    if question_type == 0:
        sql = 'DELETE FROM choice_collection WHERE Student_id = %s ' \
              'AND Lesson_id = %s AND Problem_id = %s'
    elif question_type == 1:
        sql = 'DELETE FROM judge_collection WHERE Student_id = %s ' \
              'AND Lesson_id = %s AND Problem_id = %s'
    elif question_type == 2:
        sql = 'DELETE FROM fill_collection WHERE Student_id = %s ' \
              'AND Lesson_id = %s AND Problem_id = %s'

    try:
        cur.execute(sql, (current_user.id, lesson_id, question_id))
    except:
        pass
    db.commit()
    cur.close()
    db.close()
    return ''

# @exam.route('/review', methods=['POST'])
# def review():
#     return render_template('review.html', wrong_list=session['wrong_list'],
#                            wrong_judge_list=session['wrong_judge_list'],
#                            wrong_fill_list=session['wrong_fill_list'])
