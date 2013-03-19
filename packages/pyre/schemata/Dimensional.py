# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# my superclass
from .Type import Type


# declaration
class Dimensional(Type):
    """
    A type declarator for quantities with units
    """


    # types
    from ..units import parser as parserFactory, dimensional


    # public data
    parser = parserFactory()


    # interface
    @classmethod
    def coerce(cls, value, **kwds):
        """
        Attempt to convert {value} into a dimensional
        """
        # use the unit parser to convert strings to dimensionals 
        if isinstance(value, str):
            return cls.parser.parse(value)
        # dimensionals go right through
        if isinstance(value, cls.dimensional):
            return value
        # everything else is an error
        msg="could not convert {0.value!r} into a dimensional quantity"
        raise cls.CastingError(value=value, description=msg)
        

# end of file 