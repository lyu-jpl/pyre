# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import collections
import pyre.tracking
from .Model import Model


class Configurator(Model):
    """
    The keeper of all configurable values maintained by the framework

    This class is a pyre.calc.AbstractModel that maintains the global configuration state of
    the framework. All configuration events encountered are processed by a Configurator
    instance held by the pyre executive and become nodes in the configuration model.
    """


    # constants
    TRAIT_SEPARATOR = '.'
    FAMILY_SEPARATOR = '#'

    # exceptions
    from ..calc.exceptions import (
        CircularReferenceError, DuplicateNodeError, ExpressionError, NodeError,
        UnresolvedNodeError)
    

    # public data
    counter = None # the event priority counter
    # build a locator for values that come from trait defaults
    locator = pyre.tracking.newSimpleLocator(source="<defaults>")


    # interface
    def configure(self, configuration, priority):
        """
        Iterate over the {configuration} events and insert them into the model at the given
        {priority} level
        """
        # loop over events
        for event in configuration.events:
            # build the event sequence number, which becomes its priority level
            seq = (priority, self.counter[priority])
            # update the counter
            self.counter[priority] += 1
            # and process the event
            event.identify(inspector=self, priority=seq)
        # all done
        return
 

    # support for the pyre executive
    def configureComponentClass(self, component):
        """
        Adjust the model for the presence of a component

        Look through the model for settings that correspond to {component} and transfer them to
        its inventory. Register {component} as the handler of future configuration events in
        its namespace
        """
        # get the class family
        ns = component.pyre_family
        # if there is no family name, we are done
        if not ns: return []
        # transfer the configuration under the component's family name
        errors = self._transferConfigurationSettings(configurable=component, namespace=ns)
        # return the accumulated errors
        return errors


    def configureComponentInstance(self, component):
        """
        Initialize the component instance inventory by making the descriptors point to the
        evaluation nodes
        """
        # build the component name and key
        ns = component.pyre_name.split(self.separator)
        # transfer the configuration under the component's name
        errors = self._transferConfigurationSettings(configurable=component, namespace=ns)
        # transfer the conditional configuration settings
        # return the accumulated errors
        return errors


    # meta methods
    def __init__(self, executive, name=None, **kwds):
        # construct my name
        name = name if name is not None else "pyre.configurator"
        super().__init__(name=name, executive=executive, separator=self.TRAIT_SEPARATOR, **kwds)

        # the event priority counter
        self.counter = collections.Counter()

        return


    def __getitem__(self, name):
        """
        Indexed access to the configuration store
        """
        return self.resolve(name=name).value


    def __setitem__(self, name, value):
        """
        Support for programmatic modification of the configuration store
        """
        # get the priority sequence class for explicit settings
        explicit = self.executive.EXPLICIT_CONFIGURATION
        # build the event sequence number, which becomes its priority level
        seq = (explicit, self.counter[explicit])
        # update the counter
        self.counter[explicit] += 1
        # build a slot
        slot = self.nodeFactory(value=None, evaluator=self.recognize(value=value), priority=seq)
        # build a locator
        locator = pyre.tracking.here(level=1)
        # register the slot
        self.register(name=name, node=slot)
        # and return
        return


    # implementation details
    def _transferConfigurationSettings(self, configurable, namespace, errors=None):
        """
        Transfer ownership of the configuration store to {configurable} and apply whatever
        configuration id available for it in the configuration store
        """
        # initialize the error accumulator
        errors = errors if errors is not None else []
        # get the inventory
        inventory = configurable.pyre_inventory
        # let's see what is known about this instance
        # let's see what is known about this instance
        for key, name, fqname, node in self.children(rootKey=namespace):
            # find the corresponding descriptor
            try:
                descriptor = configurable.pyre_getTraitDescriptor(alias=name)
            # found a typo?
            except configurable.TraitNotFoundError as error:
                errors.append(error)
                continue
            # get the inventory slot
            slot = inventory[descriptor]
            # merge the information
            slot.merge(other=node)
            # patch the model
            self.patch(old=node, new=slot)
            # replace the node with the inventory slot so aliases still work
            self._nodes[key] = slot
            # and eliminate the old node from the name stores
            del self._names[key]
            del self._fqnames[key]
        # establish {component} as the handler of events in its configuration namespace
        self.configurables[self.separator.join(namespace)] = configurable
        # return the accumulated errors
        return errors
        
        


# end of file 
