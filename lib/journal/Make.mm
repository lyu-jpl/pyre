# -*- Makefile -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#

include shared/target.def

PROJECT = pyre
PACKAGE = journal

PROJ_TMPDIR = $(BLD_TMPDIR)/$(PROJECT)/$(PACKAGE)
PROJ_SAR = $(BLD_LIBDIR)/lib$(PACKAGE).$(EXT_SAR)
PROJ_DLL = $(BLD_LIBDIR)/lib$(PACKAGE).$(EXT_SO)

PROJ_SRCS = \
    debuginfo.cc \
    firewalls.cc \
    journal.cc \
    Chronicler.cc \
    Console.cc \
    Device.cc \
    Renderer.cc \
    Streaming.cc \


#--------------------------------------------------------------------------
#

all: $(PROJ_DLL) export

export:: export-headers export-package-headers export-libraries

release:: release-headers release-package-headers release-libraries


EXPORT_LIBS = $(PROJ_DLL)

EXPORT_HEADERS = \
    journal.h

EXPORT_PKG_HEADERS = \
    debuginfo.h \
    firewalls.h \
    macros.h \
    manipulators.h manipulators.icc \
    Channel.h Channel.icc \
    Chronicler.h Chronicler.icc \
    Console.h \
    Debug.h Debug.icc \
    Device.h Device.icc \
    Diagnostic.h Diagnostic.icc \
    Error.h Error.icc \
    Firewall.h Firewall.icc \
    Index.h Index.icc \
    Informational.h Informational.icc \
    Inventory.h Inventory.icc \
    Locator.h Locator.icc \
    Null.h Null.icc \
    Renderer.h Renderer.icc \
    Selector.h Selector.icc \
    Streaming.h Streaming.icc \
    Warning.h Warning.icc \


# end of file 
