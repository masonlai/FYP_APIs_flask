from flask_sqlalchemy import SQLAlchemy
from flask_api import app

db = SQLAlchemy(app)

class account(db.Model):
    username = db.Column(db.String(15), primary_key=True)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    religion = db.column(db.String(20))
    birthday = db.Column(db.DateTime)
    gender = db.Column(db.String(6))
    education = db.column(db.String(20))

class page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    birthday = db.Column(db.DateTime, nullable=False)
    deathday = db.Column(db.DateTime, nullable=False)
    birth_place = db.Column(db.String(40), nullable=False)
    nationality = db.Column(db.String(20), nullable=False)
    life_profile = db.Column(db.Text, nullable=False)
    Theme = db.Column(db.Integer(1), nullable=False)
    background_img = db.Column(db.LargeBinary, nullable=False)
    creator_words = db.Column(db.Text)
    music = db.Column(db.LargeBinary)
    vedio = db.Column(db.LargeBinary)
    picture = db.Column(db.LargeBinary)

