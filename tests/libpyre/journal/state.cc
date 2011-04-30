// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
//


// for the build system
#include <portinfo>

// packages
#include <assert.h>

// access to the low level state header file
#include <pyre/journal/State.h>

// convenience
typedef pyre::journal::State<true> true_t;
typedef pyre::journal::State<false> false_t;

// main program
int main() {

    // instantiate a couple of states
    true_t on;
    false_t off;

    // check their default settings
    assert(on.state() == true);
    assert(off.state() == false);

    // flip them
    on.deactivate();
    off.activate();

    // check again
    assert(on.state() == false);
    assert(off.state() == true);

    // all done
    return 0;
}

// end of file
