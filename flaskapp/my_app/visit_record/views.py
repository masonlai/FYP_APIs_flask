from flask import request, jsonify, Blueprint, make_response, Response, current_app
from flask.views import MethodView
from .. import db, app
from .models import VisitRecord
from sqlalchemy import func, desc
from ..user.models import User
import datetime
from werkzeug import FileWrapper
from io import BytesIO
import os

visitRecord_blueprint = Blueprint('visit_record', __name__)

class visitRecordFlowerView(MethodView):
    def get(self, name):
        #show the flower
        flower = os.path.abspath(os.path.dirname(__file__)) + '/flowers/' + name
        with open(flower, "rb") as image:
            file = image.read()
            bytesLike = bytearray(file)
        b = BytesIO(bytesLike)
        w = FileWrapper(b)
        return Response(w, mimetype='image/jpeg', direct_passthrough=True)


class visitRecordView(MethodView):
    def get(self, id):
        #getting the visited record by page id
        path = current_app.config['hoster']
        record = db.session.query(VisitRecord, User, func.max(VisitRecord.creating_date)) \
            .join(User).filter(VisitRecord.user_id == User.id) \
            .filter(VisitRecord.page_id == id).group_by(VisitRecord.user_id).order_by(
            desc(func.max(VisitRecord.creating_date))).all()

        if len(record) != 0:
            response = {}
            for i in range(len(record)):
                response.update({
                    str(i): {
                        'username': record[i].User.username,
                        'date': record[i][2],
                        'flower_url': path + 'flower/' + record[i].VisitRecord.flower_name
                    }
                })
            return make_response(jsonify(response)), 200
        else:
            response = {
            }
            return make_response(jsonify(response)), 500

    def post(self):
        #If logined user using 'Floral tributes'. record that
        page_id = request.form.get('page_id')
        creating_date = datetime.datetime.now()
        access_token = request.form.get('Authorization')
        flower_name = request.form.get('flower_name')
        if access_token != 'undefined' and access_token != '' and access_token != None:
            user_id = User.decode_token(access_token)
            user = User.query.filter_by(id=user_id).first()
            if user_id != 'Invalid token. Please register or login' and user_id != 'Expired token. Please login to get a new token':
                record = VisitRecord(page_id, creating_date, user_id, flower_name)
                db.session.add(record)
                db.session.commit()
                db.session.flush()
                db.session.refresh(record)
                response = {
                    'message': 'successfully.',
                    'page_id': record.page_id,
                    'id': record.id,
                    'create_date': record.creating_date,
                    'username': user.username,
                    'flower_name': flower_name
                }
                return make_response(jsonify(response)), 200
            else:
                response = {
                    'message': user_id,
                }
                return make_response(jsonify(response)), 500
        else:
            response = {
                'message': 'have no token or pageid.',
            }
            return make_response(jsonify(response)), 500


visit_Recordt_View = visitRecordView.as_view('visit_Recordt_View')
visit_Record_Flower_View = visitRecordFlowerView.as_view('visit_Record_Flower_View')

app.add_url_rule(
    '/visitRecord', view_func=visit_Recordt_View, methods=['POST']
)

app.add_url_rule(
    '/flower/<name>', view_func=visit_Record_Flower_View, methods=['get']
)
app.add_url_rule(
    '/get_visitRecord/<int:id>', view_func=visit_Recordt_View, methods=['GET']
)
