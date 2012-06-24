import re
import urllib2
from django.http import HttpResponse, HttpResponseRedirect

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
