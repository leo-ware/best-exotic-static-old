from app import db
import datetime

questions = db.Table('questions_for_pages',
                     db.Column('question_id', db.Integer, db.ForeignKey('question.id'), primary_key=True),
                     db.Column('page_id', db.Integer, db.ForeignKey('page.id'), primary_key=True)
                     )


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    copyright_info = db.Column(db.String)
    content = db.Column(db.TEXT)
    questions = db.relationship('Question', secondary=questions, lazy='subquery',
                                backref=db.backref('pages', lazy=True))

    def assign_question(self, question):
        if not hasattr(question, "__iter__"):
            question = list(question)
        for q in question:
            self.questions.append(q)
        db.session.commit()

    def content_teaser(self, size=15):
        return self.content[:size-3]+'...'

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def new(title: str, author: str, content: str, copyright_info=""):
        new_page = Page()
        new_page.title = title
        new_page.author = author
        new_page.content = content
        new_page.copyright_info = copyright_info

        db.session.add(new_page)
        db.session.commit()

        return new_page
