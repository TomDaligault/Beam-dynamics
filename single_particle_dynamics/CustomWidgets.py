import tkinter as tk
from tkinter import ttk
import re

import numpy as np
import matplotlib.pyplot 
from matplotlib.figure import Figure
import matplotlib.animation as animation

#DigitEntry turns text red on focus-out if the text contains anything other positive whole numbers
class DigitEntry(ttk.Entry):
	def __init__(self, parent, **kwargs):
		super().__init__(parent, width=12, **kwargs)
		validation_function = self.register(self.validate_digit)
		self.configure(validate='focusout', validatecommand = (validation_function, '%P'))

	def validate_digit(self, value):
		pattern = r'^[1-9]\d*$'
		if re.fullmatch(pattern, value) is None: #if no match
			self.configure(foreground ='red')
			return False
		else:
			self.configure(foreground ='black')
			return True

	def get(self):
		return int(super().get())

#FloatEntry turns text red on focus-out if the text contains anything other than a float
class FloatEntry(ttk.Entry):
	def __init__(self, parent, **kwargs):
		super().__init__(parent, width=12, **kwargs)
		validation_function = self.register(self.validate_float)
		self.configure(validate='focusout', validatecommand = (validation_function, '%P'))

	def validate_float(self, value):
		pattern = r'^-?\d+(\.\d+)?$'
		if re.fullmatch(pattern, value) is None: #if no match
			self.configure(foreground ='red')
			return False
		else:
			self.configure(foreground ='black')
			return True

	def get(self):
		return float(super().get())

#CellDiagram is a canvas object using rectangles and ovals to make a rough FODO cell diagram
class CellDiagram(tk.Canvas):
	def __init__(self, parent, width=200, height=100, **kwargs):
		super().__init__(parent, width=width, height=height, **kwargs)
		# self.user_point = self.create_oval(-3, (height/2)-3, 3, (height/2)+3, fill='#d9544f', width=0)

		# Store the dimensions and radius
		x_offset = width/6
		y_offset = height/20
		#draw the focusing quad
		self.create_oval(2 +width/20, 2, width/4 + 2 - width/20, height+1, fill='#b5eef7', width=0)
		self.create_rectangle(2, 2, width/4 + 2, height+1)

		#draw the defocusing quad
		self.create_rectangle(2 + width/2, 2, 3*width/4, height+4, fill='#b5eef7', width=0)
		self.create_oval(2 + width/2 - x_offset, -y_offset/2, 3*width/4 - x_offset, height + y_offset/2 + 3, fill='#F0F0F0', width=0)
		self.create_oval(2 + width/2 + x_offset, -y_offset/2, 3*width/4 + x_offset, height + y_offset/2 + 3, fill='#F0F0F0', width=0)
		self.create_rectangle(2 + width/2, 2, 3*width/4 + 2, height+1)

#A pre-configured tkinter scale. Changes color if disabled.
class EllipseScale(tk.Scale):
	def __init__(self, parent, **kwargs):
		super().__init__(parent, **kwargs)
		state = kwargs.get('state', 'normal')
		self.configure(length=200, width=8, bd=0, state=state,
								   showvalue = False, orient = 'horizontal', activebackground='#f0544f', troughcolor = '#e6e6e6',
								   sliderlength=5)

	def configure(self, **kwargs):
		if 'state' in kwargs:
			state = kwargs['state']
			if state == 'disabled':
				self.configure(bg = '#F0F0F0')
			else:
				self.configure(bg = '#d9544f')
		super().configure(**kwargs)
		

class PlaySpeedOptionMenu(tk.OptionMenu):
	anim_speeds = {'fast': 0, 'med': 6, 'slow': 30}
	def __init__(self, master, **kwargs):
		self.speed_var = tk.StringVar(value='fast')
		super().__init__(master, self.speed_var, *self.anim_speeds.keys(), **kwargs)

	def set_speed(self, speed):
		if speed in self.anim_speeds:
			self.speed_var.set(speed)
	
	def get_speed(self):
		return self.anim_speeds.get(self.speed_var.get(), 0)

