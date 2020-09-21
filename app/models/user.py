from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import libgravatar as lg

from app import db, login_manager

questions = db.Table('questions_for_users',
                     db.Column('question_id', db.Integer, db.ForeignKey('question.id'), primary_key=True),
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True))

cards = db.Table('cards_for_users', db.Column('card_id', db.Integer, db.ForeignKey('card.id'), primary_key=True),
                 db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35), index=True)
    password_hash = db.Column(db.String)
    email = db.Column(db.String)
    premium = db.Column(db.Boolean)
    tutor = db.Column(db.Boolean)
    admin = db.Column(db.Boolean)
    questions = db.relationship('Question', secondary=questions, lazy='subquery',
                                backref=db.backref('users', lazy=True))
    cards = db.relationship('Card', secondary=cards, lazy='subquery',
                            backref=db.backref('users', lazy=True))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def assign_question(self, question):
        if not hasattr(question, "__iter__"):
            question = list(question)
        self.questions.append(question)
        db.session.commit()

    def assign_card(self, card):
        if not hasattr(card, "__iter__"):
            card = list(card)
        self.cards.append(card)
        db.session.commit()

    def get_next_card(self):
        self.cards.append(self.cards.pop(0))
        return self.cards[0]

    def upgrade(self):
        self.premium = True
        db.session.commit()

    def downgrade(self):
        self.premium = False
        db.session.commit()

    def promote_to_admin(self):
        self.admin = True
        db.session.commit()

    def revoke_admin(self):
        self.admin = False
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_gravatar(self, *args, **kwargs):
        return lg.Gravatar(self.email).get_image(*args, **kwargs)

    @staticmethod
    def new(name, password, email, tutor):
        new_user = User(name=name, email=email, tutor=tutor)
        new_user.name = name
        new_user.email = email
        new_user.tutor = tutor
        new_user.admin = False
        new_user.premium = False
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return new_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
