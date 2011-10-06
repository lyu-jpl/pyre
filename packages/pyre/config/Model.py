# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


import weakref
import itertools
import collections
import pyre.tracking
import pyre.patterns
from pyre.algebraic.SymbolTable import SymbolTable


class Model(SymbolTable):
    """
    A specialization of a hierarchical model that takes into account that the model nodes have
    priorities attached to them and cannot indiscriminately replace each other
    """


    # constants
    TRAIT_SEPARATOR = '.'
    from .levels import DEFAULT_CONFIGURATION, EXPLICIT_CONFIGURATION


    # types
    from .Slot import Slot as slot


    # public data
    counter = None # the event priority counter
    separator = None # the level separator in the node names
    # build a locator for values that come from trait defaults
    locator = pyre.tracking.newSimpleLocator(source="<defaults>")


    # interface for my configurator
    def default(self, value):
        """
        Build a new slot with {value}

        This is called during the component trait initialization to establish the default value
        of a trait.
        """
        # build a slot out of {value}
        slot = self._recognize(value)
        # adjust the priority
        slot.priority = self.collate(category=self.DEFAULT_CONFIGURATION)
        # and the locator
        slot.locator = self.locator # use the one that says "<defaults>"
        # hand the new node back to the component without registering it here
        return slot


    # configuration event processing
    def assign(self, key, value, priority, locator=None):
        """
        Build a node with the given {priority} to hold {value}, and register it under {key}
        """
        # dump
        # print("Model.assign:")
        # print("    key={}, value={!r}".format(key, value))
        # print("    from {}".format(locator))
        # print("    with priority {}".format(priority))
        # build the slot name
        name = self.separator.join(key)
        # get the existing slot
        existing, hashkey = self._retrieveSlot(key=key, name=name)

        # convert the value into a node
        node = self._recognize(value)
        # adjust the meta data
        node.key = hashkey
        node.locator = locator
        node.priority = priority

        # adjust the value
        existing.setValue(value=node)

        # all done
        return 


    def defer(self, assignment, priority):
        """
        Build a node that corresponds to a conditional configuration
        """
        # dump
        # print("Model.defer:")
        # print("    component={0.component}".format(assignment))
        # print("    conditions={0.conditions}".format(assignment))
        # print("    key={0.key}, value={0.value!r}".format(assignment))
        # print("    from {0.locator}".format(assignment))
        # print("    with priority {}".format(priority))

        # hash the component name
        ckey = self._hash.hash(assignment.component)
        # get the deferred event store and add the assignment to the pile
        self.deferred[ckey].append(assignment)
        # all done
        return self


    def execute(self, command, priority, locator):
        """
        Record a request to execute a command
        """
        # record the command and its context
        self.commands.append((priority, command, locator))
        # all done
        return self


    def load(self, source, locator, **kwds):
        """
        Ask the pyre {executive} to load the configuration settings in {source}
        """
        # get the executive to kick start the configuration loading
        self.executive.loadConfiguration(uri=source, locator=locator)
        # and return
        return self


    def collate(self, category=None):
        """
        Build a collation index for the next event in {category}
        """
        # adjust the optional input
        category = category if category is not None else self.EXPLICIT_CONFIGURATION
        # build and return the collation sequence
        return (category, next(self.counter[category]))


    # obligations as an observer of nodes
    def pyre_updatedDependent(self, node):
        """
        Handler invoked when one of my dependents changes value
        """
        # ignore it
        return


    def pyre_substituteDependent(self, current, replacement, clean=None):
        """
        Replace {current} with {replacement} in my node index
        """
        # get the hashkeys
        chash = current.key
        rhash = replacement.key
        assert chash == rhash
        # replace the existing slot with the new one
        self._nodes[chash] = replacement
        # and return
        return


    # meta methods
    def __init__(self, executive, separator=TRAIT_SEPARATOR, **kwds):
        super().__init__(node=self.slot, **kwds)

        # the level separator
        self.separator = separator
        # the event priority counter
        self.counter = collections.defaultdict(itertools.count)

        # record the executive
        self.executive = weakref.proxy(executive)
        # the list of command requests
        self.commands = []
        # the database of deferred bindings
        self.deferred = collections.defaultdict(list)
        # the configurables that manage their own namespace
        self.configurables = weakref.WeakValueDictionary()

        # name hashing strategy
        self._hash = pyre.patterns.newPathHash()

        # done
        return


    def __getitem__(self, name):
        """
        Resolve {name} and return the value of the associated configuration setting
        """
        # retrieve the slot
        slot, _ = self._retrieveSlot(key=name.split(self.separator), name=name)
        # extract and return its value
        return slot.getValue()


    def __setitem__(self, name, value):
        """
        Add/update the named configuration setting with the given value
        """
        # print("Model: setting {!r} <- {!r}".format(name, value))
        # build the key
        key = name.split(self.separator)
        # set the priority
        priority = self.collate(category=self.EXPLICIT_CONFIGURATION)
        # build a locator for the source of the assignment
        locator = pyre.tracking.here(level=1)
        # make the assignment
        return self.assign(key=key, value=value, priority=priority, locator=locator)


    # implementation details
    def _recognize(self, value):
        """
        Attempt to convert {value} into a slot
        """
        # build a node out of {value}
        node = super()._recognize(value)
        # add me as an observer
        node.addObserver(self)
        # and return it
        return node


    def _resolve(self, name):
        """
        Find the named node
        """
        # find the slot
        slot, identifier = self._retrieveSlot(key=name.split(self.separator), name=name)
        # return the node and its identifier
        return slot, identifier


    def _retrieveSlot(self, key, name):
        """
        Retrieve the slot associated with {name}
        """
        # hash it
        hashkey = self._hash.hash(key)
        # attempt
        try:
            # to retrieve and return the slot
            return self._nodes[hashkey], hashkey
        # if not there
        except KeyError:
            # no worries
            pass

        # build the name
        name = self.separator.join(key)
        # create a new slot
        slot = self.slot.unresolved(name=name, key=hashkey, request=name)
        # observe it
        slot.addObserver(self)
        # add it to the pile
        self._nodes[hashkey] = slot
        # and return the node and its identifier
        return slot, hashkey


    # debugging support
    def dump(self, pattern=''):
        """
        List my nodes
        """
        print("model {0!r}:".format(self.name))
        print("  nodes:")
        for name, slot in self.select(pattern):
            try: 
                value = slot.node.value
            except self.UnresolvedNodeError:
                value = "unresolved"
            print("    {!r} <- {!r}".format(name, value))
            print("        from {}".format(slot.locator))

        if self.configurables:
            print("  configurables:")
            for name in self.configurables:
                print("    {!r}".format(name))
        return


# end of file 
