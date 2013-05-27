#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


"""
Verify record building in the presence of multiple inheritance
"""


def test():
    import pyre.records


    class item(pyre.records.record):
        """
        A sample record
        """
        sku = pyre.records.field()
        description = pyre.records.field()
        cost = pyre.records.field()


    class pricing(item):
        price = 2 * item.cost


    # explore the item record
    assert isinstance(item.sku, pyre.records.field)
    assert isinstance(item.description, pyre.records.field)

    assert identical(item.pyre_localEntries, (item.sku, item.description))
    assert identical(item.pyre_fields, (item.sku, item.description))
    assert identical(item.pyre_measures, (item.sku, item.description))
    assert identical(item.pyre_derivations, ())

    assert item.pyre_index[item.sku] == 0
    assert item.pyre_index[item.description] == 1

    # explore the derived class
    assert isinstance(pricing.sku, pyre.records.field)
    assert isinstance(pricing.description, pyre.records.field)
    assert isinstance(pricing.cost, pyre.records.field)
    assert isinstance(pricing.price, pyre.records.derivation)

    assert identical(pricing.pyre_localEntries, (pricing.price,))
    assert identical(pricing.pyre_fields, (
        pricing.sku, pricing.description, pricing.cost,
        pricing.price,
        ))
    assert identical(pricing.pyre_measures, (
        pricing.sku, pricing.description, pricing.cost,
        ))
    assert identical(pricing.pyre_derivations, (pricing.price,))

    assert pricing.pyre_index[pricing.sku] == 0
    assert pricing.pyre_index[pricing.description] == 1
    assert pricing.pyre_index[pricing.cost] == 2
    assert pricing.pyre_index[pricing.price] == 3

    # now instantiate one
    cost = 1.0
    p = pricing(sku="4013", description="kiwi", cost=cost)
    # check
    assert p.sku == "4013"
    assert p.description == "kiwi"
    assert p.cost == 1.0
    assert p.price == 2 * p.cost

    return p


def identical(s1, s2):
    """
    Verify that the nodes in {s1} and {s2} are identical. This has to be done carefully since
    we must avoid triggering __eq__
    """
    for n1, n2 in zip(s1, s2):
        if n1 is not n2: return False
    return True


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
