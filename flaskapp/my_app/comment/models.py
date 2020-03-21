from .. import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Comment(db.Model):
    __tablename__ = 'Comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    creating_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('User.id'))
    page_id = db.Column(db.Integer, ForeignKey('DeceasedPage.id'))
    image = relationship("Image")

    def __init__(self, content, page_id, creating_date, user_id):
        self.content = content
        self.page_id = page_id
        self.creating_date = creating_date
        self.user_id = user_id

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.Binary, nullable=False)
    comment_id = db.Column(db.Integer, ForeignKey('Comment.id'))

    def __init__(self, image, comment_id):
        self.image = image
        self.comment_id = comment_id

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    comment_id = db.Column(db.Integer, ForeignKey('Comment.id'))

    def __init__(self, url, comment_id):
        self.url = url
        self.comment_id = comment_id