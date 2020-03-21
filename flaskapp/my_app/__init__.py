from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os, sys, click

SECRET_KEY="masonlai_fyp"
app = Flask(__name__)
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', prefix + os.path.join(app.root_path, 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['hoster'] = 'http://127.0.0.1:5000/'
app.config["JSON_SORT_KEYS"] = False
db = SQLAlchemy(app)
CORS(app)

@app.route('/')
@app.route('/home')
def home():
    return jsonify({
        "api_version": "2.0",
        "api_base_url": app.config['hoster'],
        "api_registration_url": app.config['hoster']+"registration",
        "api_login_url": app.config['hoster']+"login",
        "api_CreatingPage_url": app.config['hoster']+"CreatingPage",
        "api_GetPageIndex_url": app.config['hoster']+"GetPageIndex/<key>/<int:page>",
        "api_getPortrait_url": app.config['hoster']+"GetImage/<int:id>'",
        "api_getPageInfo_url": app.config['hoster']+"Page/<int:id>",
        "api_getTheme_url": app.config['hoster']+"Theme/<int:id>",
        "api_CraeteComment_url": app.config['hoster']+"CraeteComment",
        "api_GetComment_url": app.config['hoster']+"GetComment/<int:id>/<int:page>",
        "api_postVisitRecord_url": app.config['hoster']+"visitRecord",
        "api_getVisitRecord_url": app.config['hoster']+"get_visitRecord/<int:id>",
        "api_Melody": app.config['hoster'],


    })

from .user.views import user_blueprint
from .page.views import page_blueprint
from .comment.views import comment_blueprint
from .visit_record.views import visitRecord_blueprint

app.register_blueprint(user_blueprint)
app.register_blueprint(page_blueprint)
app.register_blueprint(comment_blueprint)
app.register_blueprint(visitRecord_blueprint)

@app.cli.command()
def initdb():
    db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


if __name__ == '__main__':
    app.run(debug=True)