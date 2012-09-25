# -*- Makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


PROJECT = pyre
PACKAGE = timers/epoch

all: export

export:: export-package-headers

release:: release-package-headers


EXPORT_PKG_HEADERS = \
    Clock.h Clock.icc

# end of file 
