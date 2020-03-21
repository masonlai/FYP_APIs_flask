from flask import request, jsonify, Blueprint, make_response, Response, current_app
from flask.views import MethodView
from .. import db, app
from .models import Comment, Image, Video
from ..page.models import DeceasedPage
from ..user.models import User
from werkzeug import FileWrapper
from io import BytesIO

import datetime

comment_blueprint = Blueprint('comment', __name__)

class CommentView(MethodView):
    def get(self, id, page, desc):
        # getting max 10comments in a page

        path = current_app.config['hoster']
        per_page = 9
        items = {0: 'one', 1: 'two', 2: 'three', 3: 'four', 4: 'five', 5: 'six', 6: 'seven', 7: 'eight', 8: 'night',
                 9: 'ten'}
        if desc == 'false':
            comment = db.session.query(Comment, User).join(User).filter(Comment.page_id == id). \
                order_by(Comment.creating_date.asc()).paginate(page, per_page, error_out=False)
        else:
            comment = db.session.query(Comment, User).join(User).filter(Comment.page_id == id). \
                order_by(Comment.creating_date.desc()).paginate(page, per_page, error_out=False)

        try:
            response = {}
            for i in range(len(comment.items)):
                images = Image.query.filter(Image.comment_id == comment.items[i].Comment.id).all()
                images_list = []
                for a in range(len(images)):
                    images_list.append(path + 'GetCommentImage/' + str(images[a].id))
                videos = Video.query.filter(Video.comment_id == comment.items[i].Comment.id).all()
                Videos_list = []
                for b in range(len(videos)):
                    Videos_list.append(videos[b].url)

                response.update({
                    items[i]: {
                        'id': comment.items[i].Comment.id,
                        'content': comment.items[i].Comment.content,
                        'creating_date': pretty_date(comment.items[i].Comment.creating_date),
                        'page_id': comment.items[i].Comment.page_id,
                        'username': comment.items[i].User.username,
                        'next_num': comment.has_next,
                        'prev_num': comment.prev_num,
                        'images_url': images_list,
                        'video': Videos_list
                    }
                })
            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500

    def post(self):
        #add a new comment record.
        page_id = request.form.get('page_id')
        content = request.form.get('content')
        exit_page = DeceasedPage.query.filter(DeceasedPage.id == page_id).first()
        creating_date = datetime.datetime.now()
        access_token = request.form.get('Authorization')
        if exit_page and access_token != 'undefined':
            user_id = User.decode_token(access_token)
            user = User.query.filter_by(id=user_id).first()
            print(user_id)
            if user_id != 'Invalid token. Please register or login' or 'Expired token. Please login to get a new token':
                comment = Comment(content, page_id, creating_date, user_id)
                db.session.add(comment)
                db.session.commit()
                db.session.flush()
                db.session.refresh(comment)

                response = {
                    'message': 'successfully.',
                    'page_id': comment.page_id,
                    'content': comment.content,
                    'id': comment.id,
                    'create_date': comment.creating_date,
                    'username': user.username
                }
                return make_response(jsonify(response)), 200
            else:
                response = {
                    'message': user_id,
                }
                return make_response(jsonify(response)), 500
        else:
            response = {
                'message': 'have no this page id.',
            }
            return make_response(jsonify(response)), 500


class CommentImageView(MethodView):
    def get(self, id):
        #getting a info of image by comment id.
        image = Image.query.filter(Image.id == id).first()
        b = BytesIO(image.image)
        w = FileWrapper(b)
        return Response(w, mimetype='image/jpeg', direct_passthrough=True)

    def post(self):
        #add a image in a comment
        comment_id = request.form.get('comment_id')
        image = request.files['image'].read()
        comment = Image(image, comment_id)
        db.session.add(comment)
        db.session.commit()
        db.session.flush()
        db.session.refresh(comment)
        response = {'message': 'pass'}
        return make_response(jsonify(response)), 200


class CommentVideoView(MethodView):
    def post(self):
        #add info of youtube video into database
        comment_id = request.form.get('comment_id')
        url = request.form.get('url')
        comment = Video(url, comment_id)
        db.session.add(comment)
        db.session.commit()
        db.session.flush()
        db.session.refresh(comment)
        response = {'message': 'pass'}
        return make_response(jsonify(response)), 200


def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    from datetime import datetime
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 60:
            return "just now"
        if second_diff < 120:
            return "a min ago"
        if second_diff < 3600:
            return str(int(second_diff / 60)) + " mins ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(int(second_diff / 3600)) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(int(day_diff)) + " days ago"
    if day_diff < 31:
        return str(int(day_diff / 7)) + " weeks ago"
    if day_diff < 365:
        return str(int(day_diff / 30)) + " mons ago"
    return str(int(day_diff / 365)) + " years ago"


Comment_View = CommentView.as_view('Comment_View')
Comment_Image_View = CommentImageView.as_view('Comment_Image_View')
Comment_Video_View = CommentVideoView.as_view('Comment_Video_View')

app.add_url_rule(
    '/CraeteComment', view_func=Comment_View, methods=['POST']
)
app.add_url_rule(
    '/CraeteCommentImage', view_func=Comment_Image_View, methods=['POST']
)
app.add_url_rule(
    '/GetCommentImage/<id>', view_func=Comment_Image_View, methods=['Get']
)
app.add_url_rule(
    '/CraeteCommentVideo', view_func=Comment_Video_View, methods=['POST']
)
app.add_url_rule(
    '/GetComment/<int:id>/<int:page>/<desc>', view_func=Comment_View, methods=['GET']
)
