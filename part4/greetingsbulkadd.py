"""Part 3 of the training session."""
import webapp2
import greetingsgen
import logging

from google.appengine.api import taskqueue
from google.appengine.api import users
from google.appengine.ext import ndb

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
  return ndb.Key('Guestbook', guestbook_name)



class Greeting(ndb.Model):
  author = ndb.UserProperty()
  content = ndb.StringProperty(indexed=False)
  date = ndb.DateTimeProperty(auto_now_add=True)

class AddTasksToQueue(webapp2.RequestHandler):

  def get(self):
    # add tasks
    q = taskqueue.Queue('pull-queue')
    tasks = []
    for x in range(0, 100):
      payload_str = 'hello world %s'% x
      tasks.append(taskqueue.Task(payload=payload_str, method='PULL'))
    logging.error(tasks)
    q.add(tasks)
    

class LeaseTasks(webapp2.RequestHandler):

  def get(self):
    # add tasks
    q = taskqueue.Queue('pull-queue')
    tasks = []
    
    #lease tasks
    tasks = q.lease_tasks(3600, 100)
    for t in tasks:
      logging.info('Processing task')
      (guestbook_name, greeting_content) = greetingsgen.GenGreetings()
      greeting = Greeting(parent=guestbook_key(guestbook_name))

      if users.get_current_user():
        greeting.author = users.get_current_user()

      greeting.content = greeting_content
      greeting.put()

      q.delete_tasks(t)



application = webapp2.WSGIApplication([
    ('/generate-greetings/lease.*', LeaseTasks),
    ('/generate-greetings/addtasks.*', AddTasksToQueue),
], debug=True)

