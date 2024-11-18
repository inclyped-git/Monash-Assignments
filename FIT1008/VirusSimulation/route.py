# libraries imported
from __future__ import annotations
from dataclasses import dataclass
from computer import Computer
from typing import TYPE_CHECKING, Union
from branch_decision import BranchDecision
from data_structures.linked_stack import LinkedStack
if TYPE_CHECKING:
    from virus import VirusType


@dataclass
class RouteSplit:
    """
    A split in the route.
       _____top______
      /              \
    -<                >-following-
      \____bottom____/
    """

    top: Route
    bottom: Route
    following: Route

    def remove_branch(self) -> RouteStore:
        """
        :description: Removes the branch, should just leave the remaining following route
        :returns: (RouteStore) -> A RouteStore object
        :best complexity: O(1) -> All operations are done in constant time.
        :worst complexity: O(1) -> All operations are done in constant time.
        """
        
        # creating a new object that only stores the FOLLOWING node's RouteStore object.
        new_route: RouteStore = self.following.store
        return new_route

@dataclass
class RouteSeries:
    """
    A computer, followed by the rest of the route

    --computer--following--
    """

    computer: Computer
    following: Route

    def remove_computer(self) -> RouteStore:
        """
        :description: Returns a route store which would be the result of: Removing the computer at the beginning of this series.    
        :returns: (RouteStore) -> Returns a RouteStore object.
        :best complexity: O(1) -> All operations are done in constant time.
        :worst complexity: O(1) -> All operations are done in constant time.
        """
        
        # creating a new RouteStore object and returning the FOLLOWING node's RouteStore object
        new_route: RouteStore = self.following.store
        return new_route

    def add_computer_before(self, computer: Computer) -> RouteStore:
        """
        :description: Returns a route store which would be the result of: Adding a computer in series before the current one.
        :param: computer (Computer) -> The computer to be added to the route.
        :returns: (RouteStore) -> A RouteStore object.
        :best complexity: O(1) -> All operations are done in constant time.
        :worst complexity: O(1) -> All operations are done in constant time.
        """
        # creating a new RouteStore object that adds a computer before the CURRENT node.
        new_route: RouteStore = RouteSeries(computer=computer, following=Route(self))
        return new_route

    def add_computer_after(self, computer: Computer) -> RouteStore:
        """
        :description: Returns a route store which would be the result of: Adding a computer after the current computer, but before the following route.
        :param: computer (Computer) -> The computer to be added to the route.
        :returns: (RouteStore) -> A RouteStore object.
        :best complexity: O(1) -> All operations are done in constant time.
        :worst complexity: O(1) -> All operations are done in constant time.
        """
        
        # creating a new RouteStore object that adds a computer after the CURRENT node.
        new_route: RouteStore = RouteSeries(computer=computer, following=self.following)
        return RouteSeries(self.computer, Route(new_route))
        
    def add_empty_branch_before(self) -> RouteStore:
        """
        :description: Returns a route store which would be the result of: Adding an empty branch, where the current routestore is now the following path.
        :returns: (RouteStore) -> A RouteStore object.
        :best complexity: O(1) -> All operations are done in constant time.
        :worst complexity: O(1) -> All operations are done in constant time.
        """
        
        # creating a new RouteSplit object that consists of empty top and bottom branches; following branch leads to the CURRENT node.
        new_route: RouteSplit = RouteSplit(top=Route(None), bottom=Route(None), following=Route(self))
        return new_route

    def add_empty_branch_after(self) -> RouteStore:
        """
        :description: Returns a route store which would be the result of: Adding an empty branch after the current computer, but before the following route
        :returns: (RouteStore) -> A RouteStore object.
        :best complexity: O(1) -> All operations are done in constant time.
        :worst complexity: O(1) -> All operations are done in constant time.
        """
        
        # creating a new RouteSplit object that consists of empty top and bottom branches; following branch leads to the node after CURRENT node.
        new_route: RouteSplit = RouteSplit(top=Route(None), bottom=Route(None), following=self.following)
        return RouteSeries(computer=self.computer, following=Route(new_route))

RouteStore = Union[RouteSplit, RouteSeries, None]

