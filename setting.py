from enum import Enum

class Status_Hero(Enum):
    FREEZE = 0
    MOVE = 1
    ATTACK = 2
    DIE = 3

class Direction(Enum):
    RIGHT = True
    LEFT = False
    
