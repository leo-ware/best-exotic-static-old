
from app import db


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.String)
    back = db.Column(db.String)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def new(front, back):
        new = Card(front, back)
        db.session.add(new)
        db.session.commit()
        return new
