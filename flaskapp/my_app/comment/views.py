from flask import request, jsonify, Blueprint, make_response
from flask.views import MethodView
from .. import db, app
from .models import Comment
from ..page.models import DeceasedPage
from ..user.models import User
import datetime

comment_blueprint = Blueprint('comment', __name__)


class CommentView(MethodView):
    def get(self, id, page, desc):
        per_page = 9
        items = {0: 'one', 1: 'two', 2: 'three', 3: 'four', 4: 'five', 5: 'six', 6: 'seven', 7: 'eight', 8: 'night',
                 9: 'ten'}

        if desc == 'false':
            comment = db.session.query(Comment, User).join(User).filter(Comment.page_id == id).\
                order_by(Comment.creating_date.asc()).paginate(page, per_page,error_out=False)
        else:
            comment = db.session.query(Comment, User).join(User).filter(Comment.page_id == id).\
                order_by(Comment.creating_date.desc()).paginate(page, per_page,error_out=False)

        try:
            response = {}
            for i in range(len(comment.items)):
                response.update({
                    items[i]: {
                        'id': comment.items[i].Comment.id,
                        'content': comment.items[i].Comment.content,
                        'creating_date': comment.items[i].Comment.creating_date,
                        'page_id': comment.items[i].Comment.page_id,
                        'username': comment.items[i].User.username,
                        'next_num': comment.has_next,
                        'prev_num': comment.prev_num,
                    }
                })
            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500

    def post(self):
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
                    'username':user.username
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


Comment_View = CommentView.as_view('Comment_View')

app.add_url_rule(
    '/CraeteComment', view_func=Comment_View, methods=['POST']
)
app.add_url_rule(
    '/GetComment/<int:id>/<int:page>/<desc>', view_func=Comment_View, methods=['GET']
)
