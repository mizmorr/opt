# # import sys
# # import numpy as np
# # from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
# # import matplotlib.pyplot as plt
# # from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# # from lab2 import sqMethod
# # from lab3 import GeneticAlg
# # from optfuncs import rosenbrock_2
# # from lab1 import grad_desc


# # class PlotCanvas(FigureCanvas):
# #     def __init__(self, parent=None, width=10, height=8, dpi=100):
# #         fig = plt.figure(figsize=(width, height), dpi=dpi)#Доп график.
# #         self.axes = fig.add_subplot(111, projection='3d')
# #         super().__init__(fig)
# #         self.setParent(parent)
# #         self.plotFunction()
# #         self.last_10_p = []

# #     def plotPoint(self, x, y, z):
# #         self.last_10_p.append((x,y,z))
# #         if len(self.last_10_p)>10:
# #             self.last_10_p.pop(0)
# #         self.clearPlot()#ВСЕ
# #         self.plotFunction()#ЭТИ
# #         for x,y,z in self.last_10_p:#СТРОКИ
# #             self.axes.scatter([x], [y], [z], c='r', marker='o')#В ОСНОВНОМ

# #     def clearPlot(self):
# #         self.axes.clear()

# #     def plotFunction(self):
# #         x = np.linspace(0, 2, 10)
# #         y = np.linspace(0, 2, 10)
# #         X, Y = np.meshgrid(x, y)
# #         Z = rosenbrock_2(X, Y)
# #         self.axes.plot_surface(X, Y, Z, cmap='viridis')

# #     def startGradientDescent(self):
# #         for x, y, k, f in grad_desc(rosenbrock_2, 2, 2, 5, 10000):
# #             print(x,y,f,k,sep=' ')
# #             if(k%100==0):
# #                 self.plotPoint(x, y, f)
# #             plt.ion()#Динамика вертеть
# #             plt.pause(0.001)#Динамика(пауза потока)



# # args = []
# # for i in sys.argv:
# #     args.append(i)

# # mainApp = PlotCanvas()
# # mainApp.startGradientDescent()
# # # mainApp.show()


# # import matplotlib.pyplot as plt
# # import matplotlib.animation
# # import numpy as np

# # fig, ax = plt.subplots()
# # x, y = [],[]
# # sc = ax.scatter(x,y)
# # plt.xlim(0,10)
# # plt.ylim(0,10)

# # def animate(i):
# #     x.append(np.random.rand(1)*10)
# #     y.append(np.random.rand(1)*10)
# #     sc.set_offsets(np.c_[x,y])

# # ani = matplotlib.animation.FuncAnimation(fig, animate,
# #                 frames=2, interval=0, repeat=True)
# # plt.show()

# import matplotlib.pyplot as plt
# import numpy as np
# import time
# plt.ion()
# fig, ax = plt.subplots()
# x, y = [],[]
# sc = ax.scatter(x,y)
# plt.xlim(0,10)
# plt.ylim(0,10)

# # plt.draw()
# for i in range(1000):
#     x.append(np.random.rand(1)*10)
#     y.append(np.random.rand(1)*10)
#     sc.set_offsets(np.c_[x,y])
#     fig.canvas.draw_idle()
#     plt.pause(0.000001)


# plt.waitforbuttonpress()

from optfuncs import *
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation
import pandas as pd
from lab6 import AIS
from matplotlib.widgets import Slider

t = np.arange(0.0, 1.0, 0.001)
s = np.sin(5*np.pi*t)
viewwindow = 0.1

import time
def update_graph(num):
    data = populations[num]
    graph._offsets3d = ([t[0] for t in data], [t[1] for t in data], [t[2] for t in data])
    dot = bests[num]
    # alphas = np.linspace(0.1, 1, 50)
    # graph.set_alpha(alphas)
    best._offsets3d = ([dot[0]],[dot[1]], [dot[2]])
    title.set_text('AIS, population={}'.format(num))
    if num < 10:
        plt.tight_layout()
        time.sleep(0.35)
    # if num>80:
    #     ax.set_zlim(0, 20)
    if num==len(populations)-1:
        ani.event_source.stop()

ais = AIS(rosenbrock_2, num_agents=50, num_clones=5, num_elite=20, num_elite_clones=10,
          x_range=-5, y_range=-5)
iter_number = 10000
populations = list()
bests = list()

for i in range(iter_number):
    ais.evolve(1/(i+1))
    current_p = list()
    for ag in ais.agents:
        current_p.append((ag[0],ag[1],ag[2]))
    populations.append(current_p)
    b = ais.get_best_agent()
    bests.append((b[0],b[1],b[2]))


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

title = ax.set_title('3D Test')
x = np.linspace(0, 2, 10)
y = np.linspace(0, 2, 10)
X, Y = np.meshgrid(x, y)
Z = rosenbrock_2(X, Y)
ax.plot_surface(X, Y, Z, cmap='bone',alpha=0.65)

graph = ax.scatter([], [],[],color = 'red',depthshade=False)
best = ax.scatter([],[],[],color = 'green',s=50,marker='*')

ani = matplotlib.animation.FuncAnimation(fig, update_graph, 1000,
                               interval=100, blit=False)

plt.show()
plt.waitforbuttonpress()