@dataclass
class Route:

    store: RouteStore = None

    def add_computer_before(self, computer: Computer) -> Route:
        """
        :description: Returns a *new* route which would be the result of: Adding a computer before everything currently in the route.
        :param: computer (Computer) -> A computer to be added.
        :returns: (Route) -> A new Route object.
        :best complexity: O(1) -> All operations are done in constant time.
        :worst complexity: O(1) -> All operations are done in constant time.
        """
        
        # creating a new RouteSeries object to insert the computer and returns the new route.
        new_series: RouteSeries = RouteSeries(computer=computer, following=self)
        return Route(new_series)

    def add_empty_branch_before(self) -> Route:
        """
        :description: Returns a *new* route which would be the result of: Adding an empty branch before everything currently in the route
        :returns: (Route) -> A new Route object.
        :best complexity: O(1) -> All operations are done in constant time.
        :worst complexity: O(1) -> All operations are done in constant time.
        """
        
        # creating a new RouteSplit object to create a branch before the CURRENT node.
        new_branch: RouteSplit = RouteSplit(Route(None), Route(None), self)
        return Route(new_branch)

    def follow_path(self, virus_type: VirusType) -> None:
        """
        :description: Follow a path and add computers according to a virus_type.
        :param: virus_type (VirusType) -> The virus that goes through a route.
        :best complexity: O(1) -> LazyVirus encounters top and bottoms branches as RouteSeries objects of equal computer hacking difficulty.
        :worst complexity: O(N) -> Where N is the length of the longest route path taken from the self to the end of the route. VirusType object traverses through the longest route.
        """
        
        # storing every following route objects when traversing through each split.
        following_nodes: LinkedStack = LinkedStack()
        
        # we will be starting from the current Route object.
        curr: Route = self
        
        # the loop will traverse indefinitely until the end route is met.
        while curr.store: # O(1) | O(N)
            
            # if the current node is a route object, convert it to Split or Series.
            if isinstance(curr, Route):
                curr: RouteStore = curr.store
            
            # now we will check if the current node is Series, Split, or reached the End of a branch.
            if isinstance(curr, RouteSplit):
                
                # if the encountered object is split,
                
                # add the following node to the following nodes stack.
                following_nodes.push(curr.following)
                
                # the virus makes a decision whether to choose top, bottom, or stop.
                match virus_type.select_branch(curr.top, curr.bottom):
                    
                    case BranchDecision.TOP:
                        curr: Route = curr.top
                    
                    case BranchDecision.BOTTOM:
                        curr: Route = curr.bottom
                    
                    case BranchDecision.STOP:
                        break
            
            
            elif isinstance(curr, RouteSeries):
            
               # if the encountered object is series,
               
               # add the computer that exists within the series.
               virus_type.add_computer(curr.computer)
               
               # after the computer, we need to check if the next route is None or not.
               if curr.following.store is None:
                   
                   # if there is nothing else left, and the stack is empty, the route is over.
                   if following_nodes.is_empty():
                       break
                   else:
                   
                       # otherwise, go to the recent following node pushed in the stack.
                       curr: Route = following_nodes.pop()
                       
               # if the next route is not None, current node is the following node.
               else:
                   curr: Route = curr.following
            

            elif isinstance(curr, None):
                
                # if the encountered object is None, just go the next following node.
                
                curr: Route = following_nodes.pop()
            

            while curr.store is None:
                
                # when the virus reaches the end point, whatever following nodes are present, just iterate through that.
                if not following_nodes.is_empty():
                    curr: Route = following_nodes.pop() 
                else:
                    break
            
    def add_all_computers(self) -> list[Computer]:
        """
        :description: Returns a list of all computers on the route
        :returns: (list) -> A list of computers that are inside the network of routes.
        :complexity: O(_auxiliary_add_all_computers()) -> Check the function docstring for complexity analysis.
        """
        
        computers_collected: list[Computer] = []
        following_nodes: LinkedStack = LinkedStack()
        self._auxiliary_add_all_computers(self.store, computers_collected, following_nodes)
        return computers_collected

    def _auxiliary_add_all_computers(self, curr: RouteStore, list_of_comps: list[Computer], stack_of_nodes: LinkedStack) -> None:
        """
        :description: An auxiliary function for the recursive add_all_computers() function. Recursively iterates through all Route objects inside the network.
        :param: curr (RouteStore) -> The next node to perform operations with.
        :param: list_of_comps (list) -> A list of computers that the curr pointer has encountered with.
        :param: stack_of_nodes (LinkedStack) -> A stack to keep track of the following nodes
        :best complexity: O(1) -> If the current pointer points to the end of the route, it halts the iteration.
        :worst complexity: O(N) -> Where N is the number of route nodes that exist inside the network. This scenario involves the recursion through every series object of every split.
        """
        
        # BASE CASE: if the stack is already empty, and if the current is None, this is the end of the trail.
        if stack_of_nodes.is_empty() and curr is None:
            return
        
        # if the curr is a RouteSeries, add the computer and recursively call the function for the following node.
        if isinstance(curr, RouteSeries):
            list_of_comps.append(curr.computer)
            self._auxiliary_add_all_computers(curr.following.store, list_of_comps, stack_of_nodes)
        
        # if the curr is a RouteSplit, 
        elif isinstance(curr, RouteSplit):
            
            # push the following nodes to the stack.
            stack_of_nodes.push(curr.following)
            
            # recursively iterate through each branch, until they reach the end of the route.
            self._auxiliary_add_all_computers(curr.top.store, list_of_comps, stack_of_nodes)
            self._auxiliary_add_all_computers(curr.bottom.store, list_of_comps, stack_of_nodes)
        
        # if the curr has reached the end of a branch, go to the recent following node.
        elif curr is None:
            if not stack_of_nodes.is_empty():
                self._auxiliary_add_all_computers(stack_of_nodes.pop().store, list_of_comps, stack_of_nodes)
