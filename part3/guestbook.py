"""Part 2 of the training session."""
import datetime
import logging
import os

import jinja2
import webapp2

from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.ext import ndb


# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.


DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
  return ndb.Key('Guestbook', guestbook_name)


def get_user_login_url(request):
  if users.get_current_user():
    url = users.create_logout_url(request.uri)
    url_linktext = 'Logout'
  else:
    url = users.create_login_url(request.uri)
    url_linktext = 'Login'
  return (url, url_linktext)


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Greeting(ndb.Model):
  author = ndb.UserProperty()
  content = ndb.StringProperty(indexed=False)
  date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):

  def get(self):
    guestbook_name = self.request.get('guestbook',
                                      DEFAULT_GUESTBOOK_NAME)
    greetings_query = Greeting.query(
        ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
    greetings = greetings_query.fetch(10)

    # 3. Bonus. Save in memcache the 10 entries
    greetings = memcache.get('%s:greetings' % guestbook_name)
    if greetings is None:
      logging.error('Not in memcache, caching')
      greetings_query = Greeting.query(
          ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
      greetings = greetings_query.fetch(10)
      if not memcache.add('%s:greetings' % guestbook_name, greetings, 10):
        logging.error('Memcache set failed.')

    counter_date_id = '%s:counter_date'%guestbook_name
    counter_value_id = '%s:counter'%guestbook_name

    # 2. Memcache the counter
    counter_value = memcache.incr(counter_value_id, initial_value=0)
    counter_date = memcache.get(counter_date_id)

    if (counter_value == 1) or (counter_date is None):
      memcache.set(counter_date_id, datetime.datetime.now())
      counter_date = memcache.get(counter_date_id)

    # 1. refactored url generated for convenience
    (url, url_linktext) = get_user_login_url(self.request)

    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render(greetings=greetings,
                                            url=url,
                                            url_linktext=url_linktext,
                                            guestbook_name=guestbook_name,
                                            counter_value=counter_value,
                                            counter_date=counter_date))


class DetailGuestbookEntry(webapp2.RequestHandler):

  def get(self):
    try:
      urlsafe_keystr = self.request.get('uid')
      # 1. generate a Key based on the UID
      rev_key = ndb.Key(urlsafe=urlsafe_keystr)
      # 1. get a key based on the key
      entry = rev_key.get()

      # 1.refactored url generated for convenience
      (url, url_linktext) = get_user_login_url(self.request)
      # 1. Set template to entry.html and send the greeting as an entry
      template = jinja_environment.get_template('entry.html')
      self.response.out.write(template.render(greeting=entry,
                                              url=url,
                                              url_linktext=url_linktext))
    except TypeError:
      logging.error('Error fetching entity. UrlSafe : %s', urlsafe_keystr)
      self.response.status = '404 Not Found'
      self.response.content_type = 'text/plain'
      self.response.write('Invalid uid. Greeting Not Found')


class Guestbook(webapp2.RequestHandler):

  def post(self):
    guestbook_name = self.request.get('guestbook', DEFAULT_GUESTBOOK_NAME)
    greeting = Greeting(parent=guestbook_key(guestbook_name))

    if users.get_current_user():
      greeting.author = users.get_current_user()

    greeting.content = self.request.get('content')
    greeting.put()

    # 3. Bonus, we delete the cache related to this
    memcache.delete('%s:greetings' % guestbook_name)

    self.redirect('/?guestbook='+guestbook_name)

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook),
    # 1. Add entry handler
    ('/entry', DetailGuestbookEntry),
], debug=True)
