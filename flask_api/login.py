from flask import jsonify, request, current_app, url_for, g
from flask.views import MethodView

class login(MethodView):
    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')
        check_username = account.query.filter_by(username=username).first()
        check_password = account.query.filter_by(password=password)
        if check_username is None or check_password is None:
            return jsonify({'code':400, 'message':'Either the username or pbn m  assword was invalid.'})

app.add_url_rule('/login', view_func=login.as_view('login'), methods=['POST'])