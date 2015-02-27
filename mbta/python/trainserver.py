#!/usr/bin/python
from twisted.internet import reactor
from twisted.web import proxy, server
from twisted.web.static import File
from twisted.web.resource import Resource
import ConfigParser
from sslproxy import SSLReverseProxyResource
import os

wwwroot = os.environ.get('wwwroot')
mbta_host = os.environ.get('mbta_host')
mq_host = os.environ.get('mq_host')
mq_path = os.environ.get('mq_path')

print mq_path

fileResource = File(wwwroot)
mbtaProxyResource = proxy.ReverseProxyResource(mbta_host, 80, '')
ironmqProxyResource = SSLReverseProxyResource(mq_host, 443, mq_path)
rootResource = Resource()

rootResource.putChild("mbta", mbtaProxyResource)
rootResource.putChild("mq", ironmqProxyResource)
rootResource.putChild("local", fileResource)

site = server.Site(rootResource)
reactor.listenTCP(8080, site)
reactor.run()

