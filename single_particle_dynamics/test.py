import matplotlib.pyplot as plt
import numpy as np

import matplotlib.animation as animation


fig, ax = plt.subplots()
data = np.array([[5,1,2,3,4,5], [0,1,2,3,4,5]])
num_frames = len(data[0])
line, = ax.plot(data[0][0], data[1][0])
ax.set_xlim(-5,5)
ax.set_ylim(-5,6)



def update(frame, data):
    line.set_xdata(data[1][:frame])
    line.set_ydata(data[0][:frame])
    return line,

print(num_frames)
# ani = animation.FuncAnimation(fig=fig, func=update, frames=range(6), fargs = (data,), interval=100, repeat=False)
# plt.show()
