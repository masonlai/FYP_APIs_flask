from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os, sys, click

SECRET_KEY = "masonlai_fyp"
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
        "api_version": "3.0",
        "api_base_url": app.config['hoster'],
        "api_registration_POST": app.config['hoster'] + "registration",
        "api_login_POST": app.config['hoster'] + "login",
        "api_CraeteComment_POST": app.config['hoster'] + "CraeteComment",
        "api_CraeteCommentImage_POST": app.config['hoster'] + "CraeteCommentImage",
        "api_GetCommentImage_GET": app.config['hoster'] + "GetCommentImage/<int:id>",
        "api_CraeteCommentVideo_POST": app.config['hoster'] + "CraeteCommentVideo",
        "api_GetComment_GET": app.config['hoster'] + "GetComment/<int:id>/<int:page>/<desc>",
        "api_CreatingPage_POST": app.config['hoster'] + "CreatingPage",
        "api_GetPageIndex_GET": app.config['hoster'] + "GetPageIndex/<key>/<int:page>",
        "api_GetImage_GET": app.config['hoster'] + "GetImage/<int:id>",
        "api_Music_GET": app.config['hoster'] + "Music/<int:id>",
        "api_MelodyImage_GET": app.config['hoster'] + "Melody",
        "api_Page_GET": app.config['hoster'] + "Page/<int:id>",
        "api_Theme_GET": app.config['hoster'] + "Theme/<int:id>",
        "api_DefaultThemeList_GET": app.config['hoster'] + "DefaultThemeList",
        "api_DefaultTheme_GET": app.config['hoster'] + "DefaultTheme/<name>",
        "api_AddVisitRecord_POST": app.config['hoster'] + "visitRecord",
        "api_visit_Record_Flower_View_GET": app.config['hoster'] + "flower/<name>",
        "api_get_visitRecord——GET": app.config['hoster'] + "get_visitRecord/<int:id>",

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
