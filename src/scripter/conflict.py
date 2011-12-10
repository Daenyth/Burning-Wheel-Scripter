#!/usr/bin/env python2

from google.appengine.ext import db

class Conflict(db.Model):
    """
    A Burning Wheel scripted conflict
    """
    ready = db.BooleanProperty(False)

class Exchange(db.Model):
    """
    One exchange in a scripted conflict
    """
    conflict = db.ReferenceProperty(Conflict, collection_name="exchanges")
    ready = db.BooleanProperty(False)

class Volley(db.Model):
    """
    One volley in an exchange
    """
    volley_number = db.IntegerProperty
    exchange = db.ReferenceProperty(Exchange, collection_name="volleys")

class Character(db.Model):
    """
    One character involved in a scripted conflict
    """
    conflict = db.ReferenceProperty(Conflict, collection_name="characters")
    name = db.StringProperty()
    password = db.StringProperty()
    finalized = db.BooleanProperty(False)
