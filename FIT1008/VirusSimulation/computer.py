from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Computer:

    name: str
    hacking_difficulty: int
    hacked_value: int
    risk_factor: float
    
    def __eq__(self, other):
        
        if not isinstance(other, Computer):
            return TypeError
        
        return (self.hacking_difficulty, self.risk_factor, self.name, self.hacked_value) == (other.hacking_difficulty, other.risk_factor, other.name, other.hacked_value)
    
    def __lt__(self, other):
        
        if not isinstance(other, Computer):
            return TypeError
        
        return (self.hacking_difficulty, self.risk_factor, self.name, self.hacked_value) < (other.hacking_difficulty, other.risk_factor, other.name, other.hacked_value)

    def __gt__(self, other):
        if not isinstance(other, Computer):
            return TypeError
        
        return (self.hacking_difficulty, self.risk_factor, self.name, self.hacked_value) > (other.hacking_difficulty, other.risk_factor, other.name, other.hacked_value)
     
    def __le__(self, other):
        if not isinstance(other, Computer):
            return TypeError
        
        return (self.hacking_difficulty, self.risk_factor, self.name, self.hacked_value) <= (other.hacking_difficulty, other.risk_factor, other.name, other.hacked_value)

    def __ge__(self, other):
        if not isinstance(other, Computer):
            return TypeError
        
        return (self.hacking_difficulty, self.risk_factor, self.name, self.hacked_value) >= (other.hacking_difficulty, other.risk_factor, other.name, other.hacked_value)