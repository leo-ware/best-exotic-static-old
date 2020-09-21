from app import app
from app.routes.utils import failure_response
from app.models import Page, User, Question

from flask import request, render_template, flash, redirect
from flask_login import current_user, login_required


@app.route('/quiz')
def quiz_for_page():
    try:
        try:
            p = int(request.args['page_id'])
            reference = Page.query.get(p)
        except KeyError:
            reference = User.query.get(int(request.args['user_id']))
        quiz = [ques for ques in reference.questions]
    except KeyError:
        quiz = [Question.query.get(int(request.args['question_id']))]

    try:
        premium = current_user.premium
    except AttributeError:
        premium = False

    return render_template("interactive/quiz.html", quiz=quiz, is_premium=premium)


@app.route('/grade_question')
def grade_question():
    try:
        question_id = request.args['question_id']
        answer_selected = request.args['answer_selected']
    except KeyError:
        return failure_response("invalid response, make sure to include question-id and index-selected parameters")

    question = Question.query.get(int(question_id))
    return Question.grade(question, answer_selected=answer_selected)


@app.route('/flashcards')
def next_card():
    return render_template('interactive/flashcards.html')


@app.route('/essays', methods=['GET', 'POST'])
def essays():
    if request.method == 'GET':
        return render_template('interactive/essay_submit.html')
    elif request.method == 'POST':
        flash('Essay submitted')
        return redirect('/')