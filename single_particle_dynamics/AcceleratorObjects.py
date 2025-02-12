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

		self.fquad_matrix = np.array([[1,0],[(-1/ (focal_length * quad_steps)),1]])
		self.dquad_matrix = np.array([[1,0],[(1/(focal_length * quad_steps)),1]])
		self.drift_matrix = np.array([[1,(drift_length / drift_steps)],[0,1]])

'''Defines the trajectory of a particle in (x, xp, s) space.
Can be propagated through a defined lattice, appends trajectories with new coordinates after each element'''
class Particle:
	def __init__(self, x, xp, s=0):
		self.x = x
		self.xp = xp
		self.s = s

def example_usage():
	particle = Particle(0.4, -0.1)
	lattice = Lattice(10, 8, 10)
	particle.propagate(lattice)
	xvals = particle.s_trajectory
	yvals = particle.x_trajectory

	plt.plot(xvals, yvals)
	plt.show()