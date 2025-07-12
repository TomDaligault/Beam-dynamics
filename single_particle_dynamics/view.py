import tkinter as tk
from tkinter import ttk
from numpy import random

import CustomWidgets

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class View(tk.Tk):
	#list of names used to dynamically create tab buttons
	tab_names = ["exercise 1", "exercise 2", "exercise 3", 'exercise 4', ' ']

	def __init__(self):
		super().__init__()
		self.title('view')

		#callback registry
		self.callback_registry = {}

		#dictionary of tab button and their names, populated dynamically as buttons are created.
		self.tab_buttons = {}

	def main(self):
		#self contains the user frame (left) and figure frame (right)
		self._make_user_frame(self)
		self._make_figure_frame(self)

		#user frames is split vertically. Tabs frame on top, control frame underneath. Tabs frame contains tab buttons
		self._make_tabs_frame(self.user_frame)
		self._make_control_frame(self.user_frame)

		#control frame contains all other user-control frames.
		#widgets inside these frames must be placed using the grid() method to make their visibility toggleable. 
		self._make_lattice_frame(self.control_frame)
		self._make_particle_frame(self.control_frame)
		self._make_animation_frame(self.control_frame)
		self._make_ellipse_frame(self.control_frame)

		self.mainloop()

	def _make_user_frame(self, frame):
		self.user_frame = tk.Frame(frame)
		self.user_frame.pack(side='left', fill='y')

	def _make_figure_frame(self, frame):
		frame = tk.Frame(frame)
		frame.pack(side='right', fill='both', expand=True)

		self.figure = CustomWidgets.plots()
		self.canvas_widget = FigureCanvasTkAgg(figure=self.figure, master=frame)
		self.canvas_widget.get_tk_widget().pack(fill='both', expand=True)

	def _make_control_frame(self, frame):
		self.control_frame = tk.Frame(frame)
		self.control_frame.pack(side='top')

	def _make_tabs_frame(self, frame):
		frame = tk.Frame(frame)
		frame.pack(side='top', fill='x')

		#dynamically create buttons, assign them a command from the controller, and collects buttons/names in the tab_buttons dictionary
		for name in self.tab_names:
			button = tk.Button(frame, text=name, command=lambda n=name: self.execute_callback('change_tab', n))
			self.tab_buttons[name] = button
			button.pack(side='left', expand=True, fill='x')

	def _make_lattice_frame(self, parent):
		self.lattice_frame = tk.Frame(parent)
		self.lattice_frame.pack(side='top', pady=10)

		self.drift_Entry = CustomWidgets.FloatEntry(self.lattice_frame)
		self.focus_Entry = CustomWidgets.FloatEntry(self.lattice_frame)
		self.cell_Entry = CustomWidgets.DigitEntry(self.lattice_frame)

		self.set_lattice_inputs(10, 8, 12)

		ttk.Label(self.lattice_frame, text='drift length').grid(row = 0, column = 0)
		ttk.Label(self.lattice_frame, text='focal length').grid(row = 0, column = 1)
		ttk.Label(self.lattice_frame, text='num cells').grid(row = 0, column = 2)
		self.drift_Entry.grid(row = 1, column = 0)
		self.focus_Entry.grid(row = 1, column = 1)
		self.cell_Entry.grid(row = 1, column = 2)

	def _make_particle_frame(self, parent):
		self.particle_frame = tk.Frame(parent)
		self.particle_frame.pack(side='top', pady=10)

		self.x_Entry = CustomWidgets.FloatEntry(self.particle_frame)
		self.xp_Entry = CustomWidgets.FloatEntry(self.particle_frame)

		self.set_particle_inputs(0.4, -0.1)

		ttk.Label(self.particle_frame, text='Initial x').grid(row=0, column=0)
		ttk.Label(self.particle_frame, text='Initial x\'').grid(row=1, column=0)
		self.x_Entry.grid(row=0, column=1)
		self.xp_Entry.grid(row=1, column=1)
		tk.Button(self.particle_frame, text='randomize', command=self.randomize_particle).grid(row=2, column=0, columnspan=2, sticky='WE')

	def _make_animation_frame(self, parent):
		frame = tk.Frame(parent)
		frame.pack(side='top', pady=10)

		self.run_button = tk.Button(frame, text="run", command=lambda: self.execute_callback('run_animation'))
		self.continue_button = tk.Button(frame, text="continue", state='disabled', command=lambda: self.execute_callback('continue_animation'))
		self.clear_button = tk.Button(frame, text="clear", command=self.clear_plots)
		self.anim_speed_option = CustomWidgets.PlaySpeedOptionMenu(frame)

		self.anim_speed_option.grid(row = 0, column = 0)
		self.run_button.grid(row = 0, column = 1)
		self.continue_button.grid(row = 0, column = 2)
		self.clear_button.grid(row = 0, column = 3)

	def _make_ellipse_frame(self, parent):
		self.ellipse_frame = tk.Frame(parent)
		self.ellipse_frame.pack()
		self.cell_diagram = CustomWidgets.CellDiagram(self.ellipse_frame)
		self.ellipse_scale = CustomWidgets.EllipseScale(self.ellipse_frame, command=lambda scale_value: self.execute_callback('update_ellipse', scale_value))

		self.cell_diagram.grid(row = 0, column = 0)
		self.ellipse_scale.grid(row = 0, column = 0)





	def register_callback(self, callback_name, callback_func):
		self.callback_registry[callback_name] = callback_func

	def execute_callback(self, callback_name, *args, **kwargs):
		if callback_name in self.callback_registry:
			self.callback_registry[callback_name](*args, **kwargs)
		else:
			pass





	def set_lattice_inputs(self, drift_length, focal_length, num_cells):		
		self.drift_Entry.delete(0, tk.END)
		self.focus_Entry.delete(0, tk.END)
		self.cell_Entry.delete(0, tk.END)
		self.drift_Entry.insert(0, drift_length)
		self.focus_Entry.insert(0, focal_length)
		self.cell_Entry.insert(0, num_cells)

	def set_particle_inputs(self, x, xp):
		self.x_Entry.delete(0, tk.END)
		self.xp_Entry.delete(0, tk.END)
		self.x_Entry.insert(0, x)
		self.xp_Entry.insert(0, xp)

	def randomize_particle(self):
		self.x_Entry.delete(0, tk.END)
		self.xp_Entry.delete(0, tk.END)
		self.x_Entry.insert(0, round(random.normal(),2))
		self.xp_Entry.insert(0, round(random.normal(),2))

	def get_particle_inputs(self):
		x = self.x_Entry.get()
		xp = self.xp_Entry.get()
		s = 0

		return x, xp, s

	def get_lattice_inputs(self):
		drift_length = self.drift_Entry.get()
		focal_length = self.focus_Entry.get()
		num_cells = self.cell_Entry.get()

		return drift_length, focal_length, num_cells
	def disable_animation_controls(self):
		#disable controls that would cause visual artifacts while blitting
		self.run_button.configure(state = 'disabled')
		self.continue_button.config(state = 'disabled')
		self.anim_speed_option.configure(state ='disabled')
		self.ellipse_scale.configure(state = 'disabled')

	def restore_animation_controls(self):
		self.run_button.configure(state ='normal')
		self.continue_button.config(state = 'normal')
		self.anim_speed_option.configure(state ='normal')
		self.ellipse_scale.configure(state = 'normal')

	#raise all tab buttons, then sink a specified button. Called whenever a tab button is clicked.
	def sink_selected_tab(self, button):
		for _ in self.tab_buttons.values():
			_.configure(relief='raised')
		self.tab_buttons[button].configure(relief='sunken')

	#Used to insure that every widget is visible after changing tabs.
	def restore_default_control_frame(self):
		for frame in self.control_frame.children.values():
			for widget in frame.children.values():
				widget.grid()
				widget.configure(state='normal')
		self.continue_button.configure(state='disabled')

	#Stop animation, restore UI controls, clear plots. Used when changing tabs, or manually clearing plots.
	def clear_plots(self):
		self.figure.stop_animation()

		self.run_button.config(state = 'normal')
		self.continue_button.config(state = 'disabled')
		self.anim_speed_option.config(state = 'normal')
		self.ellipse_scale.configure(state = 'normal')

		self.figure.clear_plots()
		self.canvas_widget.draw()

	def disable_widgets(self, frame):
		for widget in frame.children.values():
			widget.configure(state='disabled')

	def set_exercise_1(self):
		self.set_lattice_inputs(10, 8, 1)
		self.set_particle_inputs(0.4, -0.1)
		self.anim_speed_option.set_speed('slow')
		self.anim_speed_option.grid_remove()
		self.cell_diagram.grid_remove()
		self.ellipse_scale.grid_remove()
		self.continue_button.grid_remove()
		self.disable_widgets(self.lattice_frame)

	def set_exercise_2(self):
		self.set_lattice_inputs(10, 8, 12)
		self.set_particle_inputs(0.4, -0.1)
		self.anim_speed_option.set_speed('med')
		self.anim_speed_option.grid_remove()
		self.cell_diagram.grid_remove()
		self.ellipse_scale.grid_remove()
		self.continue_button.grid_remove()
		self.disable_widgets(self.particle_frame)

	def set_exercise_3(self):
		self.set_exercise_2()
		self.anim_speed_option.set_speed('med')
		self.set_lattice_inputs(10, 40, 25)
		self.set_particle_inputs(0.4, -0.1)

	def set_exercise_4(self):
		self.anim_speed_option.set_speed('fast')
		self.set_lattice_inputs(10, 40, 25)
		self.set_particle_inputs(0.4, -0.1)
		self.anim_speed_option.grid_remove()
		self.continue_button.grid_remove()
		self.disable_widgets(self.lattice_frame)

	def relimit_plots(self, x_max, xp_max, s_max, x_min, xp_min, s_min):
		self.figure.relimit_orbit_plot(s_min, s_max, x_min, x_max)
		self.figure.relimit_phase_space_plot(x_min, x_max, xp_min, xp_max) 

if __name__ == '__main__':
	view = View()
	view.main()
	