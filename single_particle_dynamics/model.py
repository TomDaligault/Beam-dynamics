import numpy as np

def propagate(particle, lattice):
	trajectory = [particle]
	for _ in range(lattice.num_cells):
		for _ in range(lattice.quad_steps):
			particle = lattice.quad_s_vector + lattice.fquad_matrix @ particle
			trajectory.append(particle)

		for _ in range(lattice.drift_steps):
			particle = lattice.drift_s_vector + lattice.drift_matrix @ particle
			trajectory.append(particle)

		for _ in range(lattice.quad_steps):
			particle = lattice.quad_s_vector + lattice.dquad_matrix @ particle
			trajectory.append(particle)

		for _ in range(lattice.drift_steps):
			particle = lattice.drift_s_vector + lattice.drift_matrix @ particle
			trajectory.append(particle)

	trajectory = np.array(trajectory)
	trajectory = np.stack(trajectory)
	return trajectory

def max_values(trajectory):
	x_max = trajectory[:,0,0].max()
	xp_max = trajectory[:,1,0].max()
	s_max = trajectory[:,2,0].max()

	return x_max, xp_max, s_max

def min_values(trajectory):
	x_min = trajectory[:,0,0].min()
	xp_min = trajectory[:,1,0].min()
	s_min = trajectory[:,2,0].min()

	return x_min, xp_min, s_min