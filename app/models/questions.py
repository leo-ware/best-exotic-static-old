from app import db

import pickle
import json
import random


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String)
    _pickled_options = db.Column(db.PickleType)
    index_correct = db.Column(db.Integer)
    free = db.Column(db.Boolean, index=True)

    def get_options(self):
        return pickle.loads(self._pickled_options)

    def set_options(self, options):
        self._pickled_options = pickle.dumps([str(i) for i in options])
        db.session.commit()

    def grade(self, index_selected=None, answer_selected=None):
        if bool(answer_selected) == bool(index_selected):
            raise ValueError("Specify exactly one of index_selected and answer_selected.")
        elif answer_selected:
            correct = self.get_options()[self.index_correct] == str(answer_selected)
        else:
            correct = int(index_selected) == self.index_correct

        if correct:
            help_text = random.choice(["Grape work!", "You're literally unbelievable.", "God is proud.", "Marry me.",
                                       "Ayy Buster, look who's givin' it to the old lady!", "Stalin approves.",
                                       "You have earned the admiration of the masses."])
        else:
            help_text = f"The correct answer was <span class='correct-answer'>" \
                        f"{self.get_options()[self.index_correct]}</span> "

        return json.dumps({'correct': correct, 'help_text': help_text})

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def new(question: str, options: list, index_correct: int, free=False):
        new_question = Question()
        new_question.question = question
        new_question.index_correct = index_correct
        new_question.free = free
        new_question.set_options(options)

        db.session.add(new_question)
        db.session.commit()

        return new_question
