import numpy as np

class Solver:
    def __init__(self, dt, world):
        self.dt = dt
        self.gravity = np.array([0, 9.8, 0])
        self.world = world

    def update(self):
        self.new_positions() # step 2
        self.intermidate_velocity() # step 3
        self.reset_acceleration() #step 4
        self.apply_gravity() #step 4
        self.new_velocity() #step 5

    def new_positions(self):
        for obj in self.world.objects:
            obj.updatePosition(self.dt)

    def reset_acceleration(self):
        for obj in self.world.objects:
            obj.reset_acceleration()

    def intermidate_velocity(self):
        for obj in self.world.objects:
            obj.updateVelocityIntermediate(self.dt)

    def new_velocity(self):
        for obj in self.world.objects:
            obj.new_velocity(self.dt)

    def apply_gravity(self):
        for obj in self.world.objects:
            obj.accelerate(self.gravity)