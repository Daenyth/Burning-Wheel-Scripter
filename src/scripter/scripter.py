#!/usr/bin/env python2

import os

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from conflict import Conflict, Character

class MainPage(webapp.RequestHandler):
    html_path = os.path.join(os.path.dirname(__file__), 'index.html')
    def get(self):
        template_values = {}
        self.response.out.write(template.render(self.html_path, template_values))

class ConflictPage(webapp.RequestHandler):
    def get(self):
        conflict_id = self.request.get("conflict_id")
        if not conflict_id:
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
        char_count = int(self.request.get('character_count'))
        conflict = Conflict.new()
        for i in xrange(char_count):
            Character(name="", intent="", conflict=conflict).put()

        html_path = os.path.join(os.path.dirname(__file__), 'create_conflict.html')
        template_values = {'conflict': conflict}
        self.response.out.write(template.render(html_path, template_values))

class CharacterPage(webapp.RequestHandler):
    def post(self):
        char = db.get(self.request.get("character_id"))
        if not char.finalized:
            char.name = self.request.get("char_name")
            char.password = self.request.get("char_password")
            char.intent = self.request.get("intent")
            char.finalized = True
            char.put()
        self.redirect('/conflict?conflict_id=%s' %
                      self.request.get("conflict_id"))

application = webapp.WSGIApplication([('/', MainPage),
                                      ('/conflict', ConflictPage),
                                      ('/character', CharacterPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

