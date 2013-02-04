#
"""
Copied from twisted proxy. Provides ReversProxyResource that talks
to an SSL back end and a non-SSL front end
"""

from twisted.internet import reactor
from twisted.web import proxy, server
import urlparse
from urllib import quote as urlquote

from twisted.internet import reactor, ssl
from twisted.internet.protocol import ClientFactory
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
from twisted.web.http import HTTPClient, Request, HTTPChannel
from twisted.web.proxy import ProxyClientFactory

class SSLReverseProxyResource(Resource):
    """
    Resource that renders the results gotten from another server

    Put this resource in the tree to cause everything below it to be relayed
    to a different server.

    @ivar proxyClientFactoryClass: a proxy client factory class, used to create
    new connections.
    @type proxyClientFactoryClass: L{ClientFactory}

    @ivar reactor: the reactor used to create connections.
    @type reactor: object providing L{twisted.internet.interfaces.IReactorTCP}
    """

    proxyClientFactoryClass = ProxyClientFactory


    def __init__(self, host, port, path, reactor=reactor):
        """
        @param host: the host of the web server to proxy.
        @type host: C{str}

        @param port: the port of the web server to proxy.
        @type port: C{port}

        @param path: the base path to fetch data from. Note that you shouldn't
        put any trailing slashes in it, it will be added automatically in
        request. For example, if you put B{/foo}, a request on B{/bar} will
        be proxied to B{/foo/bar}.  Any required encoding of special
        characters (such as " " or "/") should have been done already.

        @type path: C{str}
        """
        Resource.__init__(self)
        self.host = host
        self.port = port
        self.path = path
        self.reactor = reactor


    def getChild(self, path, request):
        """
        Create and return a proxy resource with the same proxy configuration
        as this one, except that its path also contains the segment given by
        C{path} at the end.
        """
        return SSLReverseProxyResource(
            self.host, self.port, self.path + '/' + urlquote(path, safe=""))


    def render(self, request):
        """
        Render a request by forwarding it to the proxied server.
        """
        # RFC 2616 tells us that we can omit the port if it's the default port,
        # but we have to provide it otherwise
        if self.port == 80:
            host = self.host
        else:
            host = "%s:%d" % (self.host, self.port)
        request.received_headers['host'] = host
        request.content.seek(0, 0)
        qs = urlparse.urlparse(request.uri)[4]
        if qs:
            rest = self.path + '?' + qs
        else:
            rest = self.path
        clientFactory = self.proxyClientFactoryClass(
            request.method, rest, request.clientproto,
            request.getAllHeaders(), request.content.read(), request)
        self.reactor.connectSSL(self.host, self.port, clientFactory, ssl.ClientContextFactory())
        return NOT_DONE_YET
