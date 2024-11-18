from abc import ABC
from enum import Enum
from data_structures.referential_array import ArrayR
from math import ceil

class PokeType(Enum):
    """
    This class contains all the different types that a Pokemon could belong to
    """
    FIRE = 0
    WATER = 1
    GRASS = 2
    BUG = 3
    DRAGON = 4
    ELECTRIC = 5
    FIGHTING = 6
    FLYING = 7
    GHOST = 8
    GROUND = 9
    ICE = 10
    NORMAL = 11
    POISON = 12
    PSYCHIC = 13
    ROCK = 14

class TypeEffectiveness:
    """
    Represents the type effectiveness of one Pokemon type against another.
    """
    
    EFFECT_TABLE: ArrayR = None # 2D-array storing effectivness values.
    FILE: str = "type_effectiveness.csv" # file to get the values.
    
    @classmethod
    def __generate_effectiveness_table(cls) -> None:
        """
        __description__: Populates the EFFECT_TABLE variable with effectiveness values from "type_effectiveness.csv" file.
        
        __complexity__: BEST CASE: O(1), due to the fact that EFFECT_TABLE is not None and is already populated.
                        WORST CASE: O(N^2), due to the fact that the outer loop iterates over each line in the file and the inner loop iterates
                        over each element in a line to populate the row_array. If the file has N lines, the outer loop iterates over N times, and
                        the inner_loop also iterates over N times to match the number of Poketypes in the game.
        
        __annotations__: Complexities are marked in each line as O(best case) | O(worst case)
        """

        # populate only if there is nothing in the 2d array.
        if cls.EFFECT_TABLE is None:
            
            # try-except to catch any exceptions throughout the program.
            try:
                
                with open(cls.FILE, 'r') as file:
                    
                    # getting information about the file.
                    contents: list[str] = file.readlines() # O(1): There are no contents or only few lines. | O(N): There are N lines.
                    count: int = len(contents)
                    
                    # checks if there is any content inside the file.
                    if count == 0:
                        raise InterruptedError

                    # initialise a new array of length count to EFFECT_TABLE
                    cls.EFFECT_TABLE = ArrayR(count) # O(1): Creates an array of one index | O(N): Creates an array of N indexes.
                    
                    # iterating and parsing through each line, and storing the contents inside the array.
                    for index1, line in enumerate(contents): # O(1): Iterate at most few times. | O(N): Iterates N times.
                        
                        # removing and splitting lines.
                        element_to_insert: list[str] = line.rstrip('\n').split(',') # O(1): Searches through few characters. | O(M): Searches through M characters.
                        char_count: int = len(element_to_insert)
                        
                        # checking if there are enough characters on that line to be valid.
                        if count < len(PokeType):
                            raise InterruptedError
                        
                        # creating an inner array to stored inside every array element in EFFECT_TABLE.
                        row_array: ArrayR = ArrayR(char_count) # O(1): Only one element to be stored. | O(N): N elements to be stored.
                        
                        # converting lists into arrays.                    
                        for index2, element in enumerate(element_to_insert): # O(1): Iterates no to few times only. | O(N): Iteartes N times.
                            row_array[index2] = element
                        
                        # storing the inner array inside each element of effect table.
                        cls.EFFECT_TABLE[index1] = row_array
            
            # File has not been found.        
            except FileNotFoundError: 
                print("File has not been found in the directory. Please check the path and try again.")
            
            # Interrupts within the program.
            except InterruptedError:
                print("Interrupted due to no data content in the file, or contents are not stored correctly. Try again.")
                           
    @classmethod
    def get_effectiveness(cls, attack_type: PokeType, defend_type: PokeType) -> float:
        
        """
        __description__: Returns the effectiveness of one Pokemon type against another, as a float.

        __params__:
                    attack_type (PokeType): The type of the attacking Pokemon.
                    defend_type (PokeType): The type of the defending Pokemon.

        __returns__:
                    float: The effectiveness of the attack, as a float value between 0 and 4.
                    
        __complexity__: BEST CASE: O(1), due to the fact that the effect table is already populated, and the target value to be found
                        is present in the second row and first column in the 2d array.
                        WORST CASE: O(N^2), due to the fact that the effect table is not populated, and the target value is present
                        in the last row and the last column in the 2d array. Since the dominating term in the complexity is N^2, the
                        overall tight upper bound of the function is O(N^2).
                        
        __annotations__: Complexities are represented by O(best case) | O(worst case)
        """
        cls.__generate_effectiveness_table() # O(1): table already populated. | O(N^2): table needs to be populated with each record.
        
        # finding the correct indexes to get the right effectiveness value.
        title_row: ArrayR = cls.EFFECT_TABLE[0]
        target_row: int = title_row.index(attack_type.name.title()) + 1 # O(1): If the value is in the first index | O(N) where the value is in the last index.
        target_col: int = title_row.index(defend_type.name.title()) # O(1): If the value is in the first index | O(N) where the value is in the last index.
        
        # returning the effectiveness value.
        return float(cls.EFFECT_TABLE[target_row][target_col])
        
    def __len__(self) -> int:
        """
        __description__: Returns the number of types of Pokemon
        """
        return len(PokeType) if TypeEffectiveness.EFFECT_TABLE is None else len(TypeEffectiveness.EFFECT_TABLE) - 1

