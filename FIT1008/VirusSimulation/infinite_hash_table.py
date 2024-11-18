# libraries imported
from __future__ import annotations
from typing import Generic, TypeVar
from data_structures.referential_array import ArrayR


K = TypeVar("K")
V = TypeVar("V")


class InfiniteHashTable(Generic[K, V]):
    """
    Infinite Hash Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    TABLE_SIZE = 27

    def __init__(self, level: int = 0) -> None:
        self.array: ArrayR[tuple[K, V] | None] = ArrayR(self.TABLE_SIZE)
        self.count = 0
        self.level = level
    
    def hash(self, key: K) -> int:
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE-1)
        return self.TABLE_SIZE-1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        
        best = O(1) when we are in first IHT
        worst = O(N + M*hash(key)) when we are looping through M IHTs, and iterating through N positions collected in a positions list.
        """
        
        list_of_positions = self.get_location(key)
        curr = self
        for position in list_of_positions:
            curr = curr.array[position][1]
        
        return curr

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        
        best = O(hash(key)) -> Where there is only one IHT to iterate through, and adding the tuple within that.
        worst = O( N*(hash(key)) + size ) -> Where there are N IHTs to iterate through, and creating a new IHT of length *size*, as a result of matching letter keys at a particular level.
        """
        
        curr = self
        position = curr.hash(key)
        
        while curr.array[position]:
            
            if not isinstance(curr.array[position][1], InfiniteHashTable):
                
                key1, value1 = curr.array[position]
                next_ht = InfiniteHashTable(curr.level+1)
                next_ht[key1] = value1
                next_ht[key] = value
                
                curr.array[position] = ( key[:curr.level+1] + "*", next_ht)
                self.count += 1
                return
            
            else:
                
                curr = curr.array[position][1]
                position = curr.hash(key)
                
        curr.array[position] = (key, value)
        self.count += 1

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.
        :raises KeyError: when the key doesn't exist.
        :best complexity: O(1) -> Where the item to delete is existent within the first IHT.
        :worst complexity: O(N^3(hash(key)) -> Where the program gets the locations of indexes, iterates till the last IHT, and deletes the item. If there is only one item that is not * key in the last IHT, it will traverse back to the IHT after self as there will be no conflict.
        """
        
        # gets all the probed locations from starting to the location of the key.
        all_positions = self.get_location(key)
        
        # start from the top
        curr = self
            
        # marker variable to iterate backwards when reforming infinte hash tables.
        idx = 0
        
        # retrieving the hash table that the key is inside.
        for idx in range(len(all_positions) - 1):
            
            curr = curr.array[all_positions[idx]][1]
            
        # deleting the target key area.
        curr.array[all_positions[-1]] = None
        self.count -= 1
        
        # reforming the hash tables if * keys are removed.
        to_delete = True
        while to_delete:
            
            # stop reverse iteration if reached the top table.
            if curr is self:
                break
            
            # keeping track of the tuple entry and the number of elements inside the array.
            tpl_entry = None; num_of_elements = 0
            for _ in curr.array:
                
                # if an entry exists,
                if _ is not None:
                    
                    # if there is a * included, dont reform; otherwise, reform the tables.
                    if _[0][-1] != '*':
                        tpl_entry = _
                        num_of_elements += 1
            
            # if there is at most one element and the entry exists,
            if num_of_elements <= 1 and tpl_entry:
                
                # store the key and value temporarily
                key1, value1 = tpl_entry
                
                # back iteration from target level to level 0
                prev = self
                
                # goes back to one level down.
                for pos in all_positions[:idx]:
                    prev = prev.array[pos][1]
                    
                # deletes the non * key.
                prev.array[all_positions[idx]] = None
                self.count -= 1
                
                # current becomes the prev
                curr = prev

                idx -= 1
                
                # replace the top level value with value extracted from the target table.
                self[key1] = value1
            
            # otherwise, skip deletion.
            else:
                to_delete = False

    def __len__(self) -> int:
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        raise NotImplementedError()

    def get_location(self, key) -> list[int]:
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.
        
        # Best case: O(1), when it is inside FIRST IHT.
        # Worst case: O(n*hash(key)), when you reach the last IHT.
        """
        
        # current hash table.
        curr = self
        
        # list to store indexes.
        lst = []
        
        final = None
        
        while isinstance(curr, InfiniteHashTable):
            
            # array of current hash table.
            array = curr.array
            
            # hash the key according to the level it is right now.
            position = curr.hash(key)
            
            if array[position] is None:
                
                raise KeyError
            
            lst.append(position)
            curr = array[position][1]
            
            final = array[position]
        
        if final[0] != key:
            raise KeyError
            
        
        return lst
            
    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def sort_keys(self, current=None) -> list[str]:
        """
        Returns all keys currently in the table in lexicographically sorted order.
        complexity = O(_auxiliary_sort_keys)
        """
        
        current = self if not current else current

        # list of sorted keys.
        sorted_keys = []
        
        sorted_keys = self._auxiliary_sort_keys(current, sorted_keys)
        return sorted_keys
    
    def _auxiliary_sort_keys(self, curr, sorted_keys):
        
        """
        complexity = O(TABLE_SIZE * N) -> Where N is the number of tables we iterate through to accumulate all values inside the IHTs.
        """
        
        # usually the key same name as * key are stored in the last of the array, so we are only storing the non * one.
        if curr.array[curr.TABLE_SIZE - 1] and curr.array[curr.TABLE_SIZE - 1][0][-1] != '*':
            sorted_keys.append(curr.array[curr.TABLE_SIZE - 1][0])
        
        # start lexicographically sort from a to z.
        start = ord('a') % (curr.TABLE_SIZE - 1)
        
        for _ in range(curr.TABLE_SIZE):
            tpl_entry = curr.array[start]
            
            if tpl_entry and start != curr.TABLE_SIZE - 1:
                key, val = tpl_entry
                
                if '*' in key:
                    self._auxiliary_sort_keys(val, sorted_keys)
                else:
                    sorted_keys.append(key)
            

            start = (start + 1) % curr.TABLE_SIZE

        return sorted_keys
           
if __name__ == '__main__':
    
    ih = InfiniteHashTable()
    ih['lin'] = 1
    ih["leg"] = 2
    ih["mine"] = 3
    ih["linked"] = 4
    ih["limp"] = 5
    ih["mining"] = 6
    ih["jake"] = 7
    ih["linger"] = 8
    
    print(ih.sort_keys())
    