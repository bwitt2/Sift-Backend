'''

Sift 2015
Brandon Witt, Connor Giles
Google App Engine Endpoints

'''

from google.appengine.ext import endpoints
from google.appengine.ext import ndb
from google.appengine.api.logservice import logservice  #logging.info()
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from pyteaser import SummarizeUrl
import feedparser
import logging
import datetime

# ------------------------------------
#          ARTICLE MESSAGE
# ------------------------------------

class Article(messages.Message):
  title = messages.StringField(1, required = True)
  author = messages.StringField(2, required = True)
  published = messages.StringField(3, required = True)
  published_timestamp = messages.IntegerField(4, required = True)
  image_url = messages.StringField(5, required = True)
  publication = messages.StringField(6, required = True)
  summarized_article = messages.StringField(7, repeated = True)
  full_article = messages.StringField(8, required = True)
  upvotes = messages.IntegerField(9, required = True)
  upvoted_by_user = messages.BooleanField(10, required = True)

# ------------------------------------
#       ARTICLE REQUEST MESSAGE
# ------------------------------------

class ArticleRequest(messages.Message): 
  num_of_articles = messages.IntegerField(1, required = True)
  current_article_timestamp = messages.IntegerField(2, required = True)
  user_id = messages.StringField(3, required = True)

# ------------------------------------
#       ARTICLE RESPONSE MESSAGE
# ------------------------------------

class ArticleResponse(messages.Message):
  articles = messages.MessageField(Article, 1, repeated = True)

# ------------------------------------
#       UPVOTE REQUEST MESSAGE
# ------------------------------------

class UpvoteRequest(messages.Message):
  article_title = messages.StringField(1, required = True)
  user_id = messages.StringField(2, required = True)

# ------------------------------------
#       UPVOTE RESPONSE MESSAGE
# ------------------------------------

class UpvoteResponse(messages.Message):
  article_upvotes = messages.IntegerField(1, required = True)

# ------------------------------------
#         ARTICLE NDB MODEL
# ------------------------------------

class ArticleModel(ndb.Model):
  title = ndb.StringProperty(required = True)
  author = ndb.StringProperty(required = True)
  published = ndb.StringProperty(required = True)
  published_timestamp = ndb.IntegerProperty(required = True)
  image_url = ndb.StringProperty(required = True)
  publication = ndb.StringProperty(required = True)
  summarized_article = ndb.StringProperty(indexed = False, repeated = True)
  full_article = ndb.StringProperty(indexed = False, required = True)
  upvotes = ndb.IntegerProperty(required = True)
  upvoters = ndb.StringProperty(repeated = True)

# ------------------------------------
#               SIFT API
# ------------------------------------

@endpoints.api(name='sift', version='v1', description='API for sift')
class SiftApi(remote.Service):

# ------------------------------------
#         GET ARTICLES METHOD
# ------------------------------------

    @endpoints.method(ArticleRequest,
                      ArticleResponse,
                      name='SiftApi.getArticles', 
                      path='SiftApi/getArticles', 
                      http_method='POST')
    def getArticles(self, request):

      articles_query = None
      voted = False

      if request.num_of_articles > 0:
        
        articles_query = ArticleModel.query( ArticleModel.published_timestamp > request.current_article_timestamp).order(ArticleModel.published_timestamp).fetch(request.num_of_articles)
        logging.info("num: " + str(len(articles_query)) + " request.num: " + str(request.num_of_articles))
      
      else:
        
        articles_query = ArticleModel.query( ArticleModel.published_timestamp < request.current_article_timestamp).order(-ArticleModel.published_timestamp).fetch(abs(request.num_of_articles))
        logging.info("num: " + str(len(articles_query)) + " request.num: " + str(abs(request.num_of_articles)))

      articles = []
      
      for a in articles_query: 
        
        for voter in a.upvoters: 
          
          if voter == request.user_id:
            voted = True
            break

        articles.append(Article(title = a.title,
                                author = a.author,
                                published = a.published,
                                published_timestamp = a.published_timestamp,
                                image_url = a.image_url,
                                publication = a.publication,
                                summarized_article = a.summarized_article,
                                full_article = a.full_article,
                                upvotes = a.upvotes,
                                upvoted_by_user = voted
                        )       )
        voted = False

      return ArticleResponse(articles = articles)

# ------------------------------------
#         UPVOTE ARTICLE METHOD
# ------------------------------------

    @endpoints.method(UpvoteRequest,
                      UpvoteResponse,
                      name='SiftApi.upvote', 
                      path='SiftApi/upvote', 
                      http_method='POST')
    def upvote(self, request):
      
      try:
        article = ArticleModel.query( ArticleModel.title == request.article_title).fetch(1)[0]
      except:
        return UpvoteResponse(article_upvotes = -1)

      article.upvoters.append(request.user_id)
      article.upvotes = article.upvotes + 1
      article.put()

      return UpvoteResponse(article_upvotes = article.upvotes)

application = endpoints.api_server([SiftApi])
