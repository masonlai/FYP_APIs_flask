from .. import db, SECRET_KEY
import jwt
import datetime
from datetime import timedelta
from sqlalchemy.orm import relationship


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    religion = db.Column(db.String(20), nullable=False)
    comment = relationship("Comment")
    VisitRecord = relationship("VisitRecord")
    Page = relationship('DeceasedPage')

    def __init__(self, username, password, email, religion):
        self.username = username
        self.password = password
        self.email = email
        self.religion = religion

    def generate_token(self, user_id):
        """ Generates the access token"""

        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.datetime.now() + timedelta(minutes=10),
                'iat': datetime.datetime.now(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                SECRET_KEY,
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, SECRET_KEY)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login"

