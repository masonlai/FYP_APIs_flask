from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os, sys

app = Flask(__name__)
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', prefix + os.path.join(app.root_path, 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
 
from my_app.user.views import user_blueprint
from my_app.book.views import book_blueprint
from my_app.borrow.views import borrow_blueprint

app.register_blueprint(user_blueprint)
app.register_blueprint(book_blueprint)
app.register_blueprint(borrow_blueprint)

db.create_all()