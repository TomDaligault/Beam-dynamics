import tkinter as tk
import numpy as np
from AcceleratorObjects import Particle, Lattice

from model import Model
from view import View


import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Controller:
	def __init__(self):
		self.model = Model()
		self.view = View(self)
		self.show_ellipse = True
		self.run_active = False
		self.cell_length = 1

	def main(self):
		self.view.main()

#Sink only the selected button, restore the default UI, clear plots, then setup a specific exercise if necessary
	def change_tab(self, button):
		for _ in self.view.tab_buttons.values():
			_.configure(relief='raised')
		self.view.tab_buttons[button].configure(relief='sunken')

		#This insures that every widget is visible after changing tabs.
		#Specific exercises will then remove specific widgets.
		for frame in self.view.control_frame.children.values():
			for widget in frame.children.values():
				widget.grid()
				widget.configure(state='normal')
		self.view.continue_button.configure(state='disabled')

		self.clear_plots()

		if button == 'exercise 1':
			self.set_exercise_1()
		if button == 'exercise 2':
			self.set_exercise_2()
		if button == 'exercise 3':
			self.set_exercise_3()
		if button == 'exercise 4':
			self.set_exercise_4()
		else:
			pass

	#Stop animation, restore UI controls, clear plots.
	def clear_plots(self):
		#Prevent funcanimation from throwing an error after clearing plots
		try:
			self.animation.pause()
		except AttributeError:
			pass 

		self.view.run_button.config(state = 'normal')
		self.view.continue_button.config(state = 'disabled')
		self.view.anim_speed_option.config(state = 'normal')
		self.view.ellipse_scale.configure(state = 'normal')

		self.view.figure.clear_plots()
		self.view.canvas_widget.draw()

	def set_lattice_inputs(self, drift_length, focal_length, num_cells):		
		self.view.drift_Entry.delete(0, tk.END)
		self.view.focus_Entry.delete(0, tk.END)
		self.view.cell_Entry.delete(0, tk.END)
		self.view.drift_Entry.insert(0, drift_length)
		self.view.focus_Entry.insert(0, focal_length)
		self.view.cell_Entry.insert(0, num_cells)

	def set_particle_inputs(self, x, xp):
		self.view.x_Entry.delete(0, tk.END)
		self.view.xp_Entry.delete(0, tk.END)
		self.view.x_Entry.insert(0, x)
		self.view.xp_Entry.insert(0, xp)

	def randomize_particle(self):
		self.view.x_Entry.delete(0, tk.END)
		self.view.xp_Entry.delete(0, tk.END)
		self.view.x_Entry.insert(0, round(np.random.normal(),2))
		self.view.xp_Entry.insert(0, round(np.random.normal(),2))

	def disable_widgets(self, frame):
		for widget in frame.children.values():
			widget.configure(state='disabled')

	def set_exercise_1(self):
		self.show_ellipse = False
		self.set_lattice_inputs(10, 8, 1)
		self.set_particle_inputs(0.4, -0.1)
		self.view.anim_speed_option.set_speed('slow')
		self.view.anim_speed_option.grid_remove()
		self.view.cell_diagram.grid_remove()
		self.view.ellipse_scale.grid_remove()
		self.view.continue_button.grid_remove()
		self.disable_widgets(self.view.lattice_frame)

	def set_exercise_2(self):
		self.show_ellipse = False
		self.set_lattice_inputs(10, 8, 12)
		self.set_particle_inputs(0.4, -0.1)
		self.view.anim_speed_option.set_speed('med')
		self.view.anim_speed_option.grid_remove()
		self.view.cell_diagram.grid_remove()
		self.view.ellipse_scale.grid_remove()
		self.view.continue_button.grid_remove()
		self.disable_widgets(self.view.particle_frame)

	def set_exercise_3(self):
		self.set_exercise_2()
		self.show_ellipse = True
		self.view.anim_speed_option.set_speed('med')
		self.set_lattice_inputs(10, 40, 25)
		self.set_particle_inputs(0.4, -0.1)

	def set_exercise_4(self):
		self.show_ellipse = True
		self.view.anim_speed_option.set_speed('fast')
		self.set_lattice_inputs(10, 40, 25)
		self.set_particle_inputs(0.4, -0.1)
		self.view.anim_speed_option.grid_remove()
		self.view.continue_button.grid_remove()
		self.disable_widgets(self.view.particle_frame)

	def get_particle(self):
		x = float(self.view.x_Entry.get())
		xp = float(self.view.xp_Entry.get())
		s = 0

		return Particle(x, xp, s)

	def get_lattice(self):
		drift_length = float(self.view.drift_Entry.get())
		focal_length = float(self.view.focus_Entry.get())
		num_cells = int(self.view.cell_Entry.get())

		return Lattice(drift_length, focal_length, num_cells)

	#sets plot markers from start value spaced by cell_length
	#This method is called by self.view.ellipse_scale, which passes its current value as the start value
	def update_ellipse(self, start):
		self.view.figure.show_ellipse(start = int(start), cell_length = self.cell_length)

	def run_animation(self):
		#disable controls that cause bugs or visual artifacts while blitting
		self.view.run_button.configure(state = 'disabled')
		self.view.continue_button.config(state = 'disabled')
		self.view.anim_speed_option.configure(state ='disabled')
		self.view.ellipse_scale.configure(state = 'disabled')
		self.run_active = True

		particle = self.get_particle()
		lattice = self.get_lattice()
		particle.propagate(lattice)

		self.cell_length = lattice.cell_length
		self.trajectory = particle.trajectory

		self.animate_plots()

	def continue_animation(self):
		#disable controls that cause bugs or visual artifacts while blitting
		self.view.run_button.configure(state ='disabled')
		self.view.continue_button.config(state = 'disabled')
		self.view.anim_speed_option.configure(state ='disabled')
		self.view.ellipse_scale.configure(state = 'disabled')

		#use the last particle coordinates of the previous run as the starting coordinates of the next run
		particle = Particle(self.trajectory[0][-1], self.trajectory[1][-1], self.trajectory[2][-1])
		lattice = self.get_lattice()
		particle.propagate(lattice)

		self.cell_length = lattice.cell_length
		self.trajectory = particle.trajectory

		self.animate_plots()

	def init_animation(self):
		#relimit the plot so all datapoints are within the plot window
		x_max, xp_max, s_max = np.max(self.trajectory, axis=1)
		x_min, xp_min, s_min = np.min(self.trajectory, axis=1)
		self.view.figure.relimit_orbit_plot(s_min, s_max, x_min, x_max)
		self.view.figure.relimit_phase_space_plot(x_min, x_max, xp_min, xp_max)

		#initialize the line artists. FuncAnimation will set new data for these lines on each frame
		self.orbit_line, = self.view.figure.orbit_plot.plot([],[], linewidth = 0.5, color = 'gray')
		self.phase_space_line, = self.view.figure.phase_space_plot.plot([],[], linewidth = 0.5, color = 'gray')

		if self.show_ellipse is True:
			self.view.ellipse_scale.configure(to = self.cell_length)
			self.view.figure.show_ellipse(start = self.view.ellipse_scale.get(), cell_length = self.cell_length)

		#init function must return an iterable of artists necessary for blitting
		return self.orbit_line, self.phase_space_line

	def animate_plots(self):
		self.animation = animation.FuncAnimation(fig = self.view.figure,
									  func = self.animation_fuction,
									  frames = len(self.trajectory[0]),
									  interval = self.view.anim_speed_option.get_speed(),
									  repeat = False,
									  blit = True,
									  init_func = self.init_animation)
		self.view.canvas_widget.draw()

	#Called for each frame of FuncAnimation. Must return an iterable of artists for blitting
	def animation_fuction(self, frame):
		self.orbit_line.set_data(self.trajectory[2][:frame+1], self.trajectory[0][:frame+1])
		self.phase_space_line.set_data(self.trajectory[0][:frame+1], self.trajectory[1][:frame+1])

		#Restore UI controls at the end of the animation.
		#Ideally would seperate this out
		if frame == max(range(len(self.trajectory[0]))):
			self.view.run_button.configure(state ='normal')
			self.view.anim_speed_option.configure(state ='normal')
			self.view.ellipse_scale.configure(state = 'normal')
			if self.run_active:
				self.view.continue_button.config(state = 'normal')

		return self.orbit_line, self.phase_space_line
		


if __name__ == '__main__':
	controller = Controller()
	controller.main()