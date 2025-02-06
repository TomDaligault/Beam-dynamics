from tkinter import *
import CustomWidgets

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
import matplotlib.animation as animation


class ParticleSimulatorGUI:
    def __init__(self, window):
    #initialize lists used to collect particle propagation datapoints
        self.x_values = []
        self.xp_values = []
        self.s_values = []
        self.s=0

    #lattice elements are subdivided using the step values below.
    #Higher values gives the ellipse slider more resolution, but means more compute time and more animation frames.
        self.drift_steps = 5
        self.quad_steps = self.drift_steps

    #initialize parameters used in animations
        #show_ellipse toggles the markers for cell-to-cell behavior
        #stop_animation is used to interrupt the animation
        #run_active is used to determine if the continue button should be enabled
        #animation_speeds is used to change the frames per second of the animation depending on the exercise
        self.show_ellipse = True
        self.stop_animation = False
        self.run_active = False
        self.animation_speeds = {'fast':0, 'med':6, 'slow':30}
        self.animation_speed = self.animation_speeds['fast']

    #creating the main window and pack frames into it.
        #plot_frame contains the plots
        #exercises_frame contains all the user controls.
        self.main_window = window
        self.exercises_frame = Frame(self.main_window, bg='#F0F0F0')
        self.exercises_frame.pack(side='left', fill='both')
        self.plot_frame = Frame(self.main_window)
        self.plot_frame.pack(side='right', fill='both')

        #creates and packs exercise_frame into exercises_frame 
        #contains all the exercises buttons
        self.make_exercise_frame(self.exercises_frame)

        #creates plots and adds them to plot_frame
        self.make_initial_plots(self.plot_frame)

        #user_frame contains all other user controls
        #this seperation allows us to can clear all widgets except the exercise buttons.
        self.user_frame = Frame(self.exercises_frame, bg='#F0F0F0')
        self.user_frame.pack(side='top', fill='both')

    #populate user_frame with default controls
        #user controls are grouped into different frames based on functions
        self.make_lattice_frame(self.user_frame)
        self.make_particle_frame(self.user_frame)
        self.make_animation_control_frame(self.user_frame)
        self.make_ellipse_control_frame(self.user_frame)

#creates and packs exercise_frame inside of parent_frame. Contains buttons to switch between exercises
    def make_exercise_frame(self, parent_frame):
        self.exercise_frame = Frame(parent_frame)
        self.exercise_frame.pack(side=TOP, padx=0, pady=(0,20))

        self.exercise_1_button = Button(self.exercise_frame, text='exercise 1', 
            command = lambda: [self.toggle_exercise_buttons(self.exercise_1_button),
            self.setup_exercise_1()])
        self.exercise_2_button = Button(self.exercise_frame, text='exercise 2', 
            command = lambda: [self.toggle_exercise_buttons(self.exercise_2_button),
            self.setup_exercise_2()])
        self.exercise_3_button = Button(self.exercise_frame, text='exercise 3', 
            command = lambda: [self.toggle_exercise_buttons(self.exercise_3_button),
            self.setup_exercise_3()])
        self.exercise_4_button = Button(self.exercise_frame, text='exercise 4', 
            command = lambda: [self.toggle_exercise_buttons(self.exercise_4_button),
            self.setup_exercise_4()])
        self.sandbox_button = Button(self.exercise_frame, text='sandbox',
         command = lambda: [self.toggle_exercise_buttons(self.sandbox_button),
         self.setup_default()])

        self.exercise_1_button.pack(side='left')
        self.exercise_2_button.pack(side='left')
        self.exercise_3_button.pack(side='left')
        self.exercise_4_button.pack(side='left')
        self.sandbox_button.pack(side='left')

        self.sandbox_button.configure(relief = 'sunken')

