#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Exercise file opening by the file server
"""


def test():
    import os
    import pyre
    f = pyre.executive.fileserver

    # a simple case that looks for a file in the current directory
    stream = f.open('file:sample.odb')
    assert stream.name == 'sample.odb'

    # using absolute path for the same file
    stream = f.open('file:' + os.path.abspath('sample.odb'))
    assert stream.name == os.path.abspath('sample.odb')

    # using vfs
    stream = f.open('vfs:/pyre/startup/sample.odb')
    assert stream.name == os.path.abspath('sample.odb')

    # test failure modes
    # bad scheme
    try:
        f.open('unknown:sample.odb')
        assert False
    except f.URISpecificationError as error:
        assert str(error.uri) == "unknown:sample.odb"
        assert error.reason == "unsupported scheme 'unknown'"

    # missing physical file 
    try:
        f.open('file:not-there.odb')
        assert False
    except f.SourceNotFoundError as error:
        assert error.filesystem == f
        assert str(error.uri) == 'file:not-there.odb'

    # missing logical file
    try:
        f.open('vfs:/pyre/startup/not-there.odb')
        assert False
    except f.SourceNotFoundError as error:
        assert error.filesystem == f
        assert str(error.uri) == 'vfs:/pyre/startup/not-there.odb'

    # missing logical directory
    try:
        f.open('vfs:/oops/not-there.odb')
        assert False
    except f.SourceNotFoundError as error:
        assert error.filesystem == f
        assert str(error.uri) == 'vfs:/oops/not-there.odb'

    # return the file server
    return f


# main
if __name__ == "__main__":
    test()


# end of file 
