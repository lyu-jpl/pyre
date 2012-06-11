# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import pickle

# base classes
from .Object import Object


# declaration
class Communicator(Object):
    """
    An encapsulation of MPI communicators
    """


    # types 
    from .Port import Port


    # per-instance public data
    rank = 0
    size = 1


    # communicator factories
    def include(self, processes):
        """
        Build a new communicator with the processes in the iterable {processes} as its members
        """
        # get my group
        mine = self.group()
        # create a new group out of {processes}
        group = mine.include(tuple(processes))
        # use it to build a new communicator capsule
        capsule = self.mpi.communicatorCreate(self.capsule, group.capsule)
        # if successful
        if capsule is not None:
            # wrap it and return it
            return Communicator(capsule=capsule)
        # otherwise
        return None
        

    def exclude(self, processes):
        """
        Build a new communicator with all my processes except those in {processes}
        """
        # create a new group out of the processes not in {processes}
        group = self.group().exclude(tuple(processes))
        # use it to build a new communicator capsule
        capsule = self.mpi.communicatorCreate(self.capsule, group.capsule)
        # if successful
        if capsule is not None:
            # wrap it and return it
            return Communicator(capsule=capsule)
        # otherwise
        return None


    def cartesian(self, axes, periods, reorder=1):
        """
        Build a cartesian communicator; see the MPI documentation for details
        """
        # access the factory
        from .Cartesian import Cartesian
        # build one and return it
        return Cartesian(capsule=self.capsule, axes=axes, periods=periods, reorder=reorder)
        

    # interface
    def barrier(self):
        """
        Establish a synchronization point: all processes in this communicator must call this
        method, and they all block until the last one makes the call
        """
        # invoke the low level routine
        return self.mpi.communicatorBarrier(self.capsule)


    def group(self):
        """
        Build a group that contains all my processes
        """
        # create a new group capsule out of my processes
        capsule = self.mpi.groupCreate(self.capsule)
        # wrap it up and return it
        from .Group import Group
        return Group(capsule)


    def port(self, peer, tag=Port.tag):
        """
        Establish a point-to-point communication conduit with {peer}; all messages sent through
        this port will be tagged with {tag}
        """
        # make a port and return it
        return self.Port(peer=peer, tag=tag, communicator=self)


    # communications
    def bcast(self, item=None, root=0):
        """
        Broadcast {item} from {root} to every task; only {root} has to pass an {item}
        """
        # if I am the root, pickle the {item}
        data = pickle.dumps(item) if self.rank == root else bytes()
        # broadcast the data buffer
        data = self.mpi.bcast(self.capsule, self.rank, root, data)
        # extract the item and return it
        return pickle.loads(data)


    def sum(self, item, root):
        """
        Perform a sum reduction of {item}
        """
        # pass it on
        return self.mpi.sum(self.capsule, self.rank, root, item)


    # meta methods
    def __init__(self, capsule, **kwds):
        """
        This constructor is not public, and it is unlikely to be useful to you. To make
        communicators, access the predefined {world} communicator in the {mpi} package and use
        its interface to build new communicators
        """
        # chain to my ancestors
        super().__init__(**kwds)

        # set the per-instance variables
        self.capsule = capsule
        self.rank = self.mpi.communicatorRank(capsule)
        self.size = self.mpi.communicatorSize(capsule)

        # all done
        return


    # implementation details
    capsule = None


# end of file 
