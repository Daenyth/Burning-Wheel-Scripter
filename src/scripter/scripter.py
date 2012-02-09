#!/usr/bin/env python2

import os
import sys

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from conflict import Conflict, Character

class MainPage(webapp.RequestHandler):
    html_path = os.path.join(os.path.dirname(__file__), 'index.html')
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
        template_values = {'user': user}
        self.response.out.write(template.render(self.html_path, template_values))

class ConflictPage(webapp.RequestHandler):
    def get(self):
        conflict_id = self.request.get("conflict_id")
        if not conflict_id:
            # TODO: Add overview page
            print "lolfukt"
            return

        try:
            conflict = Conflict.get_by_id(int(conflict_id))
            if conflict is None:
                raise RuntimeError("Can't find Conflict")
        except StandardError:
            self.error(404)
            return

        if all(char.finalized for char in conflict.characters):
            conflict.ready = True

        html_page = 'run_conflict.html' if conflict.ready else 'create_conflict.html'

        html_path = os.path.join(os.path.dirname(__file__), html_page)
        template_values = {'conflict': conflict}
        self.response.out.write(template.render(html_path, template_values))

    def post(self):
        """
        Create a new conflict
        """
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))

        conflict = Conflict.new()
        Character(user=user, conflict=conflict).put()

        html_path = os.path.join(os.path.dirname(__file__), 'create_conflict.html')
        template_values = {'conflict': conflict}
        self.response.out.write(template.render(html_path, template_values))

class CharacterPage(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))

        conflict_id = self.request.get("conflict_id")
        try:
            conflict = Conflict.get_by_id(int(conflict_id))
        except (db.BadKeyError, StandardError) as e:
            self.error(500)
            print >>sys.stderr, str(e)
            return

        char = Character.gql("WHERE user = :1 AND conflict = :2",
                             user, conflict).get()

        if char is None:
            char = Character(user=user, conflict=conflict)

        if not char.finalized:
            char.name = self.request.get("char_name")
            char.intent = self.request.get("intent")
            char.finalized = True
            char.put()
        self.redirect('/conflict?conflict_id=%s' % conflict_id)

class VolleyPage(webapp.RequestHandler):
    def post(self):
        raise NotImplementedError

class CharacterActionPage(webapp.RequestHandler):
    def post(self):
        raise NotImplementedError

application = webapp.WSGIApplication([('/', MainPage),
                                      ('/conflict', ConflictPage),
                                      ('/character', CharacterPage),
                                      ('/volley', VolleyPage),
                                      ('/char_action', CharacterActionPage),
                                     ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