#creates and packs lattice_frame inside of parent_frame. contains widgets to change lattice parameters
    def make_lattice_frame(self, parent_frame):
        self.lattice_frame = Frame(parent_frame)
        self.lattice_frame.pack(side='top', padx=10, pady=(0,0))

        self.input_driftlength_label = Label(self.lattice_frame, text='drift length')
        self.input_focallength_label = Label(self.lattice_frame, text='focal length')
        self.num_cells_Label = Label(self.lattice_frame, text='cells')

        self.drift_length_Entry = CustomWidgets.FloatEntry(self.lattice_frame, width=12)
        self.focal_length_Entry = CustomWidgets.FloatEntry(self.lattice_frame, width=12)
        self.num_cells_Entry = CustomWidgets.DigitEntry(self.lattice_frame, width=12)

        self.drift_length_Entry.insert(0, 10.0)
        self.focal_length_Entry.insert(0, 8.0)
        self.num_cells_Entry.insert(0, 10)

        self.input_driftlength_label.grid(row=0, column=0)
        self.input_focallength_label.grid(row=0, column=1)
        self.num_cells_Label.grid(row=0, column=2)
        self.drift_length_Entry.grid(row=1, column=0)
        self.focal_length_Entry.grid(row=1, column=1)
        self.num_cells_Entry.grid(row=1, column=2)

#creates and packs particle_frame inside of parent_frame. contains widgets to change particle initial conditions
    def make_particle_frame(self, parent_frame):
        self.particle_frame = Frame(parent_frame)
        self.particle_frame.pack(side='top', padx=0, pady=(40,0))

        self.xEntry_label = Label(self.particle_frame, text="inital x")
        self.xpEntry_label = Label(self.particle_frame, text="inital x\'")

        self.xEntry = CustomWidgets.FloatEntry(self.particle_frame)
        self.xpEntry = CustomWidgets.FloatEntry(self.particle_frame)
        self.randomize_button = Button(self.particle_frame, text="randomize", command = self.randomize)

        self.xEntry.insert(0, 0.4)
        self.xpEntry.insert(0, -0.1)

        self.xEntry_label.grid(row=0, column=0)
        self.xEntry.grid(row=0, column=1)
        self.xpEntry_label.grid(row=1, column=0)
        self.xpEntry.grid(row=1, column=1)
        self.randomize_button.grid(row=2, column=0, columnspan=2, sticky='WE')

#creates and packs animation_control_frame inside of parent_frame. contains widgets to run the animation
    def make_animation_control_frame(self, parent_frame):
        self.animation_control_frame = Frame(parent_frame)
        self.animation_control_frame.pack(side='top', padx=0, pady=(20,0))

        speed_option = StringVar(self.animation_control_frame)
        speed_option.set('fast')
        self.animation_speed_dropdown = OptionMenu(self.animation_control_frame, speed_option, *self.animation_speeds.keys(), command=self.set_animation_speed)


        self.run_button = Button(self.animation_control_frame, text="run",
                                command=lambda: [self.run_animation()])
        self.continue_button = Button(self.animation_control_frame, text="continue", state = 'disabled',
                                command=lambda: [self.continue_animation()])
        self.clear_button = Button(self.animation_control_frame, text="clear", command = self.clear_plots)

        self.animation_speed_dropdown.pack(side='left')
        self.run_button.pack(side='left')
        self.continue_button.pack(side='left')
        self.clear_button.pack(side='left')

#creates and packs ellipse_control_frame inside of parent_frame. contains cell diagram and cell-to-cell slider
    def make_ellipse_control_frame(self, parent_frame):
        self.ellipse_control_frame = Frame(parent_frame)
        self.ellipse_control_frame.pack(side='top', padx=0, pady=(20,20))

        self.cell_diagram = CustomWidgets.CellDiagram(self.ellipse_control_frame, width=200, height=100)
        self.ellipse_scale = CustomWidgets.EllipseScale(self.ellipse_control_frame, to = 2*(self.quad_steps + self.drift_steps), command = self.update_ellipse)

        self.cell_diagram.grid(row=0,column=0)
        self.ellipse_scale.grid(row=0, column=0)


#initializes the plots and add them to plot_frame 
    def make_initial_plots(self, parent_frame):
        self.fig, (self.orbit_plot, self.phase_space_plot) = plt.subplots(1,2, figsize=(8.4, 4))
        plt.subplots_adjust(wspace=0.26)
        self.orbit_plot.set_title('orbit plot')
        self.orbit_plot.set_xlabel('s')
        self.orbit_plot.set_ylabel('x', rotation=0)
        self.phase_space_plot.set_title('phase space plot')
        self.phase_space_plot.set_xlabel('x')
        self.phase_space_plot.set_ylabel('x\'', rotation=0)

        self.orbit_data, = self.orbit_plot.plot([],[], linewidth = 0.5, color = 'gray')
        self.orbit_ellipse_data, = self.orbit_plot.plot([],[], linestyle ='None', marker ='o', color = '#d9544f')

        self.phase_space_data, = self.phase_space_plot.plot([],[], linewidth = 0.5, color = 'gray')
        self.phase_space_ellipse_data, = self.phase_space_plot.plot([],[], linestyle ='None', marker ='o', color = '#d9544f')

        self.canvas = FigureCanvasTkAgg(figure=self.fig, master=parent_frame)
        self.canvas.get_tk_widget().pack()

