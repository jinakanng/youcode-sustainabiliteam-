from . import db
from flask_login import UserMixin

from sqlalchemy.sql import func


# entries - to store & display past adventure / experiences

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # foreign key - relates to user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



# users - to login 

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    # relationship - relates to notes, allows  user to see all their notes (stores each note in a list)
    entries = db.relationship('Entry')


# user profiles - to see other's profile pages
# - many-to-one relationship (many user profiles are available to one user)

# past activities - so can leave comment, connect with who was at the activity, review gear, etc.


