# libraries imported
from __future__ import annotations
from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR


K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')


class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes: list | None = None, internal_sizes: list | None = None) -> None:
        if sizes is not None:
            self.TABLE_SIZES = sizes

        if internal_sizes is not None:
            self.internal_sizes = internal_sizes
        else:
            self.internal_sizes = self.TABLE_SIZES

        self.size_index = 0
        self.array: ArrayR[tuple[K1, V] | None] | None = ArrayR(self.TABLE_SIZES[self.size_index])
        self.count = 0

    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31417
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31417
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value

    def _linear_probe(self, key1: K1, key2: K2 | None, is_insert: bool) -> tuple[int, int] | int:
        """
        :description: Find the correct position for this key in the hash table using linear probing.
        :param: key1 (K1) -> DKT's position.
        :param: key2 (K2 | None) -> LPT's position.
        :param: is_insert (bool) -> Choice for searching or inserting.
        :returns: (tuple[int,int] | int) -> Returns the DKT's and LPT's positions or only DKT's position.
        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.
        :best complexity: O(hash1(key1)) -> Where hash1(key1) is the function that hashes the DKT's key to retrieve the position of the element needed. This scenario occurs when the empty spot is found on the first iteration of DKT to create a new LPT associated with key1.
        :worst complexity: O(hash1(key1) + N*comp[==] + hash2(key2) + M*comp[==]) -> Where hash1(key1) is the function that hashes the DKT's position, hash2(key2) hashes the LPT's position, comp[==] is the complexity of object comparisons, N refers to the maximum number of clusters inside DKT and M refers to the maximum number of clusters inside LPT.
        """
        
        # getting the position of DKT.
        dkt_position = self.hash1(key1) # O(len(key1))
        
        # iterate until exhaustion.
        for _ in range(self.table_size):
            
            # if the slot is empty,
            if self.array[dkt_position] is None:
                
                # if we are searching, raise error.
                if not is_insert:
                    
                    raise KeyError(key1)
                
                # if inserting,
                else:
                    
                    # if key2 is not given, return dkt position only.
                    if key2 is None:
                        return dkt_position

                    else:
                        
                        # create a new linear probe table.
                        hash_table = LinearProbeTable(self.internal_sizes) # O(size)
                        hash_table.hash = lambda x: self.hash2(x, hash_table) # O(len)
                        self.array[dkt_position] = (key1, hash_table)
                        
                        lpt_position = hash_table._linear_probe(key2, is_insert)
                        
                        return (dkt_position, lpt_position)
            
            # if a data has been found,
            elif self.array[dkt_position][0] == key1:
                
                # if key2 is not given, return dkt position only.
                if key2 is None:
                    
                    return dkt_position

                else:
                    
                    # return two indexes.
                    hash_table = self.array[dkt_position][1]
                    lpt_position = hash_table._linear_probe(key2, is_insert)
                    return (dkt_position, lpt_position)
            
            # increment, and wrap if possible.
            else:
                
                dkt_position = (dkt_position + 1) % self.table_size

        # if still trying to insert, return fullerror.
        if is_insert:
            raise FullError
        else:
            raise KeyError(key1)

    def iter_keys(self, key: K1 | None = None) -> Iterator[K1 | K2]:
        """
        :description: Returns an iterator of keys.
        :param: key1 (K1 | None) [None] -> DKT key.
        :return: (Iterator[K1 | K2]) -> An iterator object of specified keys.
        :best complexity: O(1) -> Returns the DKT keys one by one. 
        :worst complexity: O( self._linear_probe() + N ) -> Where self._linear_probe() is the function that probes only through the DKT, and N is the maximum number of keys in LPT. In this scenario, the DKT has to probe entirely and returns all of LPT's keys at the final position. 
        """
        
        # if key is none, return DKT keys only.
        if key is None:
            
            for x in range(self.table_size):
                if self.array[x] is not None:
                    yield self.array[x][0]
        
        # otherwise, yield hash table keys.
        else:
            
            # getting the tuple entry.
            tpl_entry = self.array[self._linear_probe(key, None, False)]
            
            yield from tpl_entry[0].keys()

    def iter_values(self, key: K1 | None = None) -> Iterator[V]:
        """
        :description: Returns an iterator of values.
        :param: key (K1 | None) [None] -> Key to determine what values to be returned.
        :return: (Iterator[V]) -> An iterator object of values.
        :best complexity: O( self._linear_probe() + N ) -> The position is found in the first iteration, and the N number of values are returned from the LPT.
        :worst complexity: O( self.keys() * (self._linear_probe() + N) ) -> For each iteration with a given key from a maximum cluster of DKT, the program probes through the entire LPT and returns a list of values in O(N) time where N is the maximum number of clusters in that LPT.
        """
        
        if key is None:
            for k in self.keys():
                yield from self.array[self._linear_probe(k, None, False)][1].values()
        
        else:
            tpl_entry = self.array[self._linear_probe(key, None, False)]
            yield from tpl_entry[1].values()
                        
    def keys(self, key: K1 | None = None) -> list[K1 | K2]:
        """
        :description: Returns the keys of a table-level depending on the key provided.
        :param: key (K1 | None) [None] -> Key that determines the level of the table the keys needed to be retrieved from.
        :return: (list[K1 | K2]) -> A list of DKT keys or LPT keys.
        :best complexity: O(N) -> Where N is the number of keys that are present inside the DKT. In this case, there is only an entire iteration from the starting till the end of DKT to return the DKT keys.
        :worst complexity: O( hash1(key) + N*comp[==] + M ) -> Where hash1(key) is the function that hashes the key, N is the number of maximum clusters within DKT and M is the maximum number of clusters inside LPT. In this scenario, the function linearly probes till the end to find the desired position, and returns the list of LPT keys at that position.
        """
        
        # if no key is given, return only DKT keys.
        if key is None:
            
            res = []
            for x in range(self.table_size):
                if self.array[x] is not None:
                    res.append(self.array[x][0])
            return res
        
        else:
            
            # get the tuple entry
            tpl_entry = self.array[self._linear_probe(key, None, False)]
            
            # return the hash table keys.
            return tpl_entry[1].keys()

    def values(self, key: K1 | None = None) -> list[V]:
        """
        :description: Returns a list of values depending on the key level given.
        :param: key (K1 | None) [None] -> A key for retreiving specific LPT values or all of LPT values.
        :return: (list) -> A list of values.
        :best complexity: O( hash1(key) + M) -> Where hash1(key) is the function that hashes the key, N is the maximum number of clusters in DKT and M is the maximum number of clusters in LPT. The LPT is found with no linear probing in the DKT.
        :worst complexity: O( len(self.keys()) * ( self._linear_probe() + N ) -> Where self.keys is the function that returns the list of DKT keys, self._linear_probe() probes through the DKT only, and N is the complexity of returning the LPT's values. In this scenario, the DKT has maximum number of clusters to iterate from, and the LPT has maximum number of clusters to return values from a particular position.
        """
        
        # if key is not given, return values from all hash tables.
        if key is None:
            
            res = []
            
            for k in self.keys():
                for val in self.array[self._linear_probe(k, None, False)][1].values():
                    res.append(val)
            
            return res
        
        else:
            
            # get the tuple entry
            tpl_entry = self.array[self._linear_probe(key, None, False)]
            
            # return the hash table values.
            return tpl_entry[1].values()

    def __contains__(self, key: tuple[K1, K2]) -> bool:
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

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """

        position1, position2 = self._linear_probe(key[0], key[1], False)
        return self.array[position1][1].array[position2][1]

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """

        key1, key2 = key
        position1, position2 = self._linear_probe(key1, key2, True)
        sub_table = self.array[position1][1]

        if sub_table.is_empty():
            self.count += 1

        sub_table[key2] = data

        # resize if necessary
        if len(self) > self.table_size / 2:
            self._rehash()

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        :description: Deletes a (key, value) pair in our hash table.
        :param: key (tuple[K1 | K2]) - > DKT and LPT keys.
        :raises KeyError: when the key doesn't exist.
        :best complexity: O( self._linear_probe() + self.hash2(K2) ) -> This occurs when the position is found in the first iteration of DKT, and the position is found in the first iteration of LPT, with no probing on both tables.
        :worst complexity: O( N*hash(key2) + N^2*comp[==] + M * self._linear_probe() ) -> This occurs when there is maximum probing of DKT and LPT to find the indexes. In addition, the deletion of element inside LPT is midway through the large chain. Furthermore, if the LPT that is empty is in the midway of all DKT's clusters, it requires M associated tuples below the current position to change its indexes by one up.
        """
        
        dkt_pos, value_pos = self._linear_probe(key[0], key[1], False)
        hash_table = self.array[dkt_pos][1]
        
        del hash_table[key[1]]
        
        if hash_table.is_empty():
            
            curr_pos = self._linear_probe(key[0], None, False)
            
            self.array[curr_pos] = None
            self.count -= 1
            
            curr_pos = (curr_pos + 1) % self.table_size
            
            while self.array[curr_pos]:
                k, lpt = self.array[curr_pos]
                self.array[curr_pos] = None
                
                newpos = self._linear_probe(k, None, True)
                self.array[newpos] = (k, lpt)
                curr_pos = (curr_pos + 1) % self.table_size

    def _rehash(self) -> None:
        """
        :description: Need to resize table and reinsert all values
        :best complexity: O(N * self.hash1(K)) -> Where the loop iterates N times to insert N items into the new hash table and there is no probing. 
        :worst complexity: O(N *  self._linear_probe()) -> Where the loop iterates N times to insert N items into the new hash table and there is maximum number of probing to insert the item into a large clustered LPT.
        """

        old_array = self.array
        self.size_index += 1
        if self.size_index >= len(self.TABLE_SIZES):
            # cannot be resized further.
            return
        self.array = ArrayR(self.TABLE_SIZES[self.size_index])
        self.count = 0
        
        # tuples inside DKT.
        for tpl in old_array:
            if tpl is not None:
                key, lpt = tpl
                self.array[self._linear_probe(key, None, True)] = (key, lpt)

    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        return len(self.array)

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        return self.count

if __name__ == '__main__':

    class TestingDKT(DoubleKeyTable):
        def hash1(self, k):
            return ord(k[0]) % 12
        def hash2(self, k, sub_table):
            return ord(k[-1]) % 5
        
    dt = TestingDKT(sizes=[12], internal_sizes=[5])
    
    """
    dt["Tim", "Jen"] = 1
    dt["Amy", "Ben"] = 2
    dt["May", "Ben"] = 3
    dt["Ivy", "Jen"] = 4
    dt["May", "Tom"] = 5
    dt["Tim", "Bob"] = 6
    dt["May", "Jim"] = 7
    dt["Het", "Liz"] = 8
    """

    dt["Tim", "Jen"] = 1
    dt["Amy", "Ben"] = 2
    dt["Tim", "Kat"] = 3
    
    for x in dt.array[0][1].array:
        print(x)
    
    print()
    del dt["Tim", "Jen"]
    del dt["Tim", "Kat"]
    
    dt["Het", "Bob"] = 4

    for x in dt.array:
        print(x)
        

    
    dt["Tim", "Kat"] = 5
    print(dt._linear_probe("Tim", "Kat", False))
