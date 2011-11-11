# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


import pyre.tracking
from .Requirement import Requirement


class Actor(Requirement):
    """
    The metaclass of components

    {Actor} takes care of all the tasks necessary to convert a component declaration into a
    configurable entity that coöperates fully with the framework
    """

    # types
    from .Role import Role


    # meta methods
    def __new__(cls, name, bases, attributes,
                *, family=None, implements=None, resolver=False, **kwds):
        """
        Build a new component class record

        parameters:
            {cls}: the metaclass invoked; guaranteed to be a descendant of {Actor}
            {name}, {bases}, {attributes}: the usual class specification
            {family}: the public name of this component class; used to configure it
            {implements}: the tuple of interfaces that this component is known to implement
        """
        # build the interface specification
        try:
            interface = cls.pyre_buildImplementationSpecification(bases, implements)
        except cls.ImplementationSpecificationError as error:
            error.name = name
            error.description = "{}: {}".format(name, error.description)
            raise
        # and add it to the attributes
        attributes["pyre_implements"] = interface
        # create storage for the configurable state
        attributes["pyre_inventory"] = {}
        # get my ancestors to build the class record
        component = super().__new__(cls, name, bases, attributes, family=family, **kwds)
        # if an interface spec was derivable from the declaration, check interface compatibility 
        if interface:
            # check whether the requirements were implemented correctly
            check = component.pyre_isCompatible(interface)
            if not check:
                raise cls.InterfaceError(component, interface, check)
        # if the component wants to intercept descriptor retrieval from its namespace
        if resolver:
            # register it with the executive
            component.pyre_executive.registerNamespaceResolver(resolver=component, namespace=family)
        # and pass the component on
        return component


    def __init__(self, name, bases, attributes, hidden=False, **kwds):
        """
        Initialize a new component class record
        """
        # initialize the record
        super().__init__(name, bases, attributes, **kwds)

        # record whether I am hidden
        self.pyre_hidden = hidden
        # and if so, bail out
        if hidden: return

        # access the configuration store
        configurator = self.pyre_executive.configurator
        # cache my family name
        family = self.pyre_family

        # print("{}: setting up inventory".format(self))
        # build inventory items for all the local traits
        # print("  local traits:")
        for trait in self.pyre_localTraits:
            # print("    {.name}".format(trait))
            # check whether to keep this trait in inventory
            if not trait.isConfigurable: continue
            # otherwise, build the configurator access key
            key = family + [trait.name] if family else tuple()
            # print("      key={!r}".format(key))
            # transfer the default value of this trait to the configuration store
            slot = configurator.default(key=key, value=trait.default)
            # record the trait
            slot.trait = trait
            # add me as an observer
            slot.componentClass = self
            # save the slot in my inventory
            self.pyre_inventory[trait] = slot
            # if i am registered with the configuration store
            if key:
                # iterate over my aliases
                for alias in trait.aliases:
                    # avoid duplicate registration
                    if alias == trait.name: continue
                    # build the alias key
                    aliasKey = family + [alias]
                    # register it
                    configurator._alias(canonical=key, alias=aliasKey)
            
        # repeat with the inherited traits; the trick here is to locate which ancestor to build
        # a reference to
        # print("  inherited traits:")
        for trait in self.pyre_inheritedTraits:
            # print("    {.name}".format(trait))
            # check whether to keep this trait in inventory
            if not trait.isConfigurable: continue
            # otherwise, build the configurator access key
            key = family + [trait.name] if family else tuple()
            # search for the closest ancestor that has a slot for this trait
            for ancestor in self.pyre_pedigree:
                # if it's here
                try:
                    # get the slot and exit the search
                    anchor = ancestor.pyre_inventory[trait]
                    break
                # if it's not here
                except KeyError:
                    # no worries, get the next ancestor
                    continue
            # if it's not there at all
            else:
                # IMPOSSIBLE
                import journal
                firewall = journal.firewall("pyre.components")
                raise firewall.log(
                    "could not locate ancestor for '{.pyre_name}.{name}'".format(self, trait))

            # we found the slot; build a reference to it
            ref = anchor.ref()
            # notify the configuration store; we may get a different slot back, depending on
            # whether the configuration store has any relevant information on this trait
            slot = configurator.default(key=key, value=ref)
            # record the trait
            slot.trait = trait
            # add me as an observer
            slot.componentClass = self
            # and save the slot in my inventory
            self.pyre_inventory[trait] = slot
            # if i am registered with the configuration store
            if key:
                # iterate over my aliases
                for alias in trait.aliases:
                    # avoid duplicate registration
                    if alias == trait.name: continue
                    # build the alias key
                    aliasKey = family + [alias]
                    # register it
                    configurator._alias(canonical=key, alias=aliasKey)


        # register it with the executive
        self.pyre_executive.registerComponentClass(self)

        # all done
        return


    def __setattr__(self, name, value):
        """
        Trap attribute setting in my class record instances to support setting the default
        value using the natural syntax
        """
        # print("Actor.__setattr__: {!r}<-{!r}".format(name, value))
        # check whether the name corresponds to a trait
        try:
            trait = self.pyre_getTraitDescriptor(alias=name)
        # if it doesn't, bypass
        except self.TraitNotFoundError as error:
            super().__setattr__(name, value)
            return
        # so, the name resolved to a trait
        # build an appropriate locator
        locator = pyre.tracking.here(level=1)
        # ask the trait descriptor to set the value
        trait.pyre_setClassTrait(configurable=self, value=value, locator=locator)
        # and return
        return


    # implementation details
    @classmethod
    def pyre_buildImplementationSpecification(cls, bases, implements):
        """
        Build a class that describes the implementation requirements imposed on this
        {component}, given its class record and the list of interfaces it {implements}
        """
        # initialize the list of interfaces
        interfaces = []
        # try to understand what the component author specified
        if implements is not None:
            # accumulator for the interfaces {component} doesn't implement correctly
            errors = []
            # if {implements} is a single interface, add it to the pile
            if isinstance(implements, cls.Role):
                interfaces.append(implements)
            # the only legal alternative is an iterable of Interface subclasses
            else:
                try:
                    for interface in implements:
                        # if it's an actual Interface subclass
                        if isinstance(interface, cls.Role):
                            # add it to the pile
                            interfaces.append(interface)
                        # otherwise, place it in the error bin
                        else:
                            errors.append(interface)
                # if {implemenents} is not iterable
                except TypeError as error:
                    # put it in the error bin
                    errors.append(implements)
            # report the errors we encountered
            if errors:
                raise cls.ImplementationSpecificationError(errors=errors)
        # now, add the commitments made by my immediate ancestors
        interfaces += [
            base.pyre_implements for base in bases
            if isinstance(base, cls) and base.pyre_implements is not None ]
        # bail out if we didn't manage to find eny interfaces
        if not interfaces: return None
        # if there is only one interface on my pile
        if len(interfaces) == 1:
            # use it directly
            return interfaces[0]
        # otherwise, derive an interface from the harvested ones and return it as the
        # implementation specification
        return cls.Role("Interface", tuple(interfaces), dict(), hidden=True)


    # trait observation
    def pyre_updatedClassProperty(self, slot):
        """
        Handler invoked when the value of one of my traits changes
        """
        # ignore it, for now
        return


    def pyre_replaceClassSlot(self, current, replacement, clean=None):
        """
        Replace {current} with {replacement} in my inventory
        """
        # adjust my inventory
        self.pyre_inventory[current.trait] = replacement
        # and return
        return


    # exceptions
    from .exceptions import ImplementationSpecificationError, InterfaceError


# end of file 
