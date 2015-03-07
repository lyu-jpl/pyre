# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import time # to generate timestamps
# framework
import pyre
# my protocol
from .Language import Language
# and its default implementation
from .HTML import HTML


# declaration
class HTTP(pyre.component, implements=Language):
    """
    An HTTP compliant document renderer
    """


    # user configurable state
    encoding = pyre.properties.str(default='iso-8859-1')
    encoding.doc = 'the encoding for HTTP headers'

    html = Language(default=HTML)
    html.doc = 'the renderer of my payload'


    # public data
    version = 1,0 # my preferred protocol version


    # mill obligations
    @pyre.export
    def render(self, document, server, **kwds):
        """
        Render the document
        """
        # the string used to assemble the output
        splicer = '\r\n'
        # unpack
        code = document.code
        status = document.status
        headers = document.headers
        version = document.version
        encoding = document.encoding

        # decide which protocol to use
        protocol = self.version if self.version < version else version
        # the protocol version
        protocol = "{}.{}".format(*protocol)
        # start the response
        yield "HTTP/{} {} {}".format(protocol, code, status).encode(self.encoding, 'strict')

        # assemble the payload
        page = splicer.join(self.body(document=document, **kwds)).encode(encoding, 'strict')
        # inform the client about the size of the payload
        headers['Content-Length'] = len(page)

        # assemble the headers and send them off
        yield splicer.join(self.header(document=document)).encode(self.encoding, 'strict')
        # mark the end of the headers
        yield b''
        # send the page
        yield page
        # all done
        return


    @pyre.export
    def header(self, document):
        """
        Render the header of the document
        """
        # render the headers
        yield from ("{}: {}".format(key, value) for key,value in document.headers.items())
        # all done
        return


    @pyre.export
    def body(self, document, **kwds):
        """
        Render the body of the document
        """
        # get my html renderer to do his thing
        yield from self.html.render(document=document, **kwds)
        # all done
        return


    @pyre.export
    def footer(self):
        """
        Render the footer of the document
        """
        yield ''


# end of file