# libraries imported
from __future__ import annotations
from abc import ABC, abstractmethod
from computer import Computer
from route import Route
from branch_decision import BranchDecision
from data_structures.linked_stack import LinkedStack


class VirusType(ABC):

    def __init__(self) -> None:
        self.computers = []

    def add_computer(self, computer: Computer) -> None:
        self.computers.append(computer)

    @abstractmethod
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        raise NotImplementedError()

class TopVirus(VirusType):
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        # Always select the top branch
        return BranchDecision.TOP

class BottomVirus(VirusType):
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        # Always select the bottom branch
        return BranchDecision.BOTTOM

class LazyVirus(VirusType):
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        """
        Try looking into the first computer on each branch,
        take the path of the least difficulty.
        """
        
        """
        EDITED:
        top_route = type(top_branch.store) == RouteSeries
        bot_route = type(bottom_branch.store) == RouteSeries
        
        type() and isinstance() always produced incorrect results; replaced with .__class__.__name__.
        Should perform the same operation regardless.
        """
        top_route = top_branch.store.__class__.__name__ == "RouteSeries"
        bot_route = bottom_branch.store.__class__.__name__ == "RouteSeries"
        
        if top_route and bot_route:
            top_comp = top_branch.store.computer
            bot_comp = bottom_branch.store.computer

            if top_comp.hacking_difficulty < bot_comp.hacking_difficulty:
                return BranchDecision.TOP
            elif top_comp.hacking_difficulty > bot_comp.hacking_difficulty:
                return BranchDecision.BOTTOM
            else:
                return BranchDecision.STOP
        # If one of them has a computer, don't take it.
        # If neither do, then take the top branch.
        if top_route:
            return BranchDecision.BOTTOM
        return BranchDecision.TOP

class RiskAverseVirus(VirusType):
    """
    This class represents a special of type of virus that relies on complex operations to traverse (see below).
    """
    
    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        """
        :description: This virus is risk averse and likes to choose the path with the lowest risk factor.
        :param: top_branch (Route) -> The top branch of the route.
        :param: bottom_branch (Route) -> The bottom branch of the route.
        :returns: (BranchDecision) -> The branch that the virus will take.
        :complexity: O(calculate_value()) -> Check the function docstring for complexity analysis.
        """
        
        # storing booleans of whether both branches are series or not.
        top_route: bool = top_branch.store.__class__.__name__ == "RouteSeries"
        bot_route: bool = bottom_branch.store.__class__.__name__ == "RouteSeries"
        
        # if they are both series objects,
        if top_route and bot_route:
            
            # getting the computer objects
            top_comp: Computer = top_branch.store.computer
            bot_comp: Computer = bottom_branch.store.computer
            
            # if the both the risk factors are 0,
            if top_comp.risk_factor == 0.0 and bot_comp.risk_factor == 0.0:

                # we need to check which computer has lower hacking difficulty.
                if top_comp.hacking_difficulty < bot_comp.hacking_difficulty:
                    return BranchDecision.TOP
                elif top_comp.hacking_difficulty > bot_comp.hacking_difficulty:
                    return BranchDecision.BOTTOM
                
            elif top_comp.risk_factor == 0.0:
                return BranchDecision.TOP
            elif bot_comp.risk_factor == 0.0:
                return BranchDecision.BOTTOM
            
            # getting the values if they are not tied.
            val_top: float = self._calculate_value(top_comp.risk_factor, top_comp.hacking_difficulty, top_comp.hacked_value)
            val_bot: float = self._calculate_value(bot_comp.risk_factor, bot_comp.hacking_difficulty, bot_comp.hacked_value)
            
            # path with the highest value will make the virus travel there.
            if val_top > val_bot:
                return BranchDecision.TOP
            elif val_top < val_bot:
                return BranchDecision.BOTTOM
            else:
                
                # if tied again, the path with lowest risk factor will be infected.
                if top_comp.risk_factor > bot_comp.risk_factor:
                    return BranchDecision.BOTTOM
                elif top_comp.risk_factor < bot_comp.risk_factor:
                    return BranchDecision.TOP
                else:
                    
                    # if still tied, stop.
                    return BranchDecision.STOP
        
        # if there is one series and one split, go to the routesplit.
        if top_route and not bot_route:
            return BranchDecision.BOTTOM
        elif bot_route and not top_route:
            return BranchDecision.TOP
        
        return BranchDecision.TOP
    
    @staticmethod
    def _calculate_value(risk_factor, hacking_difficulty, hacked_value) -> float:
        """
        :description: Calculates the value that determines which route the virus will take
        :param: risk_factor (float) -> The risk factor of the computer.
        :param: hacking_difficulty (float) -> The hacking difficulty of the computer.
        :param: hacked_value (float) -> The hacked value of the computer
        :returns: (float) -> The value that determines which route the virus will takes.
        :best complexity: O(1) -> All operations are done in constant time.
        :worst complexity: O(1) -> All operations are done in constant time.
        """
        
        highest_val = max(hacking_difficulty, hacked_value / 2)
        if risk_factor > 0:
            highest_val /= risk_factor
        
        return highest_val

