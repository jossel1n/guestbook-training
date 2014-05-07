"""Part 3 of the training session."""
import webapp2

from google.appengine.api import memcache


class MainPage(webapp2.RequestHandler):

  def get(self):
    self.response.out.write('<html><body>')
    stats = memcache.get_stats()
    self.response.out.write('<b>Cache Hits:%s</b><br>' % stats['hits'])
    self.response.out.write('<b>Cache Misses%s</b><br><br>' %
                            stats['misses'])


application = webapp2.WSGIApplication([
    ('/.*', MainPage),
], debug=True)