class Pokemon(ABC):
    """
    Represents a base Pokemon class with properties and methods common to all Pokemon.
    """
    def __init__(self):
        """
        Initializes a new instance of the Pokemon class.
        """
        self.health = None
        self.level = None
        self.poketype = None
        self.battle_power = None
        self.evolution_line = None
        self.name = None
        self.experience = None
        self.defence = None
        self.speed = None

    def get_name(self) -> str:
        """
        Returns the name of the Pokemon.

        Returns:
            str: The name of the Pokemon.
        """
        return self.name

    def get_health(self) -> int:
        """
        Returns the current health of the Pokemon.

        Returns:
            int: The current health of the Pokemon.
        """
        return self.health

    def get_level(self) -> int:
        """
        Returns the current level of the Pokemon.

        Returns:
            int: The current level of the Pokemon.
        """
        return self.level

    def get_speed(self) -> int:
        """
        Returns the current speed of the Pokemon.

        Returns:
            int: The current speed of the Pokemon.
        """
        return self.speed

    def get_experience(self) -> int:
        """
        Returns the current experience of the Pokemon.

        Returns:
            int: The current experience of the Pokemon.
        """
        return self.experience

    def get_poketype(self) -> PokeType:
        """
        Returns the type of the Pokemon.

        Returns:
            PokeType: The type of the Pokemon.
        """
        return self.poketype

    def get_defence(self) -> int:
        """
        Returns the defence of the Pokemon.

        Returns:
            int: The defence of the Pokemon.
        """
        return self.defence

    def get_evolution(self):
        """
        Returns the evolution line of the Pokemon.

        Returns:
            list: The evolution of the Pokemon.
        """
        return self.evolution_line

    def get_battle_power(self) -> int:
        """
        Returns the battle power of the Pokemon.

        Returns:
            int: The battle power of the Pokemon.
        """
        return self.battle_power

    def attack(self, other_pokemon) -> float:
        """
        __description__: Calculates and returns the damage that this Pokemon inflicts on the other Pokemon during an attack.

        __params__:
                    other_pokemon (Pokemon): The Pokemon that this Pokemon is attacking.

        __returns__:
                    int: The damage that this Pokemon inflicts on the other Pokemon during an attack.
                    
        __complexity__: BEST CASE: O(1), due to the effect table being populated and the target value is in the second row and first column of
                        the 2d array.
                        WORST CASE: O(N^2), due to the effect table not being populated and the target value is in the last row and last column of
                        the 2d array. Since the dominating term in the complexity is N^2, the overall tight upper bound of the function is O(N^2).
        
        __annotations__: Complexities are represented by O(best case) | O(worst case)
        """
        
        # getting defence and attack info from pokemons.
        attacking_points: float = self.get_battle_power()
        defending_points: float = other_pokemon.get_defence()
        
        final_damage: float = 0
        
        # applying necessary formulae
        if defending_points < attacking_points / 2:
            final_damage = attacking_points - defending_points
        elif  defending_points < attacking_points:
            final_damage = ceil(attacking_points * 5 / 8 - defending_points / 4)
        else:
            final_damage = ceil(attacking_points / 4)
        
        # returning the attack inflicted.
        return final_damage * TypeEffectiveness.get_effectiveness(self.get_poketype(), other_pokemon.get_poketype()) # O(1): If the effect table is populated, and the target value is in the second row and first column of the 2d array. ...
        # | O(N^2): If the effect table is not populated, and the target value is in the last row and column of the 2d array.

    def defend(self, damage: int) -> None:
        """
        Reduces the health of the Pokemon by the given amount of damage, after taking
        the Pokemon's defence into account.

        Args:
            damage (int): The amount of damage to be inflicted on the Pokemon.
        """
        effective_damage = damage/2 if damage < self.get_defence() else damage
        self.health = self.health - effective_damage

    def level_up(self) -> None:
        """
        Increases the level of the Pokemon by 1, and evolves the Pokemon if it has
          reached the level required for evolution.
        """
        self.level += 1
        if len(self.evolution_line) > 0 and self.evolution_line.index\
            (self.name) != len(self.evolution_line)-1:
            self._evolve()

    def _evolve(self) -> None:
        """
        __description__: Evolves the Pokemon to the next stage in its evolution line, and updates its attributes accordingly.
        
        __complexity__: BEST CASE: O(1), due to the next evolution name being in the second index in the evolution line.
                        WORST CASE: O(N), due to the next evolution name being in the second last index in the evolution line.
        
        __annotations__: Complexities are represented by O(best case) | O(worst case)
        """
        
        # getting the current index of the evolution line.
        next_index: int = self.get_evolution().index(self.get_name()) + 1 # O(1): If the name is in the second index | O(N) if the name is in the second last index
        
        # updating the attributes of the Pokemon.
        self.name = self.get_evolution()[next_index]
        self.battle_power = self.get_battle_power() * 1.5
        self.health = self.get_health() * 1.5
        self.speed = self.get_speed()  * 1.5
        self.defence = self.get_defence() * 1.5
        
        print(f'\n{self.get_evolution()[next_index-1]} has evolved into {self.get_name()}!\n')

    def is_alive(self) -> bool:
        """
        Checks if the Pokemon is still alive (i.e. has positive health).

        Returns:
            bool: True if the Pokemon is still alive, False otherwise.
        """
        return self.get_health() > 0

    def __str__(self):
        """
        Return a string representation of the Pokemon instance in the format:
        <name> (Level <level>) with <health> health and <experience> experience
        """
        return f"{self.name} (Level {self.level}) with {self.get_health()} health and {self.get_experience()} experience"