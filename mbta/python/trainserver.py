#!/usr/bin/python
from twisted.internet import reactor
from twisted.web import proxy, server
from twisted.web.static import File
from twisted.web.resource import Resource
from sslproxy import SSLReverseProxyResource
import os
import sys

wwwroot = os.environ.get('wwwroot')
mbta_host = os.environ.get('mbta_host')

fileResource = File(os.path.abspath(wwwroot))
print "*** wwwroot ***: " + os.path.abspath(wwwroot)
print os.listdir('.')
sys.stdout.flush()
mbtaProxyResource = SSLReverseProxyResource(mbta_host, 443, '')
rootResource = Resource()

rootResource.putChild("mbta", mbtaProxyResource)
rootResource.putChild("local", fileResource)

site = server.Site(rootResource)
port = int(os.environ.get("PORT", 8080))
reactor.listenTCP(port, site)
reactor.run()

