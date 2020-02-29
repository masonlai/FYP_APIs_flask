from flask import request, jsonify, Blueprint, Response
from flask.views import MethodView
from .. import db, app
import datetime
from faker import Faker
import random
from .models import DeceasedPage
from ..user.models import User
from ..visit_record.models import VisitRecord
from flask import make_response, current_app
from sqlalchemy import or_
from io import BytesIO
from ..comment.models import Comment
from werkzeug import FileWrapper
import os

page_blueprint = Blueprint('page', __name__)


@app.cli.command()
def fake():
    genderList = ['Male', 'Female']
    themeList = ['Theme1', 'Theme2', 'Theme3', 'Theme4']
    position = ['rightTheme', 'centerTheme', 'leftTheme']
    fake = Faker(locale='en_US')
    for i in range(500):
        first_name = fake.first_name()
        last_name = fake.last_name()
        gender = random.choice(genderList)
        date_of_birth = fake.date_this_decade(before_today=True, after_today=False)
        date_of_death = fake.date_this_decade(before_today=True, after_today=False)
        place_of_birth = fake.country()
        nationality = fake.country()
        life_profile = fake.text(max_nb_chars=200, ext_word_list=None)
        with open("999.jpg", 'rb') as f:
            byte_im = f.read()
        portrait_position = random.choice(position)
        theme = random.choice(themeList)
        personal_theme = None
        creating_date = datetime.datetime.now()
        pageInfo = DeceasedPage(first_name, last_name, gender, date_of_birth, date_of_death, \
                                place_of_birth, nationality, life_profile, byte_im, portrait_position, \
                                theme, personal_theme, creating_date)
        db.session.add(pageInfo)
        db.session.commit()
    for i in range(200):
        username = fake.first_name()
        password = fake.first_name()
        email = fake.email()
        religion = fake.country()
        users = User(username, password, email, religion)
        db.session.add(users)
        db.session.commit()
    for i in range(400):
        content = fake.text(max_nb_chars=200, ext_word_list=None)
        page = DeceasedPage.query.all()
        user = User.query.all()
        page_id = random.choice(page)
        user_id = random.choice(user)
        creating_date = datetime.datetime.now()
        comment_info = Comment(content, page_id.id, creating_date, user_id.id)
        db.session.add(comment_info)
        db.session.commit()

        page_id = random.choice(page)
        user_id = random.choice(user)
        creating_date = datetime.datetime.now()
        VisitRecord_info = VisitRecord(page_id.id, creating_date, user_id.id)
        db.session.add(VisitRecord_info)
        db.session.commit()


@app.cli.command()
def test():
    page = DeceasedPage.query.all()
    print(page[0].id)


class ImageView(MethodView):
    def get(self, id):
        image = DeceasedPage.query.filter_by(id=id).first()
        b = BytesIO(image.portrait)
        w = FileWrapper(b)
        return Response(w, mimetype='image/jpeg', direct_passthrough=True)

class MelodyView(MethodView):
    def get(self):
        melody = os.path.abspath(os.path.dirname(__file__)) + '/melody.jpg'
        with open(melody, "rb") as image:
            file = image.read()
            bytesLike = bytearray(file)
        b = BytesIO(bytesLike)
        w = FileWrapper(b)
        return Response(w, mimetype='image/jpeg', direct_passthrough=True)

class ThemeView(MethodView):
    def get(self, id):
        pageInfo = DeceasedPage.query.filter_by(id=id).first()
        if pageInfo.personal_theme != None:
            b = BytesIO(pageInfo.personal_theme)
            w = FileWrapper(b)
            return Response(w, mimetype='image/jpeg', direct_passthrough=True)
        else:
            themeName = pageInfo.theme + '.jpg'
            theme = os.path.abspath(os.path.dirname(__file__)) + '/' + themeName
            with open(theme, "rb") as image:
                file = image.read()
                bytesLike = bytearray(file)
            b = BytesIO(bytesLike)
            w = FileWrapper(b)
            return Response(w, mimetype='image/jpeg', direct_passthrough=True)

class BackgroundMusicView(MethodView):
    def get(self, id):
        image = DeceasedPage.query.filter_by(id=id).first()
        b = BytesIO(image.background_music)
        w = FileWrapper(b)
        return Response(w, mimetype='audio/mpeg', direct_passthrough=True)

