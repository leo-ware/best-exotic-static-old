from app import app, cache
from app.models import Page, User
from app.big_brain import Interpreter

from flask import render_template, request, redirect
from werkzeug.exceptions import NotFound


@app.route('/facelift/<notion_url>')
@cache.cached()
def test(notion_url):
    i = Interpreter('https://www.notion.so/' + notion_url)
    return render_template('wiki/notion_page.html', page=i.render())


@app.route('/articles/browse')
@cache.cached()
def browse():
    try:
        query = request.args['query']
    except KeyError:
        query = ""
    return render_template('wiki/browse_pages.html', query=query, pages=Page.query.all())


@app.route('/articles')
def page():
    try:
        p = Page.query.get(int(request.args['id']))
        return render_template('wiki/page.html', page=p)
    except KeyError:
        redirect('/articles/browse')


@app.route('/articles/<page_name>')
@cache.cached()
def page_by_name(page_name):
    p = Page.query.filter_by(title=page_name).first()
    if p:
        return render_template('wiki/page.html', page=p)
    else:
        raise NotFound


@app.route('/tutors')
def show_tutors():
    return render_template('wiki/tutors.html', tutors=User.query.filter_by(tutor=True))
