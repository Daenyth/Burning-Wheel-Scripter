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
    exchange_number = db.IntegerProperty(required=True)
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

    @property
    def sorted_volleys(self):
        return sorted(self.volleys, key=lambda v: v.volley_number)

class Volley(db.Model):
    """
    One volley in an exchange
    """
    volley_number = db.IntegerProperty(required=True)
    exchange = db.ReferenceProperty(Exchange, collection_name="volleys",
                                    required=True)
    # For DoW this is fine, but for Fight! I need to figure out the best way to
    # handle 3 actions
    total_actions = db.IntegerProperty(1)
    ready = db.BooleanProperty(False)

class VolleyAction(db.Model):
    """
    One set of actions in a volley
    """
    volley = db.ReferenceProperty(Volley, collection_name="actions",
                                  required=True)
    action_number = db.IntegerProperty(required=True)
    ready = db.BooleanProperty(False)

class Character(db.Model):
    """
    One character involved in a scripted conflict
    """
    conflict = db.ReferenceProperty(Conflict, collection_name="characters")
    name = db.StringProperty(default='')
    password = db.StringProperty()
    intent = db.TextProperty()
    finalized = db.BooleanProperty(False)

class CharacterAction(db.Model):
    """
    One action from a specific character in a volley
    """
    volley_action = db.ReferenceProperty(VolleyAction,
                                         collection_name="char_actions",
                                         required=True)
    character = db.ReferenceProperty(Character, required=True)
    description = db.TextProperty()
    finalized = db.BooleanProperty(False)

