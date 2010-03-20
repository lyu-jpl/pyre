# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


PROJECT = pyre
PACKAGE = patterns
PROJ_DISTCLEAN = $(EXPORT_MODULEDIR)/$(PACKAGE)


#--------------------------------------------------------------------------
#

all: export

#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    AbstractMetaclass.py \
    AttributeClassifier.py \
    ExtentAware.py \
    Observable.py \
    Named.py \
    Singleton.py \
    __init__.py


export:: export-package-python-modules

# end of file 
