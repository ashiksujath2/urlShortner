import webapp2
from google.appengine.ext import db

class urlData(db.Model):
  longUrl = db.StringProperty()
  tinyUrl = db.StringProperty()
 
class MainPage(webapp2.RequestHandler):
  def get(self): 
    self.response.out.write('<html><body>')
    self.response.out.write("""
          <form action="/tiny" method="post">
            <div>Long Url: <input  name="longUrl"></div>
            <div><input type="submit" value="Shorten"></div>
          </form>
          </body>
      </html>""" )

def encode(string):
    return 'S'+string[5:7]+str(len(string))

class shorten(webapp2.RequestHandler):
  def post(self):
    host = self.request.url
    path = self.request.path
    urls = urlData()
    urls.longUrl = self.request.get('longUrl')
    urls.tinyUrl = encode(urls.longUrl)
    urls.put()
    url = host.replace(path[1:],urls.tinyUrl)
    self.response.out.write('<html><body>Short Url:  ')
    self.response.out.write("""<a href= %s> %s</a></body></html>""" %(url,url))
   
class urlmapper(webapp2.RequestHandler):
  def get(self):
    urls = urlData.all()
    res = urls.filter("tinyUrl =",self.request.path[1:]).get()
    self.redirect(str(res.longUrl))

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/tiny', shorten),
                               ('/S.*', urlmapper)],
                              debug=True)
