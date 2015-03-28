import webapp2

from google.appengine.ext import endpoints
from google.appengine.ext import ndb
from google.appengine.api.logservice import logservice  #logging.info()
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from pyteaser import SummarizeUrl
from pyteaser import grab_link
import feedparser
import logging
import datetime


# ------------------------------------
#           GLOBAL CONSTANTS
# ------------------------------------

FORMAT = "%Y-%b-%d %H:%M:%S"

# ------------------------------------
#         ARTICLE NDB MODEL
# ------------------------------------

class ArticleModel(ndb.Model):
  title = ndb.StringProperty(required = True)
  author = ndb.StringProperty(required = True)
  published = ndb.StringProperty(required = True)
  published_timestamp = ndb.IntegerProperty(indexed = True)
  image_url = ndb.StringProperty(required = True)
  publication = ndb.StringProperty(required = True)
  summarized_article = ndb.StringProperty(indexed = False, repeated = True)
  full_article = ndb.StringProperty(indexed = False, required = True)

# ------------------------------------
#         STANDARDIZE DATETIME
# ------------------------------------

def standardize(format, dt):
    return datetime.datetime.strptime(str(dt), format)

# ------------------------------------
#            MAKE DATETIME
# ------------------------------------

def makeTimestamp(dt, epoch = datetime.datetime(1970,1,1)):
    return (dt - epoch).total_seconds()
'''
# ------------------------------------
#         ENTREPRENEUR METHOD
# ------------------------------------

def Entrepreneur(latest):
    url = "http://feeds.feedburner.com/entrepreneur/latest"
    feed = feedparser.parse(url)

    for item in feed["items"]:

      dt = standardize("%a, %d %b %Y %H:%M:%S GMT", item["published"])
      ts = makeTimestamp(this_latest_dt)

      if int(ts) > int(latest): # there are new articles

        ArticleModel(title = str(item["title"]), 
                     author = str(item["author"]),
                     published = dt,
                     published_timestamp = int(ts), 
                     image_url = str(item["media_content"][0]["url"]),
                     publication = "Entrepreneur",
                     summarized_article = 
                     )

      else: # there are no new articles
        return
'''
# ------------------------------------
#         TECH CRUNCH METHOD
# ------------------------------------

def TechCrunch(latest):
    logging.info("TECH CRUNCH CALLED")
    url = "http://feeds.feedburner.com/TechCrunch/"
    feed = feedparser.parse(url)

    for item in feed["items"]:

      dt = standardize("%a, %d %b %Y %H:%M:%S +0000", item["published"])
      ts = makeTimestamp(dt)

      if int(ts) > int(latest): # there are new articles
        sum_article = SummarizeUrl(item["links"][0]["href"])
        full_article = grab_link(item["links"][0]["href"]).cleaned_text

        #logging.info(full_article)
        
        ArticleModel(title = item["title"], 
                     author = item["author"],
                     published = str(dt),
                     published_timestamp = int(ts), 
                     image_url = str(item["media_content"][0]["url"]),
                     publication = "TechCrunch",
                     summarized_article = sum_article,
                     full_article = full_article
                     ).put()

        logging.info(item["title"] + " from TechCrunch has been stored")

      else: # there are no new articles
        return

# ------------------------------------
#           MEDIUM METHOD
# ------------------------------------

def Medium(latest):
    return

# ------------------------------------
#         FAST COMPANY METHOD
# ------------------------------------

def FastCompany(latest):
  logging.info("FAST COMPANY CALLED")
  url = "http://feeds.feedburner.com/fastcompany/headlines"
  feed = feedparser.parse(url)

  for item in feed["items"]:

    dt = standardize("%a, %d %b %Y %H:%M:%S GMT", item["published"])
    ts = makeTimestamp(dt)

    if int(ts) > int(latest): # there are new articles
        sum_article = SummarizeUrl(item["links"][0]["href"])
        full_article = grab_link(item["links"][0]["href"]).cleaned_text

        logging.info(full_article)
        
        ArticleModel(title = item["title"], 
                     author = item["author"],
                     published = str(dt),
                     published_timestamp = int(ts), 
                     image_url = str(item["media_content"][0]["url"]),
                     publication = "FastCompany",
                     summarized_article = sum_article,
                     full_article = full_article
                     ).put()

        logging.info(item["title"] + " from FastCompany has been stored")

    else: # there are no new articles
        return

