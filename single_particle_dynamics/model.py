import numpy as np

class Model:
    def __init__(self):
        self.particle_trajectory = {'x': [], 'xp': [], 's': []}

    def propagate(self, particle, lattice):
        x_and_xp = np.array([[particle.x],[particle.xp]])
        s = particle.s

        self.particle_trajectory = {'x': [particle.x], 'xp': [particle.xp], 's': [particle.s]}

        for _ in range(lattice.num_cells):
            for _ in range(lattice.quad_steps):
                x_and_xp = lattice.fquad_matrix @ x_and_xp
                self.append_trajectory(x_and_xp[0][0], x_and_xp[1][0], s)

            for _ in range(lattice.drift_steps):
                x_and_xp = lattice.drift_matrix @ x_and_xp
                s = s + (lattice.drift_length / lattice.drift_steps)
                self.append_trajectory(x_and_xp[0][0], x_and_xp[1][0], s)

            for _ in range(lattice.quad_steps):
                x_and_xp = lattice.dquad_matrix @ x_and_xp
                self.append_trajectory(x_and_xp[0][0], x_and_xp[1][0], s)

            for _ in range(lattice.drift_steps):
                x_and_xp = lattice.drift_matrix @ x_and_xp
                s = s + (lattice.drift_length / lattice.drift_steps)
                self.append_trajectory(x_and_xp[0][0], x_and_xp[1][0], s)

    def append_trajectory(self, x, xp, s):
        self.particle_trajectory['x'].append(x)
        self.particle_trajectory['xp'].append(xp)
        self.particle_trajectory['s'].append(s)

    def main(self):
        pass

if __name__ == '__main__':
    pass