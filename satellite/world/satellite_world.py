import numpy as np
from core.world import World
import random


class SatelliteWorld(World):

    def __init__(self, config):
        World.__init__(self, config)

    def setInitPhi(self, init_phi):
        self.init_state['phi'] = init_phi
        self.state['phi'] = init_phi

    def peek(self):
         # set parameters of copter
        dt = self.dt

        s = self.state

        phi = s['phi']

        return {
            'phi': phi
        }

    def tick(self):
        self.state = self.peek()
        return self.state


# def uniform_noise():
#     return (2.0 * random.random() - 1.0)