#Custom matplotlib Figure with preconfigured subplots, titles, and axes. 
class plots(Figure):
	line_kwargs = {'linewidth' : 0.5, 'markerfacecolor':'#d9544f', 'markeredgecolor':'#d9544f', 'color' : 'gray', 'animated': True}

	def __init__(self, figsize=(8.4, 4), *args, **kwargs):
		super().__init__(figsize = figsize, *args, **kwargs)
		self.orbit_plot = self.add_subplot(1,2,1)
		self.orbit_plot.set_title('orbit plot')
		self.orbit_plot.set_xlabel('s')
		self.orbit_plot.set_ylabel('x', rotation = 0)
		self.orbit_scatter = self.orbit_plot.scatter([],[], color = '#d9544f', s=60, animated=True)

		self.phase_space_plot = self.add_subplot(1,2,2)
		self.phase_space_plot.set_title('phase space plot')
		self.phase_space_plot.set_xlabel('x')
		self.phase_space_plot.set_ylabel('x\'', rotation = 0)
		self.phase_space_scatter = self.phase_space_plot.scatter([],[], color = '#d9544f', s=60, animated=True)

		self.orbit_plot.set(xlim=(0, 0.1), ylim=(0, 0.1))
		self.phase_space_plot.set(xlim=(0, 0.1), ylim=(0, 0.1))

		self.tight_layout(pad=1.6)
		matplotlib.pyplot.tight_layout()

	def init_artists(self, show_ellipse=False, marker_start=None, cell_length=None):
		orbit_line, = self.orbit_plot.plot([],[], **self.line_kwargs)
		phase_space_line, = self.phase_space_plot.plot([],[], **self.line_kwargs)

		if show_ellipse:
			self.show_ellipse(marker_start, cell_length)

		return orbit_line, phase_space_line

	def animate_plots(self, trajectory, anim_speed=0, show_ellipse=False, marker_start=None, cell_length=None, callback=None):
		#New lines are made for each animation, lines from previous animations continue to exists unclear clear_plots is called.
		orbit_line, phase_space_line = self.init_artists(show_ellipse, marker_start, cell_length)

		self.animation = animation.FuncAnimation(fig = self,
									  func = self.animation_fuction,
									  fargs = (trajectory, orbit_line, phase_space_line, callback),
									  frames = len(trajectory),
									  interval = anim_speed,
									  repeat = False,
									  blit = True)

	#Called for each frame of FuncAnimation. Must return an iterable of artists for blitting
	def animation_fuction(self, frame, trajectory, orbit_line, phase_space_line, callback):
		orbit_line.set_data(trajectory[:frame+1,2], trajectory[:frame+1,0])
		phase_space_line.set_data(trajectory[:frame+1,0], trajectory[:frame+1,1])

		self.orbit_scatter.set_offsets(np.column_stack((trajectory[frame][2, 0], trajectory[frame][0, 0])))
		self.phase_space_scatter.set_offsets(np.column_stack((trajectory[frame][0, 0], trajectory[frame][1, 0])))

		#If a callback function is provided, execute the callback at the end of the animation.
		#Used to restore functionality to UI controls.
		if frame == max(range(len(trajectory))) and callback:
			callback()

		return orbit_line, phase_space_line, self.orbit_scatter, self.phase_space_scatter


	#Pauses the animation. Used to prevent funcanimation from throwing errors after artists are clear from the plot.
	def stop_animation(self):
		try:
			self.animation.pause()
		except AttributeError:
			pass 

	def relimit_orbit_plot(self, smin, smax, xmin, xmax):
		current_smin, current_smax, current_xmin, current_xmax = self.orbit_plot.axis()

		#check if data will exceed current plot limits, adjust plot limits if necessary
		if current_smin > smin:
			self.orbit_plot.set_xlim(xmin = smin)

		if current_smax < smax:
			self.orbit_plot.set_xlim(xmax = smax)

		if current_xmin > xmin:
			self.orbit_plot.set_ylim(ymin = xmin - 0.5)

		if current_xmax < xmax:
			self.orbit_plot.set_ylim(ymax = xmax + 0.5)

	def relimit_phase_space_plot(self, xmin, xmax, xpmin, xpmax):
		current_xmin, current_xmax, current_xpmin, current_xpmax = self.phase_space_plot.axis()

		#check if data will exceed current plot limits, adjust plot limits if necessary
		if current_xmin > xmin:
			self.phase_space_plot.set_xlim(xmin = xmin*1.1)

		if current_xmax < xmax:
			self.phase_space_plot.set_xlim(xmax = xmax*1.1)

		if current_xpmin > xpmin:
			self.phase_space_plot.set_ylim(ymin = xpmin*1.1)

		if current_xpmax < xpmax:
			self.phase_space_plot.set_ylim(ymax = xpmax*1.1)

	def clear_plots(self):
		#Scatter plots can have their data cleared
		self.orbit_scatter.set_offsets([0,0])
		self.phase_space_scatter.set_offsets([0,0])

		#Lines must be removed 
		for line in self.orbit_plot.get_lines():
				line.remove()
		for line in self.phase_space_plot.get_lines():
				line.remove()

		self.orbit_plot.set(xlim=(0, 0.1), ylim=(0, 0.1))
		self.phase_space_plot.set(xlim=(0, 0.1), ylim=(0, 0.1))

	def show_ellipse(self, marker_start, cell_length):
		for line in self.orbit_plot.get_lines():
			line.set_markevery((marker_start, cell_length))
			line.set_marker('o')

		for line in self.phase_space_plot.get_lines():
			line.set_markevery((marker_start, cell_length))
			line.set_marker('o')

		self.canvas.draw()