# ------------------------------------
#         VENTURE BEAT METHOD
# ------------------------------------

def VentureBeat(latest):
  logging.info("VENTURE BEAT CALLED")
  url = "http://feeds.venturebeat.com/VentureBeat"
  feed = feedparser.parse(url)

  for item in feed["items"]:

      dt = standardize("%a, %d %b %Y %H:%M:%S GMT", item["published"])
      ts = makeTimestamp(dt)

      if int(ts) > int(latest): # there are new articles
        sum_article = SummarizeUrl(item["links"][0]["href"])
        full_article = grab_link(item["links"][0]["href"]).cleaned_text

        logging.info(full_article)
        
        ArticleModel(title = item["title"], 
                     author = item["author"],
                     published = str(dt),
                     published_timestamp = int(ts), 
                     image_url = str(item["links"][1]["href"].replace("resize", "")),
                     publication = "VentureBeat",
                     summarized_article = sum_article,
                     full_article = full_article
                     ).put()

        logging.info(item["title"] + " from VentureBeat has been stored")

      else: # there are no new articles
        return


# ------------------------------------
#         THE VERGE METHOD
# ------------------------------------

def TheVerge(latest):
  url = "http://www.theverge.com/rss/index.xml"
  feed = feedparser.parse(url)
  dt = 0

  for item in feed["items"]:
    try:
      dt = standardize("%Y-%m-%d %H:%M:%S-04:00", item["published"].replace("T", " "))
    except: 
      dt = standardize("%Y-%m-%d %H:%M:%S-4:00", item["published"].replace("T", " "))

    ts = makeTimestamp(dt)

    if int(ts) > int(latest): # there are new articles
        sum_article = SummarizeUrl(item["links"][0]["href"])
        full_article = grab_link(item["links"][0]["href"]).cleaned_text
        
        ArticleModel(title = item["title"], 
                     author = item["author"],
                     published = str(dt),
                     published_timestamp = int(ts), 
                     image_url = str(item["content"][0]["value"].split()[2][4:].replace('"', "")),
                     publication = "TheVerge",
                     summarized_article = sum_article,
                     full_article = full_article
                     ).put()

        logging.info(item["title"] + " from The Verge has been stored")

    else: # there are no new articles
        return

# ------------------------------------
#         GET ALL METHOD
# ------------------------------------

def getArticlesFromAllPublications(latest_article_timestamp):
  #Entrepreneur(latest_article_timestamp) # snot working
  TechCrunch(latest_article_timestamp) # DONE
  #Medium(latest_article_timestamp)
  FastCompany(latest_article_timestamp) # DONE
  VentureBeat(latest_article_timestamp) # DONE
  #TheVerge(latest_article_timestamp) # NOT USING, BUT DONE

# ------------------------------------
#       UPDATE ARTICLES WEBAPP2
# ------------------------------------

class UpdateArticles(webapp2.RequestHandler):
    def get(self):
      latest_article_timestamp = 0
      logging.info("IT HAS BEEN CALLLEDDDDDDD")
      try:
        latest_article = ArticleModel.query().order(-ArticleModel.published_timestamp).fetch(1)[0]
        latest_article_timestamp = latest_article.published_timestamp
      except:
         latest_article_timestamp = 0

      getArticlesFromAllPublications(latest_article_timestamp)

      self.response.headers['Content-Type'] = 'text/plain'
      self.response.write(latest_article_timestamp)

app = webapp2.WSGIApplication([('/tasks/updateArticles', UpdateArticles)], debug=True)



