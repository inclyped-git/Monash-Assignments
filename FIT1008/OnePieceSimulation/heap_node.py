from __future__ import annotations
from dataclasses import dataclass
from landsites import Land

@dataclass
class HeapNode:
    """
    Class that sorts the order of the MaxHeap created full of Land objects with o-scores.
    """
    
    # instance variables
    land: Land
    o_score: float

    # getters
    def get_land(self) -> Land:
        """
        :description: Returns the land object.
        :param: void.
        :returns: (Land) -> The land object.
        """
        return self.land
    
    def get_score(self) -> float:
        """
        :description: Returns the o-score.
        :param: void.
        :returns: (float) -> The o-score of a land.
        """

        return self.o_score
    
    # dunder methods
    def __eq__(self, other: HeapNode) -> bool:
        """
        :description: Returns the result of evaluation.
        :param: (HeapNode) -> The other heapnode being compared.
        :returns: (bool) -> Result of evaluation.
        """
        return self.o_score == other.o_score

    def __le__(self, other: HeapNode) -> bool:
        """
        :description: Returns the result of evaluation.
        :param: (HeapNode) -> The other heapnode being compared.
        :returns: (bool) -> Result of evaluation.
        """
        return self.o_score <= other.o_score
    
    def __lt__(self, other: HeapNode) -> bool:
        """
        :description: Returns the result of evaluation.
        :param: (HeapNode) -> The other heapnode being compared.
        :returns: (bool) -> Result of evaluation.
        """
        return self.o_score < other.o_score
    
    def __ge__(self, other: HeapNode) -> bool:
        """
        :description: Returns the result of evaluation.
        :param: (HeapNode) -> The other heapnode being compared.
        :returns: (bool) -> Result of evaluation.
        """
        return self.o_score >= other.o_score
    
    def __gt__(self, other: HeapNode) -> bool:
        """
        :description: Returns the result of evaluation.
        :param: (HeapNode) -> The other heapnode being compared.
        :returns: (bool) -> Result of evaluation.
        """
        return self.o_score > other.o_score
    
    def __ne__(self, other: HeapNode) -> bool:
        """
        :description: Returns the result of evaluation.
        :param: (HeapNode) -> The other heapnode being compared.
        :returns: (bool) -> Result of evaluation.
        """
        return self.o_score != other.o_score