class PageView(MethodView):
    def get(self, key, page):
        items = {0: 'one', 1: 'two', 2: 'three', 3: 'four', 4: 'five', 5: 'six', 6: 'seven', 7: 'eight', 8: 'night',
                 9: 'ten'}
        per_page = 10
        path = current_app.config['hoster']
        pageIndex = DeceasedPage.query.filter(or_(DeceasedPage.first_name.like('%' + key + '%'), \
                                                  DeceasedPage.last_name.like('%' + key + '%'))) \
            .order_by(DeceasedPage.creating_date.desc()).paginate(page, per_page, error_out=False)
        try:
            response = {}
            for i in range(len(pageIndex.items)):
                response.update({
                    items[i]: {
                        'id': pageIndex.items[i].id,
                        'first_name': pageIndex.items[i].first_name,
                        'last_name': pageIndex.items[i].last_name,
                        'gender': pageIndex.items[i].gender,
                        'date_of_birth': pageIndex.items[i].date_of_birth,
                        'date_of_death': pageIndex.items[i].date_of_death,
                        'place_of_birth': pageIndex.items[i].place_of_birth,
                        'nationality': pageIndex.items[i].nationality,
                        'life_profile': pageIndex.items[i].life_profile,
                        'portrait_position': pageIndex.items[i].portrait_position,
                        'portrait': path + 'GetImage/' + str(pageIndex.items[i].id),
                        'creating_date': pageIndex.items[i].creating_date,
                        'next_num': pageIndex.has_next,
                        'prev_num': pageIndex.prev_num,
                    }
                })

            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {
                'message': str(e) + '1'
            }
            return make_response(jsonify(response)), 500

    def post(self):
        try:
            access_token = request.form.get('Authorization')
            if access_token != 'undefined':
                user_id = User.decode_token(access_token)
                if user_id != 'Invalid token. Please register or login':
                    first_name = request.form.get('first_name')
                    last_name = request.form.get('last_name')
                    gender = request.form.get('gender')
                    date_of_birth = request.form.get('date_of_birth')
                    date_of_death = request.form.get('date_of_death')
                    place_of_birth = request.form.get('place_of_birth')
                    nationality = request.form.get('nationality')
                    life_profile = request.form.get('life_profile')
                    portrait = request.files['portrait'].read()
                    portrait_position = request.form.get('portrait_position')
                    theme = request.form.get('theme')
                    try:
                        personal_theme = request.files['personal_theme'].read()
                    except:
                        personal_theme = None
                    try:
                        background_music = request.files['background_music'].read()
                    except:
                        background_music = None
                    creating_date = datetime.datetime.now()
                    a = date_of_birth.split()
                    b = date_of_death.split()
                    date_of_birth = datetime.datetime.strptime(a[1] + a[2] + a[3], '%b%d%Y')
                    date_of_death = datetime.datetime.strptime(b[1] + b[2] + b[3], '%b%d%Y')
                    pageInfo = DeceasedPage(first_name, last_name, gender, date_of_birth, date_of_death, \
                                            place_of_birth, nationality, life_profile, portrait, portrait_position, \
                                            theme, personal_theme, creating_date, background_music)
                    db.session.add(pageInfo)
                    db.session.commit()
                    db.session.flush()
                    db.session.refresh(pageInfo)
                    response = {
                        'message': 'You created successfully.',
                        'id': pageInfo.id,
                        'first_name': pageInfo.first_name,
                        'last_name': pageInfo.last_name,
                        'gender': pageInfo.gender,
                        'date_of_birth': pageInfo.date_of_birth,
                        'date_of_death': pageInfo.date_of_death,
                        'place_of_birth': pageInfo.place_of_birth,
                        'nationality': pageInfo.nationality,
                        'life_profile': pageInfo.life_profile,
                        'portrait_position': pageInfo.portrait_position,
                        'creating_date': pageInfo.creating_date

                    }
                    return make_response(jsonify(response)), 200
                else:
                    response = {
                        'message': 'please login',
                    }
                    return make_response(jsonify(response)), 500
            else:
                response = {
                    'message': 'please login',
                }
                return make_response(jsonify(response)), 500
        except Exception as e:
            response = {
                'message': str(e) + '1'
            }
            return make_response(jsonify(response)), 500


class PageDetailView(MethodView):
    def get(self, id):
        path = current_app.config['hoster']
        try:
            pageInfo = DeceasedPage.query.filter_by(id=id).first()
            ifMusic = None
            if pageInfo.background_music:
                ifMusic = path + 'Music/' + str(id)
            response = {
                'id': str(id),
                'first_name': pageInfo.first_name,
                'last_name': pageInfo.last_name,
                'gender': pageInfo.gender,
                'date_of_birth': pageInfo.date_of_birth,
                'date_of_death': pageInfo.date_of_death,
                'place_of_birth': pageInfo.place_of_birth,
                'nationality': pageInfo.nationality,
                'life_profile': pageInfo.life_profile,
                'portrait_position': pageInfo.portrait_position,
                'portrait': path + 'GetImage/' + str(id),
                'creating_date': pageInfo.creating_date,
                'theme': path + 'Theme/' + str(id),
                'Music': ifMusic,
                'Music_icon': path + 'Melody',
                'flower_url_base': path + 'flower/'
            }
            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500


Page_View = PageView.as_view('Page_View')
Image_View = ImageView.as_view('Image_View')
Theme_View = ThemeView.as_view('Theme_View')
Melody_View = MelodyView.as_view('Melody_View')
Music_View = BackgroundMusicView.as_view('Music_View')
Page_Detail_View = PageDetailView.as_view('Page_Detail_View')

app.add_url_rule(
    '/CreatingPage', view_func=Page_View, methods=['POST']
)
app.add_url_rule(
    '/GetPageIndex/<key>/<int:page>', view_func=Page_View, methods=['GET']
)
app.add_url_rule(
    '/GetImage/<int:id>', view_func=Image_View, methods=['GET']
)
app.add_url_rule(
    '/Music/<int:id>', view_func=Music_View, methods=['GET']
)
app.add_url_rule(
    '/Melody', view_func=Melody_View, methods=['GET']
)
app.add_url_rule(
    '/Page/<int:id>', view_func=Page_Detail_View, methods=['GET']
)
app.add_url_rule(
    '/Theme/<int:id>', view_func=Theme_View, methods=['GET']
)
