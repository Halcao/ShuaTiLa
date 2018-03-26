# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, flash, request, abort,current_app
from flask_login import current_user, login_required
from . import exam


@exam.route('/', methods=['GET', 'POST'])
def index():
    # return render_template('index.html')
    return redirect(url_for('.exam_page'))

@exam.route('/exam_page', methods=['GET', 'POST'])
def exam_page():
    question_list = [
        [u'第一题:', '1', '2', '3', '4'],
        ['The 2nd question:', '1', '2', '3', '4'],
        ['The 3rd question:', '1', '2', '3', '4'],
        ['The 4th question:', '1', '2', '3', '4']
    ]

    answer_list = ['A', 'B', 'D', 'B']
    return render_template('exam.html', question_list=question_list, answer_list=answer_list)


@exam.route('/answer', methods=['POST'])
def answer():
    if request.method == "POST":
        answer_list = []
        for i in range(4):
            answer_list.append(request.values.get('question' + str(i)))
        return str(answer_list)