import numpy as np
from classes.node import Node
from classes.solve import Solver
from classes.world import World
import datetime as dt

import pygame

if __name__=="__main__":
    print(f"\nStart @ {dt.datetime.now()}\n")
    
    world = World()
    world.simulate()