#toggles the state of exercise butttons
    def toggle_exercise_buttons(self, button):
        for widget in self.exercise_frame.winfo_children():
            if isinstance(widget, Button):
                widget.configure(relief = 'raised')

        button.configure(relief = 'sunken')

#clears all widgets in user_frame, sets animation defaults, repopulates the default UI
    def setup_default(self):
        for widget in self.user_frame.winfo_children():
            widget.destroy()
        
        self.show_ellipse = True
        self.animation_speed = self.animation_speeds['fast']

        self.make_lattice_frame(self.user_frame)
        self.make_particle_frame(self.user_frame)
        self.make_animation_control_frame(self.user_frame)
        self.make_ellipse_control_frame(self.user_frame)
        self.clear_plots()

#sets default UI, then disables or removes specific widgets. Sets lattice parameters and animation parameters
    def setup_exercise_1(self):
        self.setup_default()
        self.animation_speed_dropdown.pack_forget()
        self.continue_button.pack_forget()
        self.ellipse_control_frame.pack_forget()
        self.clear_plots()

        self.show_ellipse = False
        self.animation_speed = self.animation_speeds['slow']

        self.num_cells_Entry.delete(0, 'end')
        self.num_cells_Entry.insert(0, 1)

        self.disable_all_widgets(self.lattice_frame)


#sets default UI, then disables or removes specific widgets. Sets lattice parameters and animation parameters
    def setup_exercise_2(self):
        self.setup_default()
        self.ellipse_control_frame.pack_forget()
        self.animation_speed_dropdown.pack_forget()
        self.continue_button.pack_forget()
        self.clear_plots()

        self.show_ellipse = False
        self.animation_speed = self.animation_speeds['slow']

        self.disable_all_widgets(self.particle_frame)

#sets default UI, then disables or removes specific widgets. Sets lattice parameters and animation parameters
    def setup_exercise_3(self):
        self.setup_default()
        self.animation_speed_dropdown.pack_forget()
        self.continue_button.pack_forget()
        self.ellipse_control_frame.pack_forget()
        self.clear_plots()

        self.show_ellipse = True
        self.animation_speed = self.animation_speeds['med']

        self.focal_length_Entry.delete(0, 'end')
        self.focal_length_Entry.insert(0, 40)
        self.num_cells_Entry.delete(0, 'end')
        self.num_cells_Entry.insert(0, 25)


        self.disable_all_widgets(self.particle_frame)

#sets default UI, then disables or removes specific widgets. Sets lattice parameters and animation parameters
    def setup_exercise_4(self):
        self.setup_default()
        self.animation_speed_dropdown.pack_forget()
        self.continue_button.pack_forget()

        self.animation_speed = self.animation_speeds['med']

        self.focal_length_Entry.delete(0, 'end')
        self.focal_length_Entry.insert(0, 40)
        self.num_cells_Entry.delete(0, 'end')
        self.num_cells_Entry.insert(0, 25)

        self.disable_all_widgets(self.lattice_frame)

#disables all widgets in an input frame
    def disable_all_widgets(self, frame):
        for widget in frame.winfo_children():
            widget.config(state='disabled')

#randomize the particle initial conditions, picking from a gaussian
    def randomize(self):
        self.xEntry.delete(0,'end')
        self.xpEntry.delete(0,'end')
        self.xEntry.insert(0, round(np.random.normal(),2))
        self.xpEntry.insert(0, round(np.random.normal(),2))

#updates animation speed from user input
    def set_animation_speed(self, speed):
        self.animation_speed = self.animation_speeds[speed]
        print(self.animation_speed)




#stop animation, resets animation controls, clears plots.
    def clear_plots(self):
        self.stop_animation = True
        try:
            self.animation.event_source.stop()
        except AttributeError:
            pass

        self.run_button.config(state = 'normal')
        self.continue_button.config(state = 'disabled')
        self.animation_speed_dropdown.config(state = 'normal')
        self.ellipse_scale.config(state = 'normal')

        for line in self.orbit_plot.get_lines():
            line.remove()
        for line in self.phase_space_plot.get_lines():
            line.remove()

        self.orbit_plot.set(xlim=(-0.1, 0.1), ylim=(-0.1, 0.1))
        self.phase_space_plot.set(xlim=(-0.1, 0.1), ylim=(-0.1, 0.1))
        self.canvas.draw()
        
