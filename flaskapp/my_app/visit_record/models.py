from .. import db
from sqlalchemy import ForeignKey


class VisitRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creating_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('User.id'))
    page_id = db.Column(db.Integer, ForeignKey('DeceasedPage.id'))

    def __init__(self, page_id, creating_date, user_id):
        self.page_id = page_id
        self.creating_date = creating_date
        self.user_id = user_id
