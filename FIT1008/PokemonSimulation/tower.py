"""
This module contains BattleTower Class.

__edited__: Sharvan Saikumar
__date__: April 10 2024

"""
from poke_team import Trainer
from data_structures.queue_adt import CircularQueue
from typing import Tuple
import random
from battle_mode import *
from battle import *

class BattleTower:
    
    MIN_LIVES = 1
    MAX_LIVES = 3
    
    BATTLE_MODE: BattleMode = BattleMode.ROTATE
    SELECTION_MODE: str = "Random"
        
    def __init__(self) -> None:
        """
        __description__: Constructor for the BattleTower Class.
        """
        self.my_trainer: Trainer = None # stores my trainer
        self.my_lives: int = None # stores my trainer's lives
        self.enemy_trainers: CircularQueue = None # stores all the enemy trainers lives
        self.enemy_trainers_lives: CircularQueue = None # stores all the enemy trainer's lives
        self.wins: int = 0 # stores all the my trainers wins against enemy lives.
    
    def set_my_trainer(self, trainer: Trainer) -> None:
        """
        __description__: Setting the trainer of the battle tower class.
        
        __params__:
                    trainer (Trainer): The trainer to be chosen as the battle tower's trainer.
        """
        
        self.my_trainer = trainer
        self.my_lives = random.randint(self.MIN_LIVES, self.MAX_LIVES)
        
    def generate_enemy_trainers(self, num_teams: int) -> None:
        """
        __description__: Generates enemy trainers for the battle towers randomly.
        
        __complexity__: BEST CASE: O(1) if there is only one opponent trainer to be stored inside the queue.
                        WORST CASE: O(N^2) if there are N number of trainers to be stored inside the queue,
                        and there is to settle N number of pokemons randomly chosen and assembling them in 
                        ROTATE mode.
        """
        
        self.enemy_trainers = CircularQueue(num_teams) # O(1): Few elements to be stored | O(N): N elements to be stored.
        self.enemy_trainers_lives = CircularQueue(num_teams) # O(1): Few elements to be stored | O(N): N elements to be stored.
        
        # Iterating each time to randomly generate a enemy trainer.
        for i in range(1, num_teams+1):
            enemy_trainer: Trainer = Trainer(f"Trainer {i}")
            
            enemy_trainer.pick_team(self.SELECTION_MODE)
            
            lives_remaining: int = random.randint(self.MIN_LIVES, self.MAX_LIVES)
            self.enemy_trainers_lives.append(lives_remaining)
            
            # create teams for each enemy trainer
            enemy_trainer.get_team().assemble_team(self.BATTLE_MODE)
            self.enemy_trainers.append(enemy_trainer)
            
    def battles_remaining(self) -> bool:
        """
        __description__: Returns true if there exists anymore battles.

        Returns:
            bool: True if there exists any more battles.
        """
        return False if self.my_lives == 0 or self.enemy_trainers.is_empty() else True

    def next_battle(self) -> Tuple[Trainer, Trainer, Trainer, int, int]:
        """
        __description__: Simulates one battle in the tower between the player team and the enemy
                         team.
         __complexity__: BEST CASE: O(1), when there are few pokemons there to regenerate and assemble.
                         WORST CASE: O(N^2), where there are N pokemons to regenerate within the team and there are
                         N pokemons to assemble within the team, during the ROTATE battle.
        """
        
        # getting information on the current enemy.
        current_enemy: Trainer = self.enemy_trainers.serve()
        current_enemy_lives: int = self.enemy_trainers_lives.serve()
        
        # regenerating teams before battle.
        self.my_trainer.get_team().regenerate_team(self.BATTLE_MODE) # O(1) | O(N^2)
        current_enemy.get_team().regenerate_team(self.BATTLE_MODE) # O(1) | O(N^2)
        
        # getting battle information
        current_battle: Battle = Battle(self.my_trainer, current_enemy, self.BATTLE_MODE)
        battle_outcome: Trainer | None = current_battle.commence_battle()
        
        # if my trainer wins, update enemy live and wins.
        if battle_outcome == self.my_trainer:
            current_enemy_lives -= 1
            self.wins += 1
              
        # if enemy trainer wins, update my lives only.      
        elif battle_outcome == current_enemy:
            self.my_lives -= 1        
        
        # if it is a draw.
        else:
            self.my_lives -= 1
            current_enemy_lives -= 1
            self.wins += 1
        
        # only append if enemy lives are greater than 0.
        if current_enemy_lives > 0:
            self.enemy_trainers.append(current_enemy)
            self.enemy_trainers_lives.append(current_enemy_lives)
        

        # return tuple.
        return ( battle_outcome, self.my_trainer, current_enemy, self.my_lives, current_enemy_lives)
    
    def enemies_defeated(self) -> int:
        """
        __description__: Returns the number of enemies defeated by the player trainer

        Returns:
            int: The number of enemies defeated by the player trainer
        """
        return self.wins