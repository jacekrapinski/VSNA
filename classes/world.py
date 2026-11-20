from .solve import Solver
class World:

    def __init__(self, dt = 0.01) -> None:
        self.objects=[]
        self.solver = Solver(dt, self)
        self.frames=100

    def add_obj(self,x):
        if isinstance(x, Node):
            self.objects.append(x)        

    def set_no_frames(self, n):
        self.frames=n

    def simulate(self):
        for frame in range(0,self.frames):
            self.solver.update()
            
