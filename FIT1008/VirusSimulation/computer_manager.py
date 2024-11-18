from __future__ import annotations
from computer import Computer

from computer_organiser import ComputerOrganiser
from double_key_table import DoubleKeyTable

class ComputerManager:

    def __init__(self) -> None:
        self.dict = DoubleKeyTable()
        self.dict.hash1 = lambda x : x % self.dict.table_size
        self.organiser = ComputerOrganiser()

    def add_computer(self, computer: Computer) -> None:
        """
        best complexity = (N * comp(computer) + hash1(key) + hash2(key)) ->  Where a new computer is added to the computer list of the organiser, and a new entry is added to the DKT by finding a position in the first iteration in both the existing DKT and LPT.
        worst complexity = (N * comp(computer) + hash1(key) + N*comp[==] + hash2(key) + M*comp[==]) -> Where a new computer is added to the computer list of the organiser, and a new entry is added by maximum number of probing in both the DKT and there is maxiumum probing in LPT to retrieve the position to insert the entry.
        """
        self.organiser.add_computers([computer])
        self.dict[(computer.hacking_difficulty, computer.name)] = computer

    def remove_computer(self, computer: Computer) -> None:
        """
        best complexity = O(dict._linear_probe() + dict.hash2(key) ) -> Where the computer is deleted at the end of the list with no reshuffling of elements, and the position is found in the first iteration of DKT and the LPT with no probing in order to delete the entry inside the dict.
        worst complexity = O(L + N*hash(key2) + N^2*comp[==] + M * self._linear_probe() ) -> Where the computer is deleted at the start of the list, and requires L elements to shift to the left. In addition, there is a maximum number of probing in DKT and LPT to find the indexes to delete. The deletion of the element inside LPT is midway through the large chain. Furthermore, if the LPT that is in the midway of the DKT's clusters, it requires the associated tuples to move back to their new indexes.
        """
        self.organiser.remove_computer(computer)
        del self.dict[(computer.hacking_difficulty, computer.name)]

    def edit_computer(self, old: Computer, new: Computer) -> None:
        """
        complexity = O( add_computer() + remove_computer() )
        """
        self.remove_computer(old)
        self.add_computer(new)
        
    def computers_with_difficulty(self, diff: int) -> list[Computer]:
        """
        complexity = O( hash(key) + M ) -> Where the position of the target computers are found with linear probing in the dict DKT, and it returns M number of values that are stored within that position.
        """
        try:
            return self.dict.values(diff)
        except:
            return []

    def group_by_difficulty(self) -> list[list[Computer]]:
        """
        complexity = ( M *( hash(key) + M ) + ( dict._linear_probe() + N ) ) -> There is a maximum number of probing in the DKT to return the list of all DKT keys, and adds up with the complexity of computers_with_dfficulty() function.
        """
        res = []
        for level in self.dict.iter_keys():
            res.append(self.computers_with_difficulty(level))
        return res

if __name__ == '__main__':
    
    c1 = Computer("c1", 4, 4, 0.1)
    c2 = Computer("c2", 3, 2, 0.2)
    c3 = Computer("c3", 3, 5, 0.3)
    c4 = Computer("c4", 4, 3, 0.4)
    c5 = Computer("c5", 3, 4, 0.5)
    c6 = Computer("c6", 5, 3, 0.6)
    c7 = Computer("c7", 5, 3, 0.7)
    c8 = Computer("c8", 6, 4, 0.8)
    c9 = Computer("c9", 6, 4, 0.9)
    c10 = Computer("c10", 4, 5, 1.0)
    
    cm = ComputerManager()
    cm.add_computer(c1)
    cm.add_computer(c2)
    cm.add_computer(c3)
    cm.add_computer(c6)
    cm.add_computer(c7)
    
    print(set(id(x) for x in cm.computers_with_difficulty(3)))
    print(set(id(x) for x in [c2,c3]))
    
    print(set(id(x) for x in cm.computers_with_difficulty(4)))
    print(set(id(x) for x in [c1]))
    print(set(id(x) for x in cm.computers_with_difficulty(7)))
    print(set(id(x) for x in []))
    
    cm.add_computer(c4)
    cm.add_computer(c5)
    cm.add_computer(c8)
    cm.add_computer(c9)
    
    res = cm.group_by_difficulty()
    print(len(res))
    
    print(set(id(x) for x in res[0]))
    print(set(id(x) for x in [c2,c3,c5]))
    
    print(set(id(x) for x in res[1]))
    print(set(id(x) for x in [c1,c4]))
    
    print(set(id(x) for x in res[2]))
    print(set(id(x) for x in [c6,c7]))
    
    print(set(id(x) for x in res[3]))
    print(set(id(x) for x in [c8,c9]))
    
    cm.add_computer(c10)
    cm.remove_computer(c9)
    
    res = cm.group_by_difficulty()
    print(len(res))
    print(set(id(x) for x in res[3]))
    print(set(id(x) for x in [c8]))
   