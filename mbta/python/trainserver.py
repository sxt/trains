#!/usr/bin/python
from twisted.internet import reactor
from twisted.web import proxy, server
from twisted.web.static import File
from twisted.web.resource import Resource
import ConfigParser
from sslproxy import SSLReverseProxyResource

config = ConfigParser.ConfigParser()
config.read('cfg/train.cfg')

wwwroot = config.get('properties', 'wwwroot')
mbta_url = config.get('properties', 'mbta_url')
mq_url = config.get('properties', 'mq_url')

fileResource = File(wwwroot)
mbtaProxyResource = proxy.ReverseProxyResource(mbta_url, 80, '')
ironmqProxyResource = SSLReverseProxyResource(mq_url, 443, '')
rootResource = Resource()

rootResource.putChild("mbta", mbtaProxyResource)
rootResource.putChild("mq", ironmqProxyResource)
rootResource.putChild("local", fileResource)

site = server.Site(rootResource)
reactor.listenTCP(8080, site)
reactor.run()

