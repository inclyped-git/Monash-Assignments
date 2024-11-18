from __future__ import annotations
from msilib import Binary
from computer import Computer
from algorithms.mergesort import merge, mergesort
from algorithms.binary_search import binary_search


class ComputerOrganiser:

    def __init__(self) -> None:
        self.record = []

    def cur_position(self, computer: Computer) -> int:
        """
        best = O(1) -> If the computer is found at the middle of the list.
        worst = O(log N) -> If the computer is found in the start or end of the list, with comparisons made based on the object comparisons defined in the dunder methods in Computer class. 
        """
        try:
            pos = binary_search(self.record, computer)
           
            if id(self.record[pos]) == id(computer):
                return pos
            else:
                raise KeyError
        except:
            raise KeyError
        
    def add_computers(self, computers: list[Computer]) -> None:
        """
        best complexity = ( N log N ), where N is the length of the new computer list in ascending order and there is no computers inside self.computers to merge and sort again with.
        worst complexity = ( N log N + M ), where N is the length of the new computer list in a descending order, and M is the length of the sorted self.computers list that merges and sorts again.
        """
        
        sorted_comps = mergesort(computers, key=lambda x: (x.hacking_difficulty, x.risk_factor, x.name))
        self.record = merge(self.record, sorted_comps, key = lambda x: (x.hacking_difficulty, x.risk_factor, x.name))

    def remove_computer(self, computer):
        """
        best complexity = O(1) when the item is deleted in the last of the list and there is no reshuffling.
        worst complexity = O(N) when the item is deleted in the first of the list and there is reshuffling to the left.
        """
        self.record.remove(computer)
        
        

        
if __name__ == '__main__':
    
    c1 = Computer("c1", 2, 2, 0.1)
    c2 = Computer("c2", 9, 2, 0.2)
    c3 = Computer("c3", 6, 3, 0.3)
    c4 = Computer("c4", 1, 3, 0.4)
    c5 = Computer("c5", 6, 4, 0.5)
    c6 = Computer("c6", 3, 7, 0.6)
    c7 = Computer("c7", 7, 7, 0.7)
    c8 = Computer("c8", 8, 7, 0.8)
    c9 = Computer("c9", 6, 7, 0.9)
    c10 = Computer("c10", 4, 8, 1.0)
    co = ComputerOrganiser()
    
    #co.add_computers([c1,c2])
    #co.add_computers([c4,c3])
    #co.add_computers([c5])
    #co.add_computers([c7,c9,c6,c8])
    #print([co.cur_position(x) for x in [c1,c2,c3,c4, c5,c6,c7,c8,c9]])
    #print(co.cur_position(c10))
   
    #print(co.cur_position(Computer('test', 0, 0, 1)))
    c1, c2, c3, c4 = Computer("c1", 1, 1, 0.1), Computer("c2", 2, 2, 0.2), Computer("c3", 3, 3, 0.3), Computer("c4", 4, 4, 0.4)
    co.add_computers([c1, c2, c3, c4])
    
    print([co.cur_position(c) for c in [c1,c2,c3,c4]])
    c5, c6, c7, c8, c9, c10 = Computer("b", 7, 0, 0.5), Computer("a", 7, 2, 0.6), Computer("c", 7, 1, 0.7), Computer("c", 8, 20, 0.8), Computer("b", 8, 2, 0.9), Computer("a", 8, 1, 1.0)
    co.add_computers([c5, c6, c7])
    co.add_computers([c8, c9, c10])
    print([co.cur_position(c) for c in [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10]])