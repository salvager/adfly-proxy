import re
import urllib2
import httplib
from socket import timeout
from django.http import HttpResponse, HttpResponseRedirect

def proxy (request, code) :
    try :
        response = urllib2.urlopen("http://adf.ly/%s" % code, timeout=5)
    except urllib2.URLError :
        return HttpResponse("Couldn't connect to adfly.", mimetype="text/plain", status=502)

    data = response.read()

    matches = re.search(r'var url = \'(.*?)\';', data)

    if matches is None :
        return HttpResponse("Invalid response from adfly.", mimetype="text/plain", status=502)

    gourl = matches.group(1)
    prefix = "https://adf.ly"

    # inconsistency is the spice of life
    if gourl.startswith(prefix) :
        gourl = gourl[len(prefix):]

    try :
        con = httplib.HTTPConnection("adf.ly", timeout=5)
        con.request("GET", gourl)
    except httplib.HTTPException :
        return HttpResponse("Couldn't connect adfly to get the destination of the /go/ url.", mimetype="text/plain", status=502)
    except timeout :
        return HttpResponse("Connection to adfly for the /go/ url timed out.", mimetype="text/plain", status=502)

    resp = con.getresponse()
    url = resp.getheader("Location")

    if resp.status != 302 or not url :
        return HttpResponse("Invalid /go/ response from adfly.", mimetype="text/plain", status=502)

    return HttpResponseRedirect(url)
