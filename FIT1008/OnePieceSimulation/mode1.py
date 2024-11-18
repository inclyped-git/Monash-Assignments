from landsites import Land
from data_structures.bst import BSTInOrderIterator, BinarySearchTree
from algorithms.mergesort import mergesort
from data_structures.node import TreeNode

class Mode1Navigator:
    """
    A class to manage and navigate through a collection of Land objects for obtaining maximum rewards.
    
    Attributes
        sites (BinarySearchTree): A BST containing Land objects sorted by guardians-to-gold ratio.
        total_adventurers (int): Total number of adventurers available for navigation.
        
    Behaviours
        __init__(self, sites, adventurers): Initialises the class with a sorted list of Land objects, append it to the BST and initialise total adventurers.
        select_sites(self): Selects the most optimal path for the navigator based on available adventurers.
        select_sites_from_adventure_numbers(self, adventure_numbers): Calculates the maximum reward acheived from the optimal path taken for each total adventurers.
        update_site(self, land, new_reward, new_guardian): Updates the states of a Land site and re-inserts into the BST.
        
    Other methods
        _create_bst(self, l): Constructs a BST from a sorted list of Land objects.
        _append_to_bst(self, bst, l, start, end, incrementer): Appends items to the BST in a specified order.
        main(): Main method of the class.
    
    Example
        >>> sites = [ Land('A', 500, 100), Land('B', 300, 170), Land('C', 100, 50) ]
        >>> nav = Mode1Navigator(sites, 300)
        >>> nav.select_sites()
        >>> [(Land(name='A', gold=500, guardians=100), 100), (Land(name='C', gold=100, guardians=50), 50), (Land(name='B', gold=300, guardians=170), 150)]
        ...
        >>> nav.select_sites_from_adventure_numbers([130, 500, 230])
        >>> [560.0, 900.0, 741.1764705882354]
        ...
        >>> nav.update_site(sites[1], 350, 450)
        >>> nav.select_sites())
        >>> [(Land(name='A', gold=500, guardians=100), 100), (Land(name='C', gold=100, guardians=50), 50), (Land(name='B', gold=350, guardians=450), 150)]
        ...
        >>> nav.select_sites_from_adventure_numbers([130, 500, 230]))
        >>> [560.0, 872.2222222222222, 662.2222222222222]
    
    Time Complexity
        __init__() -> O(N log N)
            - Used merge sorting algorithm to sort the list of Land objects with the ratio of guardians to gold. >> O(N log N)
            - Added the median Land object to the BST. >> O(log N)
            - Iterated through the elements left to the median Land object. >> O(N log N)
            - Iterated through the elements right to the median Land object. >> O(N log N)
            - Overall: N log N + log N + N log N + N log N = 3 * N log N + log N => O(N log N) as 3 is constant and N log N > log N asymptotically.
        
       select_sites() -> O(1) to O(N)
            - Created an Iterator object to yield values in O(1) time (initial setup complexity not required.)
            - Uses a while loop to return node object at each iteration; minimum adventurers calculation done inside method.
            - Best case = O(1) when the first land site obtained is enough to accomodate all adventurers.
            - Worst case = O(N) when the navigator invades all land sites with enough adventurers.
       
       select_sites_from_adventure_numbers() -> O(A) to O(A * N)
            - Loops through the entire adventurer total list. >> O(A)
            - Best case = O(1) when the first land encountered is enough to accomodate all adventurer totals.
            - Worst case = O(N) when all adventurer totals invade all land sites present in the BST.
            - Overall: O(1 * A) = O(A) for best case, O(A * N) = O(N * A) for worst case.
       
       update_site() -> O(log N)
            - Finds the node to delete and update it back to the BST.
            - O(log N) when the deletion and updating is done at the BST regardless of balance property.
    """

    def __init__(self, sites: list[Land], adventurers: int) -> None:
       """
       :description: Non-default constructor method of the Mode1Navigator class.
       :param: sites (list) -> A list of Land objects to be inserted.
       :param: adventurers (int) -> Total number of adventurers the navigator can have.
       :returns: void.
       
       COMPLEXITY ANALYSIS
       :variable: N -> The number of Land objects present in a list container.
       :best/worst complexity: O(N log N) -> The method sorts the list of Land objects and appends the items to the BST by adding the median object, items left to the median, and items right to the median. We are assuming the depth of a BST is bounded by O(log N), yielding to the complexity being the same for best and worst regardless of balance property.
       """
       
       # sorting the list based on the unique ratio.
       sorted_sites: list[Land] = mergesort(l=sites, key=lambda x: x.get_guardians() / x.get_gold()) # O(N log N)
       
       # initialising states.
       self.sites: BinarySearchTree = self._create_bst(l=sorted_sites) # O(N log N)
       self.total_adventurers: int = adventurers

    def select_sites(self) -> list[tuple[Land, int]]:
        """
        :description: Behaviour that selects the most optimal path for the navigator to go through.
        :param: void.
        :returns: (list) -> A list of tuples that contains the Land objects visited with the optimal number of adventurers sent.
        
        COMPLEXITY ANALYSIS
        :variable: N -> Number of Land objects present inside the BST.
        :best complexity: O(1) -> When the deepest left leaf node contains a Land object with greater than or equal to the total adventurers that the navigator has. The method will stop the while loop after one iteration.
        :worst complexity: O(N) -> When the navigator has enough adventurers to visit all the Lands to collect gold. This involves the method travelling towards all the N nodes present inside the BST.
        """
        
        # storing the final list of tuples.
        res_tuples: list[tuple[Land, int]] = []
        
        # keeping track of the adventurers.
        remaining_adventurers: int = self.total_adventurers

        # creating an iterator.
        bst_iter: BSTInOrderIterator = iter(self.sites)
        
        # loop while there are adventurers remaining.
        while remaining_adventurers > 0: # O(N)
            
            # initial state of site.
            site_node: TreeNode[float, Land] = None
            
            # try to fetch the next node or stop iteration if exhausted.
            try:
                site_node = next(bst_iter) # Amortized O(1)
            except (StopIteration):
                return res_tuples
            
            # calculating optimal adventurers needed for invasion.
            minimum_adventurers_required: int = min(remaining_adventurers, site_node.item.get_guardians())
            
            # append and update.
            res_tuples.append((site_node.item, minimum_adventurers_required))
            remaining_adventurers -= minimum_adventurers_required

        # return final optimal path.
        return res_tuples    

    def select_sites_from_adventure_numbers(self, adventure_numbers: list[int]) -> list[float]:
        """
        :description: Behaviour that calculates the maximum reward acheived from the optimal path taken.
        :param: adventure_numbers (list) -> A list of total adventurers.
        :returns: (list) -> A list of maximum rewards.
        
        COMPLEXITY ANALYSIS
        :variable: N -> The number of land sites available in the BST.
        :variable: A -> The number of total adventurer elements in the list container.
        :best complexity: O(A) -> When the deepest leaf node contains a land site that is enough to accomodate all the adventurers in all iterations of the adventure_numbers list.
        :worst complexity: O(N * A) -> When every member from the adventure_numbers list contain with enough members to be able to invade all the land sites present in the BST. This means it iterates over N sites present in the BST.
        """
        
        # storing the maximum gold reward acheived.
        res_rewards: list[float] = []
        
        # storing the instance variable total_adventurers temporarily.
        temp: int = self.total_adventurers
        
        # iterate through each total adventurer element.
        for current_advs in adventure_numbers: # O(A)
            
            # reusing self.sites() to calculate reward
            self.total_adventurers = current_advs
            optimal_path: list[tuple[Land, int]] = self.select_sites() # O(1) | O(N)
            
            # calculating the reward achieved.
            total_reward: float = 0
            
            for (land, adv) in optimal_path:
                
                # calculating and rounding.
                reward: float = min(adv * land.get_gold()/land.get_guardians(), land.get_gold())
                total_reward += reward
            
            res_rewards.append(total_reward)
        
        # restoring state.
        self.total_adventurers = temp

        return res_rewards
    
    def update_site(self, land: Land, new_reward: float, new_guardians: int) -> None:
        """
        :description: Behaviour that updates the state of the Land site.
        :param: land (Land) -> Land site to be updated.
        :param: new_reward (float) -> New amount of gold present.
        :param: new_guardians (int) -> New amount of guardians.
        :returns: void.
        
        COMPLEXITY ANALYSIS
        :variable: N -> The number of land sites inside the BST.
        :best/worst complexity: O(log N) -> The land site is found at the the BST, updated, and inserted back at the BST. We are still assuming that the depth of BST is bounded by O(log N), making the worst and best case complexity the same regardless of balance property.
        """
        
        # getting the land object from the bst.
        key: float = land.get_guardians() / land.get_gold()
        del self.sites[key] # O(log N)
        
        # updating the land object.
        land.gold = new_reward
        land.guardians = new_guardians
        
        # adding the land back to the bst with the new key.
        key = land.get_guardians() / land.get_gold()
        self.sites[key] = land # O(log N)
    
    def _create_bst(self, l: list[Land]) -> BinarySearchTree:
        """
        :description: Protected method to construct a BST for self.sites.
        :param: l (list) -> A list of Land objects.
        :returns: (BinarySearchTree) -> A BST of Land objects.
        
        COMPLEXITY ANALYSIS
        :variable: N -> The number of Land objects present in a list container.
        :best/worst complexity: O(N log N) -> The method appends the median Land object first, and then iterates over items left to the median, and then iterates over items right to the median. We are assuming the depth of BST is always bounded by O(log N), making the complexity case the same for best/worst.
        """
        
        # creating a resultant bst.
        res_bst: BinarySearchTree = BinarySearchTree()
        
        # finding the median value to serve as root node.
        median_index: int = len(l) // 2
        
        # create and put root node.
        item = l[median_index]
        key = item.get_guardians() / item.get_gold()
        
        res_bst[key] = item
        
        # put the rest of the elements accordingly.
        self._append_to_bst(bst=res_bst, l=l, start=median_index-1, end=-1, incrementer=-1) # O(N log N)
        self._append_to_bst(bst=res_bst, l=l, start=median_index+1, end=len(l), incrementer=1) # O(N log N)
        
        return res_bst
    
    def _append_to_bst(self, bst:BinarySearchTree, l: list[Land], start: int, end: int, incrementer: int) -> None:
        """
        :description: Protected method to append items to the BST.
        :param: bst (BinarySearchTree) -> The BST of items to be returned.
        :param: l (list) -> A list of Land objects.
        :param: start (int) -> Starting index of the list.
        :param: end (int) -> Ending index of the list.
        :param: incrementer (int) -> Step variable to increment.
        :returns: void.
        
        COMPLEXITY ANALYSIS
        :variable: N -> The number of Land objects present in a list container.
        :best/worst complexity: O(N log N) -> The method iterates over N land objects and adds them to the BST. We are assuming the depth of BST is bounded by O(log N) so the complexity case will be the same for best/worst.
        """
        # looping through the list before/after the median.
        for i in range(start, end, incrementer): # O(N)
            
            # adding nodes to the bst.
            item = l[i]
            key = item.get_guardians() / item.get_gold()
            bst[key] = item # O(log N)
