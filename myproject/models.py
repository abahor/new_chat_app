from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from myproject import login, db


@login.user_loader
def load_user(user_id):
    return UsersModel.query.get(user_id)


# VolumeRelationship = db.Table(

# db.Column('SenderID', db.Integer, db.ForeignKey('Volumes.ID')),
# db.Column('ReceiverID', db.Integer, db.ForeignKey('Volumes.ID')),
# db.Column('message', db.Text, )
# )


class UsersModel(db.Model, UserMixin):
    __tablename__ = 'users'
    # __searchable__ = ['description']
    # __analyzer__ = StemmingAnalyzer()

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)

    address_city = db.Column(db.Text, )
    profile_pic = db.Column(db.String(64))
    last_time_logged_in = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, email, username, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def check_password(self, field):
        return check_password_hash(self.password, field)


class Rooms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uu = db.Column(db.String(36), unique=True)
    participant_one = db.Column(db.Integer, )
    participant_two = db.Column(db.Integer, )

    def __init__(self, participant_1, uui, participant_2):
        self.participant_two = participant_2
        self.participant_one = participant_1
        self.uu = uui


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    SenderID = db.Column(db.Integer, )
    ReceiverID = db.Column(db.Integer, )
    text = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, senderid, receiverid, text, timestamp):
        self.SenderID = senderid
        self.ReceiverID = receiverid
        self.text = text
        self.timestamp = timestamp
