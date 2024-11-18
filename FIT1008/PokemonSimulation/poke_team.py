
from pokemon import *
import random
from battle_mode import BattleMode
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.bset import BSet

class PokeTeam:
    TEAM_LIMIT: int = 6 # team limit
    POKE_LIST: ArrayR = get_all_pokemon_types() # list of all Pokemon types
    CRITERION_LIST: list[str] = ["health", "defence", "battle_power", "speed", "level"] # criterion list

    def __init__(self):
        """
        __description__: Constructor the PokeTeam class.
        """
        self.team: object = None # the actual team, the one with chosen ADTs.
        self.team_count: int = 0 # the number of pokemons chosen.
        self.selected_pokemons: ArrayR = ArrayR(PokeTeam.TEAM_LIMIT) # the pokemons chosen for the trainer.
        self.health_records: ArrayR = ArrayR(PokeTeam.TEAM_LIMIT) # the pokemons' health records.
        self.list_reversed: bool = False # restricts the entry of data in a particular order.
     
    def __getitem__(self, index: int) -> Pokemon:
        """
        __description__: Returns the object in position index.

        __params__:
                    index (int): The position of the object

        __returns__:
                     Pokemon: The Pokemon stored in position index.
        
        __complexity__: BEST CASE: O(1), due to the self.team being a normal arrayR or an arraysortedlist. We can get access directly to the
                        elements with their indexes.
                        
                        WORST CASE: O(N), due to the self.team being a stack or queue. We need to pop/serve out all N elements, and then directly 
                        access them with the functions' return value.
        
        __annotations__: Complexities are denoted by O(best case) | O(worst case)
        """
        
        # if self.team is neither of the ADT, it is a normal array.
        if not isinstance(self.team, (ArrayStack, CircularQueue, ArraySortedList)): # O(isinstance): The complexity of the isinstance() method.
            return self.selected_pokemons[index] 
        
        # if self.team is an arraystack
        if isinstance(self.team, ArrayStack): # O(isinstance): The complexity of the isinstance() method.
            return self._retrieve_stack_elements()[index] # Best = O(1), Worst = O(n)
        
        # if self.team is an circularqueue
        elif isinstance(self.team, CircularQueue): # O(isinstance): The complexity of the isinstance() method.
            return self._retrieve_queue_elements()[index] # Best = O(1), Worst = O(n)
        
        # otherwise, it must be arraysortedlist
        return self.team[index].value

    def __len__(self) -> int:
        """
        __description__: Returns the number of Pokemons inside self.team.
        
        __returns__:
                     int: The number of Pokemons inside self.team.
        """
        
        # if the self.team is a normal array
        if not isinstance(self.team, (ArrayStack, ArraySortedList, CircularQueue)):
            return self.team_count
        
        # if it is an ADT
        else:
            return len(self.team)

    def __str__(self) -> str:
        """
        __description__: Returns the string representation of self.team.

        __returns__:
                    str: A String that represents the Pokemons stored inside self.team
        
        __complexity__: BEST CASE: O(1), due to the self.team being a normal array with zero to few elements to be iterated and processed.
                        Due to a restricted number of iterations, this function will run in constant time. Since O(isinstance) can vary from
                        time to time, the functions's tight upper bound will exclude its complexity.
                        
                        WORST CASE: O(N * comp(concatenation)), due to the self.team containing N number of pokemons to be processed and iterated.
                        As the number of pokemons grow, the computation required to iterate and concatenate the strings will grow linearly which makes
                        the complexity grow linearly with respect to the number of pokemons inside self.team.
        
        __annotations__: Complexities are denoted by O(best case) | O(worst case)
        """
        # Temporary variable to store Pokemons, and a String to store the list of Pokemons.
        temp_array: object = None
        length: int = 0
        final_string: str = ""
        
        # Determining the Data Structure used for self.team
        if isinstance(self.team, (ArrayStack, ArraySortedList, CircularQueue)): # O(isinstance): The complexity of the isinstance() method.
        
            # If the self.team is an ArrayStack,
            if isinstance(self.team, ArrayStack): # O(isinstance): The complexity of the isinstance() method.
                temp_array = self._retrieve_stack_elements() # Best = O(1), Worst = O(n)
        
            # If the self.team is an CircularQueue,
            elif isinstance(self.team, CircularQueue): # O(isinstance): The complexity of the isinstance() method.
                temp_array = self._retrieve_queue_elements() # Best = O(1), Worst = O(n)
            
            # If the self.team is an ArraySortedList,
            elif isinstance(self.team, ArraySortedList): # O(isinstance): The complexity of the isinstance() method.
                temp_array = self.team
            
            length = len(self.team)
        
        # If we are accessing the normal array,
        else: # O(isinstance): The complexity of the isinstance() method.
            temp_array = self.selected_pokemons
            length = self.team_count
        
        
        # Final string to output the Pokemon details.
        for index in range(length): # Best = O(1), Worst = O(n)
            
            # O(concatenation): Computation time to concatenate strings.
            final_string += f"{index + 1}. {temp_array[index]}\n" if not isinstance(self.team, ArraySortedList) else f"{index + 1}. {temp_array[index].value}\n"
        
        # Returning string.
        return final_string  

    def choose_manually(self) -> None:
        """
        __description__ : Enables the user to choose Pokemons of their choice manually, up to the team limt.
        
        __complexity__: BEST CASE: O(1), due to the team limit being 0 or a small integer. If there is a small integer team limit,
                        then the computations depend on the number of failures the user faces when inputting data. By assumption of 
                        user inputting the correct data at all times, the function will run in constant time with predefined limit.
                        
                        WORST CASE: O(N), due to the team limit being N. By assumption of the fact that the inputs will be right, the
                        computation will only grow in linear time as the team limit increases. By taking into account of the number of 
                        validation checks, the function will continue to increase in O(N * comp(failures)) complexity, with both complexities
                        growing linearly assuming both the team limit and the number of failures will increase linearly.
        
        __annotations__: Complexities are denoted by O(best case) | O(worst case)
        """
        
        # calling the constructor to reset attributes of the object.
        PokeTeam.__init__(self)
        
        # calling the string representation function to print the options.
        print(PokeTeam._generate_string_options()) # O(1): POKE LIST is empty or has a few elements | O(N * comp(concatenation)): POKELIST has N elements and concatenates N details.
        
        # running the while loop until the team reached its limit.
        while self.team_count < self.TEAM_LIMIT: # O(1): team limit is 0 or a small integer. | O(N): team limit is N number of pokemons.
            
            # this section will cover the correct input of the options.
            
            # flag variable to indicate if the input is correct or wrong.
            correct_num: bool = False
            
            while not correct_num: # O(failures): Depends on the user inputs.
                
                # try-catch to get the correct number
                try:
                    
                    input_num: int = int(input('Please enter your choice [1-77]')) 
                    assert 1 <= input_num <= len(PokeTeam.POKE_LIST)
                    
                    # if it successfully passes the checks, add it to selected_pokemons.
                    self.selected_pokemons[self.team_count] = self.POKE_LIST[input_num - 1]()
                    self.health_records[self.team_count] = self.selected_pokemons[self.team_count].get_health()
                    self.team_count += 1
                                   
                    # breaks the loop if validations are passed.
                    correct_num = True
                    
                # if the input data type is incorrect
                except ValueError:
                    print('Please enter a number between 1-77 only.')
                
                # if the input range is incorrect
                except AssertionError:
                    print('You are out of range. Please enter a number between 1 to 77 only!')
            
            # early exit if the team limit has been reached.
            if self.team_count == self.TEAM_LIMIT:
                print('You have reached the team limit.')
                break
            
            # this section will cover  whether user wants to stop adding more Pokemon or not.
            
            # flags to control the while loop and breaking the outer while loop.
            correct_option: bool = False
            choose_more: bool = True
            
            while not correct_option: # O(failures): Depends on the user inputs.
                try:
                    option: str = input('Do you want to add more Pokemons or no? [Y/N] - ')
                    assert option.lower() == 'y' or option.lower() == 'n'
                    
                    # breaks the while loop.
                    correct_option = True
                    
                    choose_more = False if option ==  'n' else True
                    
                except AssertionError:
                    print('You might have mispelled or entered data incorrectly. Enter only "Y" or "N" please.')
            
            # if user wants to exit, break the loop.
            if not choose_more:
                break

    def choose_randomly(self) -> None:
        
        PokeTeam.__init__(self)
        
        for i in range(self.TEAM_LIMIT):
            rand_int = random.randint(0, len(self.POKE_LIST)-1)
            self.selected_pokemons[i] = self.POKE_LIST[rand_int]()
            self.health_records[i] = self.selected_pokemons[i].get_health()
            self.team_count += 1

    def regenerate_team(self, battle_mode: BattleMode, criterion: str = None) -> None:
        """
        __description__: Regenerates health of all the pokemons the trainer chose.

        __params__:
                    battle_mode (BattleMode): The current battle mode that the trainers are fighting.
                    criterion (str, optional): An optional parameter used to order the pokemons inside an arraysortedlist.
        
        __complexity__: BEST CASE: O(1), if the number of pokemons are limited, and requires assembly of one pokemon to a team only.
                        WORST CASE: O(N) if the number of pokemons are N. Additional overhead may arrive from the computations of assemble_team().
        """
        
        # iterating through the array of pokemons chosen, and regenerating their healths.
        for index, pokemon in enumerate(self.selected_pokemons): # O(1): The selected pokemons are 0 or few numbers | O(N): The number of selected pokemons is N.
            pokemon.health = self.health_records[index]
        
        # assembling the team
        self.assemble_team(battle_mode, criterion) # O(1): If the team assembled consists of one pokemon only. | O(N) for SET and ROTATE and O(N^2) for OPTIMISE.

    def assign_team(self, criterion: str = None) -> None:
        """
        __description__: Assembles the team for ArraySortedList teams based on a given criterion.

        __params__:
                    criterion (str, optional): The criterion used to order the elements in the team.
        
        __complexity__: ADDING TO FRONT:
                            - BEST CASE: O(1) if the team has 0 elements, and only requires only one element to be added to the list.
                            - WORST CASE: O(N^2) if the team has N elements, and require N-1 elements to be shifted to the right when adding
                                          the pokemon to the front of the list.
                        
                        ADDING TO BACK:
                            - BEST CASE: O(1) if the team has 0 elements, and only requires one element to be added to the list. It is O(log N) if the team has N elements.
                            - WORST CASE: O(N*logN) if the team has N elements, and won't require any shifts to the right. So the only
                                          highest order complexity in adding elements is O(log N), and iterating N times to give the worst 
                                          case.
                        
                        OVERALL COMPLEXITY:
                            - BEST CASE: O(1) if the team only needs to store 1 pokemon. 
                            - WORST CASE: O(N^2) if the team stores the pokemon in the front of the list.
        
        __annotations__: Complexities are denoted by O(best case) | O(worst case).
        """
            
        # iterate through the whole selected pokemons array.
        for pokemon in self.selected_pokemons: # O(1): If the selected pokemons array contain no elements or 1 element | O(N): the selected pokemons array contains N pokemons.
            
            # finds the key and adds the pokemon to the team.
            key = self._get_criterion_key(pokemon, criterion)
            
            if self.list_reversed: 
                self.team.add(ListItem(value=pokemon, key= 1 / key)) # O(1): adding the pokemon to an empty list | # O(N): adding pokemon to far left, and shuffling rest of the elements to the right.
            else:
                self.team.add(ListItem(value=pokemon, key= key)) # O(1): adding the pokemon to an empty list | # O(N): adding pokemon to far right, and shuffling rest of the elements to the left.
    
    def assemble_team(self, battle_mode: BattleMode, criterion: str = None) -> None:
        """
        __description__: Assembles the teams for a given battle mode.

        __params__:
                    battle_mode (BattleMode): The current battle mode the trainer is fighting in.
                    criterion (str, optional): The criteria used for ordering the teams in OPTIMISE.
        
        __complexity__: SET MODE: 
                            - BEST CASE: O(1), where the team count is 1 and there is only one pokemon in the team.
                            - WORST CASE: O(N), where the team count is N and there are N pokemons in the team to be pushed.
                        
                        ROTATE MODE:
                            - BEST CASE: O(1), where the team count is 1 and there is only one pokemon in the team.
                            - WORST CASE: O(N), where the team count is N and there are N pokemons in the team to be appended.
                        
                        OPTIMISE MODE:
                            - BEST CASE: O(1), where the team count is 1 and there is only one pokemon in the team.
                            - WORST CASE: O(N^2), where the team count is N and adding element to the left will result in N elements
                              to shift to the right in O(N) time.
                        
                        OVERALL COMPLEXITY:
                            - BEST CASE: O(1) across all modes when only dealing with single Pokemon.
                            - WORST CASE: O(N) for SET and ROTATE modes, while O(N^2) for OPTIMISE mode.

        __annotations__: Complexities are denoted by O(best case) | O(worst case).
        """
        
        # if the battle mode is SET
        if battle_mode.value == 0:
            self.team = ArrayStack(self.team_count) # O(1): Only one element to be stored | O(N): N number of pokemons to be stored.
            
            # the last appearing pokemon should pop out first.
            for pokemon in self.selected_pokemons: # O(1): Only one iteration to be done | O(N): N number of iterations to be done.
                self.team.push(pokemon)
        
        # if the battle mode is ROTATE
        elif battle_mode.value == 1:
            self.team = CircularQueue(self.team_count) # O(1): Only one element to be stored | O(N): N number of pokemons to be stored.
            
            for index in range(self.team_count): # O(1): Only one iteration to be done | O(N): N number of iterations to be done.
                self.team.append(self.selected_pokemons[index])

        # if the battle mode is OPTIMISE
        else:
            self.team = ArraySortedList(self.team_count) # O(1): Only one element to be stored | O(N): N number of pokemons to be stored.
            self.assign_team(criterion) # O(1): Only one element to be added | O(N^2): N elements added to the front of the team with N elements.
            
    def special(self, battle_mode: BattleMode) -> None:
        """
        __description__: Special function for the trainer team.

        __params__:
                    battle_mode (BattleMode): The battle mode that is currently being played.
        
        __complexity__: They are defined in respective functions. Please check the docstring of defined functions.
        """
        
        # if it is a SET battle
        if battle_mode.value == 0:
            self._special_method_set()
        
        # if it is a ROTATE battle
        elif battle_mode.value == 0:
            self._special_method_rotate()
        
        # if it is an OPTIMISE battle
        else:
            self._special_method_optimise()

    @classmethod
    def _generate_string_options(cls) -> str:
        """
        __description__ : Generates a string containing options for user input.

        __returns__ :
                        str: String representation of the options.
        
        __complexity__: BEST CASE: O(1), due to the POKE_LIST being empty. If there is a fixed number of pokemons, then we need to consider
                        only the computation cost of concatenation ( O(concatenation) ). Considering all the possible cases, the case where
                        the poke list is empty is by far the most fastest in terms of computations.
                        
                        WORST CASE: O(N * comp(concatenation)), due to the N number of pokemons being present in the poke list, and the
                        computation cost required to concatenate Strings as they grow can be denoted with O(concatenation).
        
        __annotations__: Complexities of each line will be denoted by O(best case) | O(worst case)
        """
        
        # final variable to store all of the pokemon options.
        final_string: str = "This is the list of Pokemons to choose from:\n"
        
        # concatenating each pokemon class 
        for index, class_reference in enumerate(cls.POKE_LIST): # O(1): There is no types to iterate or few types to iterate | O(N): There are N types to iterate through.
            
            final_string += f"{index + 1}. {class_reference().get_name()}\n" # O(concatenation): Computation cost for concatenation.
            
        # returning the final String.
        return final_string
        
    def _get_criterion_key(cls, pokemon: Pokemon, criterion: str = None) -> float:
        """
        __description__: Finds the criterion key required to be added with the pokemon inside the
                         arraysortedlist.

        __params__:
                    pokemon (Pokemon): The pokemon to be added to the list.
                    criterion (str, optional): The criterion required to order the list.

        __raises__:
                    ValueError: If the incorrect criterion is given, it raises an error.

        __returns__:
                    float: The value associated with the criterion key.
        """
        
        # if the criterion is based on health
        if criterion == "health" or criterion is None:
            return pokemon.get_health()
            
        # if the criterion is based on defence
        elif criterion == "defence":
            return pokemon.get_defence()
        
        # if the criterion is based on battle power
        elif criterion == "battle_power":
            return pokemon.get_battle_power()
            
        # if the criterion is based on speed
        elif criterion == "speed":
            return  pokemon.get_speed()
            
        # if the criterion is based on level
        elif criterion == "level":
            return pokemon.get_level()

        # raise an error otherwise
        else:
            raise ValueError('Invalid criterion')
    
    def _retrieve_stack_elements(self) -> ArrayR:
        """
        __description__: Retrieves the elements within a stack, and pushes the elements back into the stack while
                         retaining its order.

        __returns__:
                     ArrayR: An array of elements popped from the stack.
                     
        __complexity__: BEST CASE: O(1), due to the stack being empty or containing minimal number of elements.
                        WORST CASE: O(N), due to the stack containing N number of Pokemons to pop and push back.

        __annotations__: Complexities of each line will be denoted by O(best case) | O(worst case)
        """
        
        # temporary array to store the Pokemon objects.
        i: int = 0
        temp_array: ArrayR = ArrayR(len(self.team)) if len(self.team) > 0 else None # O(1): If team has no elements, or has few elements. | O(N): if there N Pokemons in the stack.
        
        # printing empty stack results.
        if temp_array is None:
            print("The team is currently empty.")
        
        # tracking elements inside the stack, and storing them in a temporary array.
        while not self.team.is_empty(): # O(1): If the team has no elements or has a few elements | O(N): If the team has N pokemons inside the stack.
            temp_array[i] = self.team.pop()
            i += 1
        
        # putting back elements into the stack in the same order.
        for j in range(i-1,-1,-1): # O(1): If the team has no elements or has a few elements | O(N): If the team has N pokemons inside the stack.
            self.team.push(temp_array[j]) 
        
        return temp_array
    
    def _retrieve_queue_elements(self) -> ArrayR:
        """
        __description__: Retrieves the elements within a queue, and appends the elements back into the queue while
                         retaining its order.

        __returns__:
                     ArrayR: An array of elements served from the queue.
                     
        __complexity__: BEST CASE: O(1), due to the queue being empty or containing minimal number of elements.
                        WORST CASE: O(N), due to the queue containing N number of Pokemons to serve and append back.

        __annotations__: Complexities of each line will be denoted by O(best case) | O(worst case)
        """
        
        # temporary array to store the Pokemon objects.
        i: int = 0
        temp_array: ArrayR = ArrayR(len(self.team)) if len(self.team) > 0 else None # O(1): If team has no elements, or has few elements. | O(N): if there N Pokemons in the stack.
        
        # printing empty stack results.
        if temp_array is None:
            print("The team is currently empty.")
            
        # tracking elements inside the queue, and storing them in a temporary array.
        while not self.team.is_empty():
            temp_array[i] = self.team.serve()
            i += 1
            
        # putting back elements into the queue in the same order.
        for j in range(i):
            self.team.append(temp_array[j])
            
        return temp_array

    def _special_method_set(self):
        """
        __description__: Reverses the first half of the stack members.
        
        __complexity__: BEST CASE: O(1), if the size of the stack was small, which results in lower amounts of pop and push 
                        operations. Since the operations inherently depend on the number of elements, the best case scales with N, making it
                        O(N).
                        
                        WORST CASE: O(N), if the size of the stack was N, which results in N/2 operations of pop and pushes.
        """
        
        target_length: int = len(self.team) // 2
        temp_array: ArrayR = ArrayR(target_length) # O(1): if the size was a smaller number | O(N): if the size was N.
        
        for index1 in range(target_length): # O(1): if the size was a smaller number | O(N): if the size was N
            temp_array[index1] = self.team.pop()
        
        for index2 in range(target_length): # O(1): if the size was a smaller number | O(N): if the size was N
            self.team.push(temp_array[index2])
    
    def _special_method_rotate(self):
        """
        __description__: Reverse the back of the queue.
        
        __complexity__: BEST CASE: O(N), if the size of the queue is very small, the operations still scale linearly with the number of elements
                        due to the serve and append operations. However, the impact is minimal for very small sizes.
                        
                        WORST CASE: O(N), if the size of the stack was N, which results in inherently processing each element in the queue.
        """
        
        # target length variable
        target_length: int = 0
        
        # the target length changes depending on the size
        if len(self.team) % 2 == 0:
            target_length = (len(self.team) // 2 - 1)
        else:
            target_length = len(self.team) // 2
        
        # temporary array to store pokemons
        temp_array: ArrayR = ArrayR(len(self.team)) # O(1): if the size of the team was 1 | O(N): If the size of the team was N.
        
        for index in range(len(self.team)): # O(1): if the size of the team was 1 | O(N): If the size of the team was N.
            temp_array[index] = self.team.serve()
        
        # variable for reversing elements
        offset: int = 0
        
        for index in range(len(temp_array)): # O(1): if the size of the team was 1 | O(N): If the size of the team was N.
            if target_length - index >= 0:
                self.team.append(temp_array[index])
            else:
                self.team.append(temp_array[len(temp_array) - 1 - offset])
                offset += 1
    
    def _special_method_optimise(self):
        """
        __description__: Toggles the sorting order of the OPTIMISE battle.
        
        __complexity__: BEST CASE: O(1), where the team size is 1. But considering that the list has N elements, the overall
                        best case complexity for that scenario is O(N log N) because we are iterating N times, and adding the elements to
                        the back of the list.
                        
                        WORST CASE: O(N^2), where the team size is N. Considering it iterates N times, when the elements are added to the
                        far left of the list, it requires shuffling of the N elements to the right, which increases complexity of this function in
                        the worst case scenario.
        """
        self.list_reversed = not self.list_reversed
        
        # getting the length of the list beforehand
        length: int = len(self.team)
        
        # temporary array to store listitem objects
        temp_array: ArrayR = ArrayR(length) # O(1): if the size of the team was 1 | O(N): If the size of the team was N.
        
        # delete every element inside the list.
        for iteration in range(length): # O(1): if the size of the team was 1 | O(N): If the size of the team was N.
            temp_array[iteration] = self.team.delete_at_index(len(self.team)-1)
        
        # toggling the sorting order.
        for pokemon in temp_array: # O(1): if the size of the team was 1 | O(N): If the size of the team was N.
            item = ListItem(value=pokemon.value, key=1/pokemon.key)
            self.team.add(item) # O(log N): If the element was added in the back of the team. | O(N): If the element was added in the front and required shuffling of elements to the right.
        
class Trainer:

    def __init__(self, name) -> None:
        """
        __description__: Constructor for the Trainer class.

        __params__:
                    name (str): The name of the trainer.
        """
        self.name: str = name
        self.poketeam: PokeTeam = PokeTeam()
        self.pokedex: BSet = BSet()
        self.team_registered: bool = False

    def pick_team(self, method: str) -> None:    
        """
        __description__: Picks the choice of method choosing for the trainer.

        __params__:
                    method (str): The type of method to choose Pokemons from.

        __raises__:
                    ValueError: In case of any invalid method name written.
        
        __complexity__: BEST CASE: O(1), due to the method being incorrectly written and also it can consider the case where the
                        number of chosen pokemons are few so the overall complexity runs in constant time.
                        
                        WORST CASE: O(N), due to the N number of pokemons chosen by the user and we have to iterate over N times to
                        register the pokemons.
        
        __annotations__: Complexities are denoted by O(best case) | O(worst case)
        """
        
        # Try-catching if the method argument is correct or not.
        try:
            assert method == 'Random' or method == 'Manual'

            # If it passes the cases above.
            if method == 'Random':
                self.poketeam.choose_randomly()  # O(1): the limit is a small number. | O(N): The limit is N.
            else:
                self.poketeam.choose_manually() # O(1): User chooses few pokemons or the limit is small | O(N): The limit is N, and the user chooses all of the N pokemons with significant input failures.
            
        except AssertionError:
            print('You should only enter \'Random\' or \'Manual\'\nTry again!')  
        
        # register the pokemons chosen if not done already
        while not self.team_registered:
            for pokemon in self.poketeam.selected_pokemons: # O(1): If the user chose few pokemons | O(N): If the user chose N pokemons.
                if pokemon is not None:
                    self.register_pokemon(pokemon)
                
            self.team_registered = True

    def get_team(self) -> PokeTeam:
        """
        __description__: Returns the PokeTeam of the trainer.

        __returns__:
                     PokeTeam: The PokeTeam of the trainer.
        """
        return self.poketeam

    def get_name(self) -> str:
        """
        __description__: Returns the name of the Trainer.

        __returns__:
                     str: The name of the Trainer.
        """
        return self.name
    
    def register_pokemon(self, pokemon: Pokemon) -> None:
        """
        __description__: Registers poketypes for the trainer.

        __params__:
                    pokemon (Pokemon): Pokemon seen in the battle or team.
        """
        # checking if the pokemon type is already inside the bset or not.
        if pokemon.get_poketype().value + 1 not in self.pokedex:
            
            # add if the type is unique.
            self.pokedex.add(pokemon.get_poketype().value + 1) 

    def get_pokedex_completion(self) -> float:
        """
        __description__: Returns the completion percentage of the pokedex.

        __returns__:
                     float: The percentage of completion.
        
        __complexity__: BEST CASE: O(1), due to the complexity being low if there are few types of pokemons to be processed.
                        WORST CASE: O(N), due to the complexity being high if N is the number of poketypes in the battle and requires
                        N iterations to be processed.
        
        __annotations__: Complexities are denoted by O(best case) | O(worst case)
        """
        
        return round( len(self.pokedex) / len(PokeType), 2 ) # O(1) if the number of types are few | O(N): If there are N number of types.

    def get_trainer_team(self) -> object:
        """
        __description__: Returns self.team of the Poketeam object.

        Returns:
            object: Any one ADT described for self.team.
        """
        return self.get_team().team

    def __str__(self) -> str:
        """
        __description__: Returns the string representation of the Trainer.

        __returns__:
                    str: The string representation of the Trainer.
        """
        return f"Trainer {self.get_name()} Pokedex Completion: {int(self.get_pokedex_completion() * 100)}%"