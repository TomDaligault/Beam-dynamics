import tkinter as tk
from tkinter import ttk
import re

class DigitEntry(ttk.Entry):
	def __init__(self, frame, **kwargs):
		super().__init__(frame, **kwargs)
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
		super().__init__(frame, **kwargs)
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
        self.configure( length=200, width=8, bg='#d9544f', bd=0,
								   showvalue = False, orient = 'horizontal', activebackground='#f0544f', troughcolor = "#e6e6e6",
								   sliderlength=5)