import random

#inspiration from : 
PEOPLE = [
    "Matthew", "Mark", "Luke", "John", "Romeo", "Juliet",
    "Simon", "everyone", "the hen", "the duck", "your mother",
    "my wife", "the king", "the knight", "his highness", "Jim",
    "Mr. Icke", "the goose", "Rene", "Webdriver Torso", "the BBC",
    "A858DE45F56D9BC9", "the Eagle", "the Copper Eye", "our friend",
]

PLACES = [
    "France", "Mars", "the Moon", "Home", "Switzerland", "South Africa",
    "the palace", "the Eiffel Tower", "Downing Street", "the White House",
    "the Nest", "the Portal", "Hades", "Google",
]

THINGS = [
    "cookie", "book", "pen", "glass", "phone", "bowl", "egg", "clock",
    "loaf", "coin", "document", "device", "scepter", "message",
    "computer", "signal", "box", "transmission", "laser",
]

PHRASES = [
    "%(person)s : It has been a long day and i am tired. Thanks for everything",
    "%(person)s : Merci pour tout !!!!",
    "%(person)s bronze is a metal, is it called an alloy?",
    "%(person)s knows about the %(thing)s",
    "App Engine %(thing)s was raised in  %(place)s",
    "Send the %(thing)s to %(person)s",
    "%(person)s has eaten the %(thing)s",
    "The %(thing)s is in %(place)s",
    "%(place)s is lovely at this time of year",
    "%(person)s has lost the %(thing)s",
    "%(person)s must know about the %(thing)s",
    "the %(thing)s for %(person)s in %(place)s",
    "the incident in %(place)s is known to %(person)s",
    "you cannot trust %(person)s, not in %(place)s",
    "%(person)s snuck into %(place)s last night",
    "the best %(thing)s is to be found in %(place)s",
    "the %(thing)s is still in %(place)s",
    "%(person)s left the %(thing)s in %(place)s",
    "contact %(person)s and ask about the %(thing)s",
    "execute the %(thing)s protocol",
    "the %(thing)s is in play",
    "lightning is striking in %(place)s",
]


def GenGreetings():
  phrase = random.choice(PHRASES)
  place = random.choice(PLACES)
  greeting = phrase % {
      "person": random.choice(PEOPLE),
      "place": place,
      "thing": random.choice(THINGS),
  }
  guestbook = place
  return (guestbook, greeting)



