import matplotlib.pyplot as plt
import numpy as np

'''Defines transfer matrices from give lattice parameters.'''
'''Supports optionally subdividing lattice elements via quad_steps and drift_steps. Default is 5 subdivisions.'''
class Lattice:
    def __init__(self, drift_length, focal_length, num_cells, quad_steps = 9, drift_steps = 9):
        self.focal_length = focal_length
        self.drift_length = drift_length
        self.quad_steps = quad_steps
        self.drift_steps = drift_steps
        self.num_cells = num_cells
        self.cell_length = 2*(self.drift_steps + self.quad_steps)

        self.fquad_matrix = np.array([[1, 0, 0], 
                                      [(-1/ (focal_length * quad_steps)), 1, 0], 
                                      [0, 0, 1]])

        self.dquad_matrix = np.array([[1, 0, 0], 
                                      [(1/(focal_length * quad_steps)), 1, 0],
                                      [0, 0, 1]])

        self.drift_matrix = np.array([[1, (drift_length / drift_steps), 0],
                                     [0, 1, 0], 
                                     [0, 0, 1]])

        self.quad_s_vector = np.array([[0],
                                       [0],
                                       [0]])

        self.drift_s_vector = np.array([[0],
                                        [0],
                                        [drift_length / drift_steps]])
