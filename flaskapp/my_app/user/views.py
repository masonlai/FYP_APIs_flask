from flask import request, jsonify, Blueprint
from flask.views import MethodView
from flask import make_response
from .. import db, app
from .models import User

user_blueprint = Blueprint('user', __name__)

class UserView(MethodView):

    def post(self):
        #sign up an account
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        religion = request.form.get('religion')
        exit_user = User.query.filter_by(username=username).first()
        if not exit_user:
            usr = User(username, password, email, religion)
            db.session.add(usr)
            db.session.commit()

            try:
                user = User.query.filter_by(username=username).first()
                access_token = user.generate_token(user.id)
                if access_token:
                    response = {
                        'message': 'You logged in and signed up successfully.',
                        'access_token': access_token.decode(),
                        'username': user.username,
                        'email': usr.email,
                        'religion': usr.religion
                    }
                    return make_response(jsonify(response)), 200

            except Exception as e:
                response = {
                    'message': str(e) + '1'
                }
                return make_response(jsonify(response)), 500
        else:
            response = {
                'message': 'User already exists. Please login.'
            }

            return jsonify(response)



class LoginView(MethodView):

    def post(self):
        #login function and error checking
        try:
            # Get the user object using their email (unique to every user)
            user = User.query.filter_by(username=request.form.get('username')).first()
            # Try to authenticate the found user using their password
            if user and user.password == request.form.get('password'):
                # Generate the access token. This will be used as the authorization header
                access_token = user.generate_token(user.id)
                if access_token:
                    response = {
                        'message': 'You logged in successfully.',
                        'access_token': access_token.decode(),
                        'username': user.username
                    }
                    return make_response(jsonify(response)), 200
            else:
                response = {
                    'message': 'Invalid email or password, Please try again'
                }
                return make_response(jsonify(response)), 401

        except Exception as e:
            response = {
                'message': str(e) + '1'
            }
            return make_response(jsonify(response)), 500



User_view = UserView.as_view('user_view')
Login_view = LoginView.as_view('login_view')

app.add_url_rule(
    '/registration', view_func=User_view, methods=['POST']
)

app.add_url_rule(
    '/login', view_func=Login_view, methods=['POST']
)

