import numpy as np
class Node:
    def __init__(self, position, mass = 1) -> None:
        self.position = position
        self.position_old = position
        self.velocity_old = np.zeros(3)
        self.velocity = np.zeros(3)
        self.velocity_intermediate = np.zeros(3)
        self.acceleration = np.zeros(3)
    
    def updatePosition(self, dt):
        self.position_current = self.position_old + self.velocity_old * dt + 0.5 * self.acceleration * dt**2

    def updateVelocityIntermediate(self, dt):
        self.velocity_intermediate = self.velocity_old + 0.5 * self.acceleration * dt

    def accelerate(self, acceleration):
        self.acceleration += acceleration

    def reset_acceleration(self):
        self.acceleration = np.zeros(3)

    def new_velocity(self, dt):
        self.velocity_current = self.velocity_intermediate + 0.5 * self.acceleration * dt
        self.velocity_old = self.velocity_current
        self.position_old = self.position_current