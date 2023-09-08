""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json
from sqlalchemy.exc import IntegrityError

from __init__ import app, db

class Player(db.Model):
    __tableuser__ = 'players'  # table user is plural, class user is singular

    # Define the Player schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _user = db.Column(db.String(255), unique=False, nullable=False)
    _score = db.Column(db.Integer)    

    # constructor of a Player object, initializes the instance variables within object (self)
    def __init__(self, user, score):
        self._user = user    # variables with self prefix become part of the object, 
        self._score = score

    # a user getter method, extracts user from object
    @property
    def user(self):
        return self._user
    
    # a setter function, allows user to be updated after initial object creation
    @user.setter
    def user(self, user):
        self._user = user
        
    
    @property
    def password(self):
        return self._password[0:10] + "..." # because of security only show 1st characters

    # dob property is returned as string, to avoid unfriendly outcomes
    @property
    def score(self):
        return self._score
    
    # dob should be have verification for type date
    @score.setter
    def score(self, score):
        self._score = score

    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a player object from Player(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "user": self.user,
            "score": self.score,
        }

    # CRUD update: updates user, uid, password, score
    # returns self
    def update(self, dictionary):
        """only updates values in dictionary with length"""
        for key in dictionary:
            if key == "user":
                self.user = dictionary[key]
            if key == "score":
                self.score = dictionary[key]
        db.session.commit()
        return self

    # CRUD delete: remove self
    # return self
    def delete(self):
        player = self
        db.session.delete(self)
        db.session.commit()
        return player


"""Database Creation and Testing """

# Builds working data for testing
def initPlayers():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester records for table"""
        players = [
            Player(user='John Doe', score=25),
            Player(user='Jane Doe', score=30),
        ]

        """Builds sample user/note(s) data"""
        for player in players:
            try:
                player.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {player.user}")