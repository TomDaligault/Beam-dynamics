import tkinter as tk
from tkinter import ttk

import CustomWidgets

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class View(tk.Tk):

	tab_names = ["exercise 1", "exercise 2", "exercise 3", 'exercise 4', ' ']


	def __init__(self, controller):
		super().__init__()
		self.title('view')
		self.controller = controller
		self.tab_buttons ={}

	def main(self):
		#self contains the user frame (left) and figure frame (right)
		self._make_user_frame(self)
		self._make_figure_frame(self)

		#user frames is split vertically. Tabs frame on top, control frame underneath. Tabs frame contains tab buttons
		self._make_tabs_frame(self.user_frame)
		self._make_control_frame(self.user_frame)

		#control frame contains all UI frames.
		#widgets inside these UI frames must use the grid() method
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
		self.canvas_widget.get_tk_widget().pack( fill='both', expand=True)

	def _make_control_frame(self, frame):
		self.control_frame = tk.Frame(frame)
		self.control_frame.pack(side='top')

	def _make_tabs_frame(self, frame):
		frame = tk.Frame(frame)
		frame.pack(side='top', fill='x')

		for name in self.tab_names:
			button = tk.Button(frame, text=name, command = lambda n=name: self.controller.change_tab(n))
			self.tab_buttons[name] = button
			button.pack(side='left', expand=True, fill='x')

	def _make_lattice_frame(self, parent):
		self.lattice_frame = tk.Frame(parent)
		self.lattice_frame.pack(side='top', pady=10)

		self.drift_Entry = CustomWidgets.FloatEntry(self.lattice_frame)
		self.focus_Entry = CustomWidgets.FloatEntry(self.lattice_frame)
		self.cell_Entry = CustomWidgets.DigitEntry(self.lattice_frame)

		self.controller.set_lattice_inputs(10, 8, 12)

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

		self.controller.set_particle_inputs(0.4, -0.1)

		ttk.Label(self.particle_frame, text='Initial x').grid(row = 0, column = 0)
		ttk.Label(self.particle_frame, text='Initial x\'').grid(row = 1, column = 0)
		self.x_Entry.grid(row = 0, column = 1)
		self.xp_Entry.grid(row = 1, column = 1)
		tk.Button(self.particle_frame, text='random', command = self.controller.randomize).grid(row = 2, column = 0, columnspan =2, sticky='WE')

	def _make_animation_frame(self, parent):
		frame = tk.Frame(parent)
		frame.pack(side='top', pady=10)

		animation_speeds ={'fast': 0, 'med': 6, 'slow':30}
		speed_option = tk.StringVar(frame)
		speed_option.set('fast')

		self.run_button = tk.Button(frame, text="run", command = self.controller.run_animation)
		self.continue_button = tk.Button(frame, text="continue", state = 'disabled', command = self.controller.continue_animation)
		self.clear_button = tk.Button(frame, text="clear", command = self.controller.clear_plots)
		self.speed_options = tk.OptionMenu(frame, speed_option, *animation_speeds.keys())


		self.speed_options.grid(row = 0, column = 0)
		self.run_button.grid(row = 0, column = 1)
		self.continue_button.grid(row = 0, column = 2)
		self.clear_button.grid(row = 0, column = 3)

	def _make_ellipse_frame(self, parent):
		self.ellipse_frame = tk.Frame(parent)
		self.ellipse_frame.pack()
		self.cell_diagram = CustomWidgets.CellDiagram(self.ellipse_frame)
		self.ellipse_scale = CustomWidgets.EllipseScale(self.ellipse_frame, command = self.controller.update_ellipse)

		self.cell_diagram.grid(row = 0, column = 0)
		self.ellipse_scale.grid(row = 0, column = 0)

if __name__ == '__main__':
	pass