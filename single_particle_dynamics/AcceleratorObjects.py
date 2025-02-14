import matplotlib.pyplot as plt
import numpy as np

'''Defines transfer matrices from give lattice parameters.
Supports optionally subdividing lattice elements via quad_steps and drift_steps'''
class Lattice:
    def __init__(self, drift_length, focal_length, num_cells, quad_steps = 5, drift_steps = 5):
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

'''Defines the trajectory of a particle in (x, xp, s) space.
Can be propagated through a defined lattice, appends trajectories with new coordinates after each element'''
class Particle:
    def __init__(self, x, xp, s=0):
        self.particle = np.array([[x],
                             [xp],
                             [s]])

        self.trajectory = np.array(self.particle)

    def propagate(self, lattice):
        for _ in range(lattice.num_cells):
            for _ in range(lattice.quad_steps):
                self.particle = lattice.quad_s_vector + lattice.fquad_matrix @ self.particle
                self.trajectory = np.concatenate((self.trajectory, self.particle), axis = 1)

            for _ in range(lattice.drift_steps):
                self.particle = lattice.drift_s_vector + lattice.drift_matrix @ self.particle
                self.trajectory = np.concatenate((self.trajectory, self.particle), axis = 1)

            for _ in range(lattice.quad_steps):
                self.particle = lattice.quad_s_vector + lattice.dquad_matrix @ self.particle
                self.trajectory = np.concatenate((self.trajectory, self.particle), axis = 1)

            for _ in range(lattice.drift_steps):
                self.particle = lattice.drift_s_vector + lattice.drift_matrix @ self.particle
                self.trajectory = np.concatenate((self.trajectory, self.particle), axis = 1)

if __name__ == '__main__':
    particle = Particle(10, 4, -0.1)
    lattice = Lattice( 10, 8, 1)
    particle.propagate(lattice)
    # plt.plot(particle.trajectory[2], particle.trajectory[0])
    # plt.show()

    print(particle.trajectory[0][0])