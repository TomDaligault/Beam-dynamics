import tkinter as tk
from tkinter import ttk
import re

import matplotlib.pyplot 
from matplotlib.figure import Figure

class DigitEntry(ttk.Entry):
	def __init__(self, frame, **kwargs):
		super().__init__(frame, width=12, **kwargs)
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

class FloatEntry(ttk.Entry):
	def __init__(self, frame, **kwargs):
		super().__init__(frame, width=12, **kwargs)
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

class EllipseScale(tk.Scale):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(length=200, width=8, bg='#d9544f', bd=0,
								   showvalue = False, orient = 'horizontal', activebackground='#f0544f', troughcolor = "#e6e6e6",
								   sliderlength=5)

class LatticeControlFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.input_driftlength_label = tk.Label(self, text='drift length')
        self.input_focallength_label = tk.Label(self, text='focal length')
        self.num_cells_Label = tk.Label(self, text='cells')

        self.drift_length_Entry = FloatEntry(self, width=12)
        self.focal_length_Entry = FloatEntry(self, width=12)
        self.num_cells_Entry = DigitEntry(self, width=12)

        self.drift_length_Entry.insert(0, 10.0)
        self.focal_length_Entry.insert(0, 8.0)
        self.num_cells_Entry.insert(0, 12)

        self.input_driftlength_label.grid(row=0, column=0)
        self.input_focallength_label.grid(row=0, column=1)
        self.num_cells_Label.grid(row=0, column=2)
        self.drift_length_Entry.grid(row=1, column=0)
        self.focal_length_Entry.grid(row=1, column=1)
        self.num_cells_Entry.grid(row=1, column=2)


class plots(Figure):
    def __init__(self, figsize=(8.4, 4), *args, **kwargs):
        super().__init__(figsize = figsize, *args, **kwargs)
        self.orbit_plot = self.add_subplot(1,2,1)
        self.orbit_plot.set_title('orbit plot')
        self.orbit_plot.set_xlabel('s')
        self.orbit_plot.set_ylabel('x', rotation = 0)

        self.phase_space_plot = self.add_subplot(1,2,2)
        self.phase_space_plot.set_title('phase space plot')
        self.phase_space_plot.set_xlabel('x')
        self.phase_space_plot.set_ylabel('x\'', rotation = 0)

        self.tight_layout(pad=1.6)
        matplotlib.pyplot.tight_layout()

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
        for line in self.orbit_plot.get_lines():
                line.remove()
        for line in self.phase_space_plot.get_lines():
                line.remove()

        self.orbit_plot.set(xlim=(0, 0.1), ylim=(0, 0.1))
        self.phase_space_plot.set(xlim=(0, 0.1), ylim=(0, 0.1))

    def show_ellipse(self, start, cell_length):
        for line in self.orbit_plot.get_lines():
            line.set_markevery(( start, cell_length))
            line.set_marker('o')
            line.set_markerfacecolor('#d9544f')
            line.set_markeredgecolor('#d9544f')

        for line in self.phase_space_plot.get_lines():
            line.set_markevery(( start, cell_length))
            line.set_marker('o')
            line.set_markerfacecolor('#d9544f')
            line.set_markeredgecolor('#d9544f')

        self.canvas.draw()