#updates lattice parameters from user inputs
    def get_lattice(self):
        self.drift_length = float(self.drift_length_Entry.get())
        self.focal_length = float(self.focal_length_Entry.get())
        self.num_cells = int(self.num_cells_Entry.get())

        #lattice elements are subdivided by quad_steps or drift_steps accordingly. 
        #ie, given a drift_step=5, 1 driftspace of length 10 is subdivided into 5 driftspaces of length 2.
        self.drift_matrix = np.array([[1,(self.drift_length / self.drift_steps)],[0,1]])
        self.fquad_matrix = np.array([[1,0],[(-1/ (self.focal_length * self.quad_steps)),1]])
        self.dquad_matrix = np.array([[1,0],[(1/(self.focal_length * self.quad_steps)),1]])

#update particle initial coniditions from user input
    def get_initial_conditions(self):
        self.x = float(self.xEntry.get())
        self.xp = float(self.xpEntry.get())

        #create a column vector from x and xp
        self.x_and_xp = np.array([[self.x],[self.xp]])
        #store initial conditions in seperate lists. The animations will iterate through these lists
        self.x_values = [self.x_and_xp[0][0]]
        self.xp_values = [self.x_and_xp[1][0]]
        self.s_values = [self.s]

#append current particle parameters to lists
    def append_particle_trajectory(self):
        self.x_values.append(self.x_and_xp[0][0])
        self.xp_values.append(self.x_and_xp[1][0])
        self.s_values.append(self.s)

#propagate particle through one FODO cell and append particle parameter lists after each lattice element, accounting for subdivisions.
    def propagate_particle(self):
        for _ in range(self.quad_steps):
            self.x_and_xp = self.fquad_matrix @ self.x_and_xp
            self.append_particle_trajectory()

        for _ in range(self.drift_steps):
            self.x_and_xp = self.drift_matrix @ self.x_and_xp
            self.s = self.s + (self.drift_length / self.drift_steps)
            self.append_particle_trajectory()

        for _ in range(self.quad_steps):
            self.x_and_xp = self.dquad_matrix @ self.x_and_xp
            self.append_particle_trajectory()

        for _ in range(self.drift_steps):
            self.x_and_xp = self.drift_matrix @ self.x_and_xp
            self.s = self.s + (self.drift_length / self.drift_steps)
            self.append_particle_trajectory()

#update data marker locations based on ellipse_slider value
    def update_ellipse(self, start):
        for line in self.orbit_plot.get_lines():
            self.mark_ellipse(line, int(start))
        for line in self.phase_space_plot.get_lines():
            self.mark_ellipse(line, int(start))
        self.canvas.draw()

#set plot markers at integer cell spacings. Default starting location is 0, entrance of the focusing quad.
    def mark_ellipse(self, line, start=0):
            line.set_markevery((start, 2*(self.drift_steps + self.quad_steps)))
            line.set_marker('o')
            line.set_markerfacecolor('#d9544f')
            line.set_markeredgecolor('#d9544f')

#plots complete data set without animating. Currently unused.
    def final_plots(self):
        self.orbit_line, = self.orbit_plot.plot(self.s_values,self.x_values, linewidth = 0.5, color = 'gray')
        self.phase_space_line, =self.phase_space_plot.plot(self.x_values, self.xp_values, linewidth = 0.5, color = 'gray')

        if self.show_ellipse is True:
            self.mark_ellipse(self.orbit_line, self.ellipse_scale.get())
            self.mark_ellipse(self.phase_space_line, self.ellipse_scale.get())

#plot a small gray point at the particle's initial coniditions
    def plot_initial_conditions(self):
        self.orbit_plot.plot(self.s_values[0],self.x_values[0], linewidth = 0.5, marker='.',color = 'gray')
        self.phase_space_plot.plot(self.x_values[0],self.xp_values[0], linewidth = 0.5, marker='.',color = 'gray')

#disable run button, get user inputs, set s=0, propagate particle, start the animation
    def run_animation(self):
        self.run_button.configure(state='disabled')
        self.run_active = True
        self.s = 0

        self.get_lattice()
        self.get_initial_conditions()
        for cell in range(self.num_cells):
            self.propagate_particle()

        self.animate_orbit()