class FancyVirus(VirusType):
    """
    This class contains a special type of virus that uses the reverse polish notation to determine its route.
    """

    CALC_STR = "7 3 + 8 - 2 * 2 /"

    def select_branch(self, top_branch: Route, bottom_branch: Route) -> BranchDecision:
        """
        :description: This virus has a fancy-pants and likes to overcomplicate its approach.
        :param: top_branch (Route) -> The top branch of the route.
        :param: bottom_branch (Route) -> The bottom branch of the route.
        :returns: (BranchDecision) -> The branch that the virus will take.
        :complexity: O(calculate_threshold()) -> Please check the docstring for complexity analysis.
        """
        
        threshold: float = self._calculate_threshold(self.CALC_STR)
        
        # storing booleans of whether both branches are series or not.
        top_route: bool = top_branch.store.__class__.__name__ == "RouteSeries"
        bot_route: bool = bottom_branch.store.__class__.__name__ == "RouteSeries"
        
        # if they are both series objects,
        if top_route and bot_route:
            top_comp: Computer = top_branch.store.computer
            bot_comp: Computer = bottom_branch.store.computer
            
            # if both computers exist,
            if top_comp and bot_comp:
                if top_comp.hacked_value < threshold:
                    return BranchDecision.TOP
                elif bot_comp.hacked_value > threshold:
                    return BranchDecision.BOTTOM
                else:
                    return BranchDecision.STOP
        
        # if there is one series and one split, go to the routesplit.
        if top_route and not bot_route:
            return BranchDecision.BOTTOM
        elif bot_route and not top_route:
            return BranchDecision.TOP
        
        # default return
        return BranchDecision.TOP
            
    @staticmethod
    def _calculate_threshold(STR: str) -> float:
        """
        :description: Calculates the threshold value based on a given reverse polish string.
        :param: STR (str) -> The reverse polish string.
        :returns: (float) -> The threshold value.
        :best complexity: O(N*comp[==]) -> Where N is the number of entries inside the String. By default, if it is a number, it gets pushed into the stack.
        :worst complexity: O(N*comp[==]) -> Where N is the number of entries inside the String. The entry '/' is at the end of the string, and is compared in the end to divide two numbers.
        """
        
        # splitting the characters into a list.
        characters = STR.split()
        
        # a stack to keep track of the numbers.
        nums_collected = LinkedStack()
        
        for element in characters:
            
            if element not in '+-*/':
                nums_collected.push(int(element))
            else:
                operands = (nums_collected.pop(), nums_collected.pop())
                
                if element == '+':
                    nums_collected.push(operands[1] + operands[0])
                elif element == '-':
                    nums_collected.push(operands[1] - operands[0])
                elif element == '*':
                    nums_collected.push(operands[1] * operands[0])
                elif element == '/':
                    nums_collected.push(operands[1] / operands[0])
        
        return nums_collected.pop()
