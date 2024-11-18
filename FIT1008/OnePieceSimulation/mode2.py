from data_structures.heap import MaxHeap
from landsites import Land
from heap_node import HeapNode
from data_structures.referential_array import ArrayR

class Mode2Navigator:
    """
    A class to manage and navigate through a collection of Land objects for obtaining maximum o-score.
    
    Attributes
        sites (MaxHeap): A heap containing Land objects ordered in terms of o-scores.
        sites_temp (ArrayR): An array that keeps track of all land objects inserted to the program.
        n_teams (int): Keeps track of the number of teams in the game.
        
    Behaviours
        __init__(self, n_teams): Initialises the class with the number of teams in the game, and nulls both the heap structure and array structure to store contents later.
        add_sites(self, sites): Adds sites to the array to keep track of the Land objects that could be invaded in the game.
        simulate_day(self, adventurer_size): Simulates the game that runs for a day, involving teams to travel to optimise their o-score earnings.
        compute_score(self, site, adventurers_size): Computes the o-score for a land, the remaining adventurers and gold earned for each team.
        construct_score_data_structure(self, adventurer_size): Constructs the heap with the given array from the class' attribute.
    
    Other methods
        _update_site(self, land, reward_lost, guardians_lost, adventurer_size): Updates the fields of the Land object and the HeapNode within the MaxHeap.
   
    Example
        >>> sites = [ Land('A', 400, 100), Land('B', 750, 120), Land('C', 200, 30) ]
        >>> nav = Mode2Navigator(5)
        >>> nav.add_sites(sites)
        >>> nav.simulate_day(100)
        >>> [(Land(name='B', gold=0, guardians=0), 100), (Land(name='A', gold=0, guardians=0), 100), (Land(name='C', gold=0, guardians=0), 30), (Land(name='B', gold=0, guardians=0), 20), (None, 0)]
        ...
        >>> nav.add_sites([Land('D', 980, 230)])
        >>> nav.simulate_day(80)
        >>> [(Land(name='D', gold=0, guardians=0), 80), (Land(name='D', gold=0, guardians=0), 80), (Land(name='D', gold=0, guardians=0), 70), (None, 0)]
    
    Time Complexity
        __init__() -> O(1)
            - All instance variables are instantiated in O(1) of complexity.
        
        add_sites() -> O(N + S)
            - The method creates a new array of size N + S. >> O(N + S)
            - The method iterates over N items from the old array. >> O(N)
            - The method iterates over S new items from the sites list. >> O(S)
            - Overall: N + S + N + S = 2 * N + 2 * S => O(N + S) as 2 is a constant.
        
        compute_score() -> O(1)
            - The method calculates the o-score of a land, the remaining adventurers, and gold invaded in constant time.
        
        construct_score_data_structure() -> O(N)
            - Creates a new array of size N. >> O(N)
            - Looping through each element to convert it to a HeapNode object. >> O(N)
            - Heapifying the array formed after conversion. >> O(N)
            - Overall: N + N + N = 3 * N => O(N) as 3 is a constant.
        
        simulate_day() -> O(N + K) to O(N + K log N)
            - Creates a Max heap of Heap Node objects. >> O(N)
            - Loops through each team. >> O(K)
            - MaxHeap.get_max()
                - Best case = O(1) -> When the child Heap Node is equal to one of its children.
                - Worst case = O(log N) -> When the child Heap node is smaller than all of its descendants, resulting in sinking to the depth of the heap.
            - Mode2Navigator._update_site()
                - Best case = O(1) -> When the child added to the heap is equal to its parent.
                - Worst case = O(log N) -> When the child added to the heap is the most maximum element, resulting in complete rise to the root.
            - Appending is done after every turn. >> O(1)
            - Overall: O(N + K*(1+1)) = O(N + K) for best case, O(N + K*(log N + log N)) = O(N + K log N) for worst case.
    """

    def __init__(self, n_teams: int) -> None:
        """
        :description: Non-default constructor for the class.
        :param: n_teams (int) -> The number of adventurer teams participating in the game.
        :returns: void.
        
        COMPLEXITY ANALYSIS
        :best/worst complexity: O(1) -> The constructor initialises the states of the instance variables in constant time.
        """
        
        self.sites: MaxHeap = None
        self.sites_temp: ArrayR = None
        self.n_teams: int = n_teams

    def add_sites(self, sites: list[Land]) -> None:
        """
        :description: Behaviour that adds the sites to an array.
        :param: sites (list) -> A list of Land objects.
        :returns: void.
        
        COMPLEXITY ANALYSIS
        :variable: S -> Additional Land objects to be inserted to the array.
        :variable: N -> Existing land objects inside the array.
        :best/worst complexity: O(N + S) -> Where there are new S land objects to be added to the new array of size N + S. The program involves creating a new array in O(N + S) complexity to accomodate space to iterate and insert N items into the array, followed by additonal S new items into the array.
        """
        
        
        # if array is empty, create a new one with length of sites.
        if not self.sites_temp:
            
            self.sites_temp = ArrayR(len(sites))
            
            # traverse through the list to add the items.
            for i in range(len(self.sites_temp)): # O(S)
                self.sites_temp[i] = sites[i]

        # if items already exist.
        else:
            
            # store old array temporarily and create new array.
            old_array = self.sites_temp
            self.sites_temp = ArrayR(len(old_array) + len(sites)) # O(N + S)
            
            # restore old items.
            for _ in range(len(old_array)): # O(N)
                self.sites_temp[_] = old_array[_]
            
            # add new items.
            for i in range(len(sites)): #O(S)
                self.sites_temp[len(old_array) + i] = sites[i]

    def simulate_day(self, adventurer_size: int) -> list[tuple[Land | None, int]]:
        """
        :description: Behaviour that simulates a day of the game.
        :param: adventurer_size (int) -> The total adventurer size for each team.
        :returns: (list) -> A list of tuples that contain where did each team go and how many adventurers they sent.
        
        COMPLEXITY ANALYSIS
        :variable: N -> The number of land objects inside the array.
        :variable: K -> The number of teams playing the game.
        :best complexity: O(N + K) -> This occurs when the max heap construction has been made for the game to be played, and all the HeapNodes have the same o-score which means every time someone get_max() a node, it won't involve the child node to sink since its equal to one of its parents. Same goes with add() as it will just stay in the leaf on the depth of the heap.
        :worst complexity: O(N + K log N) -> This occurs when the max heap construction has been made for the game to be played, and the heap nodes sink down everytime the root node is accessed using get_max() and the updated heap node rises back up to the root due to having a higher o-score than other nodes.
        """
        
        # storing resultant tuples.
        res_tuples: list[tuple[Land | None, int]] = []
        
        # constructing a max heap using the array of Land objects
        self.sites = self.construct_score_data_structure(adventurer_size) # O(N)

        # playing the game with k teams.
        for _ in range(self.n_teams): # O(K)
            
            # resultant tuple to store what Land each team went, with how many adventurers they sent.
            res: tuple[Land | None, int] = (None, 0)
            
            # maximum o-score land retrieved.
            heap_node: HeapNode = self.sites.get_max() # O(1) | O(log N)
            
            # getting the land and o-score
            current_land: Land = heap_node.get_land()
            current_score: float = heap_node.get_score()
            
            # if the o-score from the land is more than the minimum o-score, then invade.
            if current_score > 2.5 * adventurer_size:
                
                # compute the remainining adventurers and gold retrieved.
                result = self.compute_score(current_land, adventurer_size)
                
                # resultant tuple.
                res = (current_land, adventurer_size - result[2])
                
                # updating the sites accordingly.
                self._update_site(current_land, result[1], (adventurer_size - result[2]) , adventurer_size) # O(1) | O(log N)
            
            # append the result to the list.
            res_tuples.append(res)
        
        # return list.
        return res_tuples
            
    def compute_score(self, site: Land, adventurers_size: int) -> tuple[float, float, int]:
        """
        :description: Behaviour that computes o-scores, remaining adventurers, and reward gained for teams.
        :param: site (Land) -> The land to be invaded by the team.
        :param: adventurers_size (int) -> The adventurer total to invade the lands.
        :returns: (tuple) -> A tuple of final land o-score, reward, and remaining adventurers
        
        COMPLEXITY ANALYSIS
        :best/worst complexity: O(1) -> All operations done here are in constant time, making it overall of O(1).
        """
        
        # getting minimum adventurers needed for invasion.
        minimum_adventurers_needed: int = min(site.get_guardians(), adventurers_size)
        
        # getting maximum reward earned.
        try:
            reward_earned: float = min(minimum_adventurers_needed*site.get_gold()/site.get_guardians(), site.get_gold())
        except ZeroDivisionError:
            reward_earned = 0

        # calculating remaining adventurers and o-score
        remaining_adventurers: int = adventurers_size - minimum_adventurers_needed
        o_score: float = 2.5 * remaining_adventurers + reward_earned
        
        # returning calculations.
        return o_score, reward_earned, remaining_adventurers

    def construct_score_data_structure(self, adventurer_size) -> MaxHeap:
        """
        :description: Behaviour that constructs a heap for the simulation.
        :param: adventurer_size (int) -> The total adventurer number to invade a land.
        :returns: (MaxHeap) -> A heap that is ordered based on the o-score yielded by different lands.
        
        COMPLEXITY ANALYSIS
        :variable: N -> The number of land objects present inside the list.
        :best/worst complexity: O(N) -> The method iterates over each item in the list, converting it to a HeapNode item. The array is later heapified in O(N) complexity cost.
        """

        # creating a temporary array of HeapNode objects to be stored inside MaxHeap.
        arr = ArrayR(len(self.sites_temp))
        
        # looping through each Land object and converting it to HeapNode.
        for i in range(len(arr)): # O(N)
            arr[i] = self.sites_temp[i]
            res = self.compute_score(arr[i], adventurer_size)
            arr[i] = HeapNode(arr[i], res[0])
           
        # heapify the array and return a MaxHeap
        return MaxHeap.heapify(points=arr) # O(N)

    def _update_site(self, land: Land, reward_lost: int, guardians_lost: int, adventurer_size: int) -> None:
        """
        :description:  Protected method that updates the fields of a Land object and the heap.
        :param: land (Land) -> The land object fields to be changed.
        :param: reward_lost (int) -> The gold lost as a result of invasion.
        :param: guardians_lost (int) -> The guardians lost as a result of invasion.
        :param: adventurer_size (int) -> The total adventurers being sent to a land.
        :returns: void.
        
        COMPLEXITY ANALYSIS
        :variable: N -> The number of Land objects present inside the heap.
        :best complexity: O(1) -> When the inserted heap node has a smaller or equal o-score value to its parent node, it is just O(1) as it involves constant access to arrays.
        :worst complexity: O(log N) -> When the inserted heap node has a greater o-score value than all of its parent nodes, it rises up to the root.
        """
        # updating land fields.
        land.set_guardians(  land.get_guardians() - guardians_lost )
        land.set_gold( max(0, land.get_gold() - reward_lost ) )
        
        res = self.compute_score(land, adventurer_size)
        self.sites.add(HeapNode(land, res[0])) # O(1) | O(log N)
