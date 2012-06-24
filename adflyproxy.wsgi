# I realize that the way I'm doing this is non-standard.

import re
import urllib2

# for compatibility with django view
class HttpResponse (object) :
    def __init__ (self, content = "", mimetype = None, status = 200) :
        self.content = content
        self.status = status
        self.mimetype = mimetype

    def construct (self) :
        descriptions = {
            502 : "Bad Gateway",
            400 : "Bad Request",
            200 : "OK",
        }

        return self.content, (
            # Status
            "%s %s" % (str(self.status), descriptions[self.status]), 
            # Other headers
            [("Content-type", self.mimetype), ("Content-Length", str(len(self.content)))]
        )
        
class HttpResponseRedirect (object) :
    def __init__ (self, where) :
        self.where = where

    def construct (self) :
        # Is the empty string neccessary?
        return "", ("302 Found", [("Location", self.where)])
      
# ripped right out of the django app's views!       
def proxy (request, code) :
    try :
        response = urllib2.urlopen("http://adf.ly/%s" % code)
    except urllib2.URLError :
        return HttpResponse("Couldn't connect to adfly.", mimetype="text/plain", status=502)

    data = response.read()

    matches = re.search(r'var url = \'(.*?)\';', data)

    if matches is None :
        return HttpResponse("Invalid response from adfly.", mimetype="text/plain", status=502)

    url = "http://adf.ly" + matches.group(1)

    return HttpResponseRedirect(url)

 
def application (environ, start_response) :
    code = environ["REQUEST_URI"][len(environ["SCRIPT_NAME"])+1:]
    if re.match(r"[A-Za-z0-9]{5}", code) :
        output, params = proxy(None, code).construct()
    else :
        output, params = HttpResponse("You're calling this manually or you specified an invalid code.", mimetype="text/plain", status=400).construct()

    start_response(*params)

    return [output]