#used last calculated particle parameters as inputs for next propagation, propagate, start the animation
    def continue_animation(self):
        self.x_values = [self.x_and_xp[0][0]]
        self.xp_values = [self.x_and_xp[1][0]]
        self.s_values = [self.s]
        self.get_lattice()
        for _ in range(self.num_cells):
            self.propagate_particle()

        self.animate_orbit()

#if particle parameters exceed plot limits, update plot limits.
    def set_plot_limits(self):

        orbit_plot_x_min, orbit_plot_x_max, orbit_plot_y_min, orbit_plot_y_max = self.orbit_plot.axis()
        phase_space_plot_x_min, phase_space_plot_x_max, phase_space_plot_y_min, phase_space_plot_y_max = self.phase_space_plot.axis()

        #check if data will exceed current plot limits, adjust plot limits if necessary
        if orbit_plot_x_min > min(self.s_values):
            self.orbit_plot.set_xlim(xmin=min(self.s_values))

        if orbit_plot_x_max < max(self.s_values):
            self.orbit_plot.set_xlim(xmax=max(self.s_values))

        if orbit_plot_y_min > min(self.x_values):
            self.orbit_plot.set_ylim(ymin=min(self.x_values) - 0.5)

        if orbit_plot_y_max < max(self.x_values):
            self.orbit_plot.set_ylim(ymax= max(self.x_values) + 0.5)


        #check if data will exceed current plot limits, adjust plot limits if necessary
        if phase_space_plot_x_min > min(self.x_values):
            self.phase_space_plot.set_xlim(xmin= min(self.x_values)*1.1 - 0.1)

        if phase_space_plot_x_max < max(self.x_values):
            self.phase_space_plot.set_xlim(xmax=max(self.x_values)*1.1 + 0.1)

        if phase_space_plot_y_min > min(self.xp_values):
            self.phase_space_plot.set_ylim(ymin= min(self.xp_values)*1.1 - 0.1)

        if phase_space_plot_y_max < max(self.xp_values):
            self.phase_space_plot.set_ylim(ymax=max(self.xp_values)*1.1 + 0.1)


#init function is called once at the start of the animation
#must return a list of artists redrawn if using blitting
    def init_animation(self):
        self.stop_animation = False
        self.plot_initial_conditions()
        self.set_plot_limits()

        #configure GUI to prevent running another animation before the currrent one finishes
        self.run_button.configure(state='disabled')
        self.continue_button.config(state = 'disabled')
        self.animation_speed_dropdown.configure(state='disabled')
        self.ellipse_scale.config(state = 'disabled')


        #orbit_data and phase_space_data are use to plot data from the current run
        self.orbit_data, = self.orbit_plot.plot([],[], linewidth = 0.5, color = 'gray')
        self.phase_space_data, = self.phase_space_plot.plot([],[], linewidth = 0.5, color = 'gray')


        if self.show_ellipse is True:
            self.mark_ellipse(self.orbit_data, self.ellipse_scale.get())
            self.mark_ellipse(self.phase_space_data, self.ellipse_scale.get())

        return [self.orbit_data, self.phase_space_data]

#called for every frame of the animation function. frame is incremented after each call.
    def animation_frame(self, frame):
        #update plot data for current frame
        self.orbit_data.set_data(self.s_values[:frame], self.x_values[:frame])
        self.phase_space_data.set_data(self.x_values[:frame], self.xp_values[:frame])

        #stop animation if necessary
        if self.stop_animation is True:
            self.animation.event_source.stop()

        if frame == max(range(len(self.s_values))):
            self.run_button.configure(state='normal')
            self.animation_speed_dropdown.configure(state='normal')
            self.ellipse_scale.config(state = 'normal')

            if self.run_active:
                self.continue_button.config(state = 'normal')

        return [self.orbit_data, self.phase_space_data]

#matplotlib built-in animation
    def animate_orbit(self):
        self.animation = animation.FuncAnimation(fig=self.fig,
                                                 func = self.animation_frame,
                                                 frames = range(len(self.s_values) + 1),
                                                 interval = self.animation_speed,
                                                 repeat = False,
                                                 blit=True,
                                                 init_func = self.init_animation)


if __name__ := '__main__':
    window = Tk()
    start = ParticleSimulatorGUI(window)
    window.mainloop()