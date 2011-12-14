#!/usr/bin/env python2

from google.appengine.ext import db

class Conflict(db.Model):
    """
    A Burning Wheel scripted conflict
    """
    ready = db.BooleanProperty(False)
    description = db.TextProperty()

    @classmethod
    def new(cls):
        """
        Factory method for making Conflicts.

        This calls .put() on the created object

        It's not recommended to override __init__ on db.Model subclasses.
        Ref: http://stackoverflow.com/a/3280270/350351
        """
        conflict = cls()
        conflict.put()
        Exchange.new(conflict=conflict, exchange_number=1)
        return conflict

    @property
    def sorted_exchanges(self):
        return sorted(self.exchanges, key=lambda e: e.exchange_number)

class Exchange(db.Model):
    """
    One exchange in a scripted conflict
    """
    conflict = db.ReferenceProperty(Conflict, collection_name="exchanges")
    exchange_number = db.IntegerProperty
    ready = db.BooleanProperty(False)

    @classmethod
    def new(cls, **kwargs):
        exchange = cls(**kwargs)
        exchange.put()
        for i in xrange(1, 4):
            volley = Volley(exchange=exchange,
                            volley_number=i)
            volley.put()

        return exchange

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
    intent = db.TextProperty()
    finalized = db.BooleanProperty(False)
