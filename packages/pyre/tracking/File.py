# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# declaration
class File:
    """
    A locator that records a position within a file
    """


    # meta methods
    def __init__(self, source, line=None, column=None):
        self.source = source
        self.line = line
        self.column = column
        return


    def __str__(self):
        text = [
            "file={!r}".format(str(self.source))
            ]
        if self.line is not None:
            text.append("line={.line!r}".format(self))
        if self.column is not None:
            text.append("column={.column!r}".format(self))

        return ", ".join(text)


    # implementation details
    __slots__ = "source", "line", "column"


# end of file 
