from .. import db, SECRET_KEY
from sqlalchemy.orm import relationship
import jwt
import datetime
from datetime import timedelta


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    religion = db.Column(db.String(20), nullable=False)
    birthday = db.Column(db.DateTime)
    gender = db.Column(db.String(6))
    education = db.Column(db.String(20))

    def __init__(self, username, password, email, religion, birthday=None, gender=None, education=None):
        self.username = username
        self.password = password
        self.email = email
        self.religion = religion
        self.birthday = birthday
        self.gender = gender
        self.education = education

    def save(self):
        """Save a student to the database.
        This includes creating a new user and editing one.
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete a user from the database.
        """
        db.session.delete(self)
        db.session.commit()

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

    @staticmethod
    def isAdmin(request):
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[0]

        if access_token:
            # Attempt to decode the token and get the User ID
            user_id = User.decode_token(access_token)
            user = User.query.filter_by(id=user_id).first()
            if user.isAdmint == True:
                return True

    def __repr__(self):
        return '<username %s>' % self.username


class DeceasedPage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    date_of_death = db.Column(db.DateTime, nullable=False)
    place_of_birth = db.Column(db.String(20), nullable=False)
    nationality = db.Column(db.String(20), nullable=False)
    life_profile = db.Column(db.Text, nullable=False)
    portrait = db.Column(db.Binary, nullable=False)
    portrait_position = db.Column(db.String(15), nullable=False)
    theme = db.Column(db.Binary, nullable=False)
    creating_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, first_name, last_name, gender, date_of_birth, date_of_death \
                 , place_of_birth, nationality, life_profile, portrait, portrait_position, theme, creating_date):
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.date_of_death = date_of_death
        self.place_of_birth = place_of_birth
        self.nationality = nationality
        self.life_profile = life_profile
        self.portrait = portrait
        self.portrait_position = portrait_position
        self.theme = theme
        self.creating_date = creating_date

    def save(self):
        """Save a page to the database.
        This includes creating a new user and editing one.
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete a page from the database.
        """
        db.session.delete(self)
        db.session.commit()
