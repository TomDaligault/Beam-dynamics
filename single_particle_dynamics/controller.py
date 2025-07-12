import numpy as np
from AcceleratorObjects import Lattice

from view import View
import model

class Controller:
	def __init__(self, view):
		self.view = view
		self.show_ellipse = True
		self.run_active = False
		self.cell_length = 1

	def main(self):
		self.view.register_callback('run_animation', self.run_animation)
		self.view.register_callback('continue_animation', self.continue_animation)
		self.view.register_callback('change_tab', self.change_tab)
		self.view.register_callback('update_ellipse', self.update_ellipse)
		self.view.main()

#Sink only the selected button, restore the default UI, clear plots, then setup a specific exercise if necessary
	def change_tab(self, button):
		self.view.sink_selected_tab(button)
		self.view.restore_default_control_frame() #Insure that all controls are visible after changing tabs.
		self.view.clear_plots()

		#Specific methods many remove widgets from the UI.
		if button == 'exercise 1':
			self.show_ellipse = False
			self.view.set_exercise_1()
		if button == 'exercise 2':
			self.show_ellipse = False
			self.view.set_exercise_2()
		if button == 'exercise 3':
			self.show_ellipse = True
			self.view.set_exercise_3()
		if button == 'exercise 4':
			self.show_ellipse = True
			self.view.set_exercise_4()
		else:
			pass

	def make_particle(self):
		x, xp, s = self.view.get_particle_inputs()
		return np.array([[x], [xp], [s]])

	def get_lattice(self):
		drift_length, focal_length, num_cells = self.view.get_lattice_inputs()
		return Lattice(drift_length, focal_length, num_cells)

	#sets plot markers from start_value, spaced by cell_length
	#This method is called by self.view.ellipse_scale, which passes its current value as the start value
	def update_ellipse(self, scale_value):
		self.view.figure.show_ellipse(marker_start = int(scale_value), cell_length = self.cell_length)

	def run_animation(self):
		#Flag that determines if the continue button should be enabled
		# self.run_active = True
		self.view.disable_animation_controls()

		particle = self.make_particle()
		lattice = self.get_lattice()
		self.trajectory = model.propagate(particle, lattice)

		self.cell_length = lattice.cell_length
		self.view.ellipse_scale.configure(to = lattice.cell_length)

		self.relimit_plots(self.trajectory)

		anim_speed = self.view.anim_speed_option.get_speed()
		start = self.view.ellipse_scale.get()

		anim_kwargs = {'anim_speed': anim_speed, 'show_ellipse': self.show_ellipse, 'marker_start': start, 'cell_length': lattice.cell_length, 'callback': self.view.restore_animation_controls}
		self.view.figure.animate_plots(self.trajectory, **anim_kwargs)

	def continue_animation(self):
		#disable controls that cause bugs or visual artifacts while blitting
		self.view.disable_animation_controls()

		#use the last particle coordinates of the previous run as the starting coordinates of the next run
		particle = self.trajectory[-1]
		lattice = self.get_lattice()
		self.trajectory = model.propagate(particle, lattice)
		self.cell_length = lattice.cell_length
		self.view.ellipse_scale.configure(to = lattice.cell_length)

		self.relimit_plots(self.trajectory)

		anim_speed = self.view.anim_speed_option.get_speed()
		start = self.view.ellipse_scale.get()

		anim_kwargs = {'anim_speed': anim_speed, 'show_ellipse': self.show_ellipse, 'marker_start': start, 'cell_length': lattice.cell_length, 'callback': self.view.restore_animation_controls}
		self.view.figure.animate_plots(self.trajectory, **anim_kwargs)
		

	def relimit_plots(self, trajectory):
		x_max, xp_max, s_max = model.max_values(trajectory)
		x_min, xp_min, s_min = model.min_values(trajectory)
		self.view.relimit_plots(x_max, xp_max, s_max, x_min, xp_min, s_min)
		


if __name__ == '__main__':
	view = View()
	controller = Controller(view)
	controller.main()