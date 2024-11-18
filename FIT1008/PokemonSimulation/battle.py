
from __future__ import annotations
from poke_team import Trainer
from battle_mode import BattleMode
from math import ceil
from data_structures.sorted_list_adt import ListItem

class Battle:
    def __init__(self, trainer_1: Trainer, trainer_2: Trainer, battle_mode: BattleMode, criterion = "health") -> None:
        """
        Constructor for the Battle class.

        Args:
            trainer_1 (Trainer): Trainer 1 in the battle.
            trainer_2 (Trainer): Trainer 2 in the battle.
            battle_mode (BattleMode): The battle mode the trainers will be fighting in.
            criterion (str, optional): The criteria to order for OPTIMISE mode.
        """
        self.trainer_1: Trainer = trainer_1
        self.trainer_2: Trainer = trainer_2
        self.battle_mode: Trainer = battle_mode
        self.criterion: Trainer = criterion

    def commence_battle(self) -> Trainer | None:
        """
        __description__: Creates a battle between Trainer 1 and Trainer 2.

        __returns__:
                    Trainer | None: A winning trainer or a draw.
        
        __complexity__: Please refer to the docstrings of the methods called.
        """
        
        # if the battle mode is a SET
        if self.battle_mode == BattleMode.SET:
            return self._set_battle()

        # if the battle mode is ROTATE
        elif self.battle_mode == BattleMode.ROTATE:
            return self._rotate_battle()
        
        else:
            return self._optimise_battle()
        
    def _create_teams(self, method: str = 'Random') -> None:
        """
        __description__: Creates the teams for the trainers fighting each other.

        __params__:
                    method (str, optional): The method to pick the teams.
        
        __complexity__: Please refer to the docstrings of the defined functions.
        """
        
        # Picking teams for trainer 1 and trainer 2
        self.trainer_1.pick_team(method)
        self.trainer_2.pick_team(method)
        
        # assembling teams
        self.trainer_1.get_team().assemble_team(self.battle_mode, self.criterion)
        self.trainer_2.get_team().assemble_team(self.battle_mode, self.criterion)

    def _set_battle(self) -> Trainer | None:
        """
        __description__: The logic for SET battle.
        
        __returns__:
                     Trainer | None: The winning trainer or a draw.
        """
        
        # getting the teams to battle.
        set_team_1 = self.trainer_1.get_trainer_team()
        set_team_2 = self.trainer_2.get_trainer_team()
        
        index: int = 0
        while not (set_team_1.is_empty() or set_team_2.is_empty()):
            pokemon_1 = set_team_1.pop() # trainer 1's pokemon
            pokemon_2 = set_team_2.pop() # trainer 2's pokemon
            
            # registering pokemons
            self.trainer_1.register_pokemon(pokemon_2)
            self.trainer_2.register_pokemon(pokemon_1)
            
            print(f'{pokemon_1.get_name()} is going in battle with {pokemon_2.get_name()}')
            
            # battling and updating stacks
            Battle._battle_logic(pokemon_1, pokemon_2, self.trainer_1, self.trainer_2)
            self._update_set_mode(pokemon_1, pokemon_2)
            
            print(f'\nROUND {index + 1} OVER\n')
            index += 1
        
        if set_team_1.is_empty() and not set_team_2.is_empty():
            return self.trainer_2
        elif set_team_2.is_empty() and not set_team_1.is_empty():
            return self.trainer_1
        else:
            return None
            
    def _rotate_battle(self) -> Trainer | None:
        """
        __description__: Logic for the ROTATE mode.
        
        __returns__:
                     Trainer | None: Winning trainer or a draw.
        """
        
        # getting the teams to battle.
        queue_team_1 = self.trainer_1.get_trainer_team()
        queue_team_2 = self.trainer_2.get_trainer_team()
        
        index: int = 0
        
        while not (queue_team_1.is_empty() or queue_team_2.is_empty()):
            
            pokemon_1 = queue_team_1.serve() # trainer 1's pokemon
            pokemon_2 = queue_team_2.serve() # trainer 2's pokemon
            
            # registering pokemons
            self.trainer_1.register_pokemon(pokemon_2)
            self.trainer_2.register_pokemon(pokemon_1)
            
            # battle logics and updating queues.
            Battle._battle_logic(pokemon_1, pokemon_2, self.trainer_1, self.trainer_2)
            self._update_rotate_mode(pokemon_1, pokemon_2)
            
            print(f'\nROUND {index + 1} OVER\n')
            index += 1
        
        if queue_team_1.is_empty() and not queue_team_2.is_empty():
            return self.trainer_2
        elif queue_team_2.is_empty() and not queue_team_1.is_empty():
            return self.trainer_1
        else:
            return None

    def _optimise_battle(self) -> Trainer | None:
        """
        __description__: The logic for OPTIMISE battle.
        
        __returns__:
                     Trainer | None: Winning trainer or draw.
                     
        __complexity__: Deleting at index: O(1) best case for having one element to shift to the left, O(N) for worst case
                        for having N elements to be shifted to the left after removal. 
                        
                        For updating the list, check the _update_optimise_mode docstring.
        """ 
        
        # get the teams from both trainers.
        list_team_1 = self.trainer_1.get_trainer_team()
        list_team_2 = self.trainer_2.get_trainer_team()
        
        index: int = 0
        
        while not (list_team_1.is_empty() or list_team_2.is_empty()):
            
            # getting pokemons
            
            # deleting takes O(1) as best case as there is only one element to shift to the left but in general,
            # all case scenarios involve O(N), where N is the number of elements to shift to the left.
            pokemon_1 = self.trainer_1.get_trainer_team().delete_at_index(0).value
            pokemon_2 = self.trainer_2.get_trainer_team().delete_at_index(0).value
            
            # registering pokemons
            self.trainer_1.register_pokemon(pokemon_2)
            self.trainer_2.register_pokemon(pokemon_1)
            
            # battle logic and updating queues.
            Battle._battle_logic(pokemon_1, pokemon_2, self.trainer_1, self.trainer_2)
            self._update_optimise_mode(pokemon_1, pokemon_2)
            
            print(f'\nROUND {index + 1} OVER\n')
            index += 1
        
        if list_team_1.is_empty() and not list_team_2.is_empty():
            return self.trainer_2
        elif list_team_2.is_empty() and not list_team_1.is_empty():
            return self.trainer_1
        else:
            return None

    @staticmethod
    def _battle_logic(p1, p2, tr1, tr2):
        """
        __description__: Battle logic for a single round in a battle.
        
        __complexity__: BEST CASE: O(1), where the trainers have little experience because they have not
                        seen a lot of Pokemons and hence the complexity of O(len(BSet)) is minimal.
                        
                        WORST CASE: O(N), where the trainers have a lot of experience because they have seen
                        a lot of Pokemons and hence the complexity of O(len(BSet)) is closer to O(N).
        """
        
        # if p1 speed > p2 speed, p1 attacks first.
        if p1.get_speed() > p2.get_speed():
            attack_damage: int = ceil( p1.attack(p2) * (tr1.get_pokedex_completion() / tr2.get_pokedex_completion()) )
            p2.defend(attack_damage)
            
            # if p2 is alive after this, p2 attacks back.
            if p2.is_alive():
                attack_damage: int = ceil( p2.attack(p1) * (tr2.get_pokedex_completion() / tr1.get_pokedex_completion()) )
                p1.defend(attack_damage)

        # if p2 speed > p1 speed, p2 attacks first.
        elif p1.get_speed() < p2.get_speed():
            attack_damage: int = ceil( p2.attack(p1) * (tr2.get_pokedex_completion() / tr1.get_pokedex_completion()) )
            p1.defend(attack_damage)
            
            # if p1 is still alive, p1 attacks back.
            if p1.is_alive():
                attack_damage: int = ceil( p1.attack(p2) * (tr1.get_pokedex_completion() / tr2.get_pokedex_completion()) )
                p2.defend(attack_damage)
        
        # both attack in the same time.
        else:
            attack_damage: int = ceil( p1.attack(p2) * (tr1.get_pokedex_completion() / tr2.get_pokedex_completion()) )
            p2.defend(attack_damage)
            
            attack_damage: int = ceil( p2.attack(p1) * (tr2.get_pokedex_completion() / tr1.get_pokedex_completion()) )
            p1.defend(attack_damage)
        
        # if they are still alive, reduce hp.
        if p1.is_alive() and p2.is_alive():
            print("Both Pokemons are still alive. Reducing 1HP")
            p1.health = p1.get_health() - 1
            p2.health = p2.get_health() - 1
    
    def _update_set_mode(self, p1, p2):
        """
        __description__: Updating the stacks of the two trainer teams in SET mode.
        """
        
        # if both pokemons have fainted, leave them.
        if not p1.is_alive() and not p2.is_alive():
            print('Both fainted!')
            
        # if p1 is not alive, update p2's level and put p2 back in the team.
        elif not p1.is_alive():
            print(f'{p1.get_name()} faints')
            p2.level_up()
            self.trainer_2.get_trainer_team().push(p2)
            
        # if p2 is not alive, update p1's level and put p1 back in the team.
        elif not p2.is_alive():
            print(f'{p2.get_name()} faints')
            p1.level_up()
            self.trainer_1.get_trainer_team().push(p1)
        
        # otherwise, put them both in their respective teams.
        else:
            print("Both Pokemons are still alive. Going back to their teams")
            self.trainer_2.get_trainer_team().push(p2)
            self.trainer_1.get_trainer_team().push(p1)
    
    def _update_rotate_mode(self, p1, p2):
        """
        __description__: Logic for ROTATE battles. Updates the queues.
        """
        
        # if both pokemons are not alive, leave them.
        if not p1.is_alive() and not p2.is_alive():
            print('Both fainted!')
        
        # if p1 is not alive, update p2 level and send it back to the team.
        elif not p1.is_alive():
            
            print(f'{p1.get_name()} faints')
            p2.level_up()
            self.trainer_2.get_trainer_team().append(p2)
        
        # if p2 is not alive, update p1 level and send it back to the team.
        elif not p2.is_alive():
            print(f'{p2.get_name()} faints')
            p1.level_up()
            self.trainer_1.get_trainer_team().append(p1)
        
        # otherwise, send both of them back to their respective teams.
        else:
            print("Both Pokemons are still alive. Going back to their teams")
            self.trainer_2.get_trainer_team().append(p2)
            self.trainer_1.get_trainer_team().append(p1)
    
    def _update_optimise_mode(self, p1, p2):
        """
        __description__: Logic for OPTIMISE battle. Updates the lists.
        
        __complexity__: Adding to the list:
                         - BEST CASE: O(log N) for adding an element to the far right of the list.
                         - WORST CASE: O(N) for adding an element to the far left of the list and shuffling
                        elements to the right as a result.
        """
        
        # if both pokemons faint, leave them.
        if not p1.is_alive() and not p2.is_alive():
            print("Both fainted.")
            
        # if p1 is not alive, level up p2 and add back to the list.
        elif not p1.is_alive():
            p2.level_up()
            if self.trainer_2.get_team().list_reversed:
                self.trainer_2.get_trainer_team().add( ListItem(value= p2, key=1 / p2.get_health()))
            else:
                self.trainer_2.get_trainer_team().add( ListItem(value= p2, key=p2.get_health()))
                
            print(f'{p1.get_name()} faints')
        
        # if p2 is not alive, level up p1 and add back to the list.
        elif not p2.is_alive():
            p1.level_up()
            if self.trainer_1.get_team().list_reversed:
                self.trainer_1.get_trainer_team().add(ListItem(value=p1, key=1 /p1.get_health()))
            else:
                self.trainer_1.get_trainer_team().add(ListItem(value=p1, key=p1.get_health()))
            print(f'{p2.get_name()} faints')
        
        # add both back to list.
        else:
            print("Both Pokemons are still alive. Going back to their teams")
            
            if self.trainer_2.get_team().list_reversed:
                self.trainer_2.get_trainer_team().add( ListItem(value= p2, key=1 / p2.get_health()))
            else:
                self.trainer_2.get_trainer_team().add( ListItem(value= p2, key=p2.get_health()))
            
            if self.trainer_1.get_team().list_reversed:
                self.trainer_1.get_trainer_team().add(ListItem(value=p1, key=1 /p1.get_health()))
            else:
                self.trainer_1.get_trainer_team().add(ListItem(value=p1, key=p1.get_health()))