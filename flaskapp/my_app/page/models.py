from .. import db
from sqlalchemy.orm import relationship


class DeceasedPage(db.Model):
    __tablename__ = 'DeceasedPage'
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
    theme = db.Column(db.String(20), nullable=True)
    personal_theme = db.Column(db.Binary, nullable=True)
    creating_date = db.Column(db.DateTime, nullable=False)
    comment = relationship("Comment")
    background_music = db.Column(db.Binary, nullable=True)
    VisitRecord = relationship("VisitRecord")

    def __init__(self, first_name, last_name, gender, date_of_birth, date_of_death, place_of_birth,
                 nationality, life_profile, portrait, portrait_position, theme, personal_theme, creating_date,
                 background_music=None):
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
        self.personal_theme = personal_theme
        self.creating_date = creating_date
        self.background_music = background_music
