import tkinter as tk
import numpy as np
from AcceleratorObjects import Particle, Lattice

from model import Model
from view import View

class Controller:
	def __init__(self):
		self.model = Model()
		self.view = View(self)
		self.show_ellipse = False

	def main(self):
		self.view.main()

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

		if button == 'exercise 1':
			self.set_exercise_1()
		if button == 'exercise 2':
			self.set_exercise_2()
		if button == 'exercise 3':
			self.set_exercise_3()
		if button == 'exercise 4':
			self.set_exercise_4()

	def clear_plots(self):
		self.view.plots_figure.clear_plots()
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

	def randomize(self):
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
		self.view.speed_options.grid_remove()
		self.view.cell_diagram.grid_remove()
		self.view.ellipse_scale.grid_remove()
		self.view.continue_button.grid_remove()
		self.disable_widgets(self.view.lattice_frame)

	def set_exercise_2(self):
		self.show_ellipse = False
		self.view.speed_options.grid_remove()
		self.view.cell_diagram.grid_remove()
		self.view.ellipse_scale.grid_remove()
		self.view.continue_button.grid_remove()
		self.disable_widgets(self.view.particle_frame)

	def set_exercise_3(self):
		self.show_ellipse = True
		self.set_exercise_2()

	def set_exercise_4(self):
		self.show_ellipse = True
		self.view.speed_options.grid_remove()
		self.view.continue_button.grid_remove()

	def run_animation(self):
		x = float(self.view.x_Entry.get())
		xp = float(self.view.xp_Entry.get())
		s = 0

		drift_length = float(self.view.drift_Entry.get())
		focal_length = float(self.view.focus_Entry.get())
		num_cells = int(self.view.cell_Entry.get())

		particle = Particle(x, xp, s)
		lattice = Lattice(drift_length, focal_length, num_cells)
		self.model.propagate(particle, lattice)
		x_values, xp_values, s_values = self.model.particle_trajectory.values()


		self.view.plots_figure.orbit_plot.plot(s_values, x_values)
		self.view.plots_figure.phase_space_plot.plot(x_values, xp_values)

		self.view.plots_figure.relimit_orbit_plot(min(s_values), max(s_values), min(x_values), max(x_values))
		self.view.plots_figure.relimit_phase_space_plot(min(x_values), max(x_values), min(xp_values), max(xp_values))
		self.view.canvas_widget.draw()


if __name__ == '__main__':
	controller = Controller()
	controller.main()