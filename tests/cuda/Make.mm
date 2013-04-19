# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


PROJECT = pyre

#--------------------------------------------------------------------------
#

all: test

test: sanity

sanity:
	${PYTHON} ./sanity.py
	${PYTHON} ./extension.py
	${PYTHON} ./manager.py


# end of file 