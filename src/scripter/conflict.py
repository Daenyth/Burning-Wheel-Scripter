#!/usr/bin/env python2

from google.appengine.ext import db

class Conflict(db.Model):
    """
    A Burning Wheel scripted conflict
    """
    def __init__(self, character_count):
        """
        Initialize a conflict

        character_count: The number of characters involved in the conflict
        """
        self.exchanges = db.ListProperty(Exchange, [db.ReferenceProperty(Exchange)])
        self.characters = db.ListProperty(Character)
        for char in xrange(character_count):
            self.characters.append(db.ReferenceProperty(Character))

class Exchange(db.Model):
    """
    One exchange in a scripted conflict
    """
    def __init__(self):
        """
        Initialize an exchange
        """
        volley = db.ReferenceProperty(Volley)
        self.volleys = db.ListProperty(Volley, [volley, volley, volley])
        self.ready = db.BooleanProperty(False)

class Volley(db.Model):
    """
    One volley in an exchange
    """
    pass

class Character(db.Model):
    """
    One character involved in a scripted conflict
    """
    def __init__(self, name=None):
        self.name = db.StringProperty(name)
        self.password = db.StringProperty()
        self.finalized = db.BooleanProperty(False)
