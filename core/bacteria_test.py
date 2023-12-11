from lab7 import Bacteria
from optfuncs import *
from optfuncs import *
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation
import pandas as pd
matplotlib.rcParams['toolbar'] = 'None'
import time
def update_graph(num):
    data = populations[num]
    graph._offsets3d = ([t[0] for t in data], [t[1] for t in data], [t[2] for t in data])
    dot = bests[num]
    # alphas = np.linspace(0.1, 1, 50)
    # graph.set_alpha(alphas)
    best._offsets3d = ([dot[0]],[dot[1]], [dot[2]])
    title.set_text('Bacteria, population={}'.format(num))
    # if num>80:
    #     ax.set_zlim(0, 20)
    if num==len(populations)-1:
        res = {'x':[], 'y':[], 'z':[]}
        for bac in bacterias.agents:
            res['x'].append(bac[0])
            res['y'].append(bac[1])
            res['z'].append(bac[2])
        dot = bacterias.get_best()
        time.sleep(0.2)

        graph._offsets3d = (res['x'],res['y'],res['z'])
        best._offsets3d = ([dot[0]],[dot[1]], [dot[2]])
        #опциональный зум для интереса
        # ax.axis([dot[0]-0.1,dot[0]+0.1,dot[1]-0.1,dot[1]+0.1,dot[2]-10,dot[2]+200])

        title.set_text('Result - best bacterias')
        ani.event_source.stop()

bacterias = Bacteria(rosenbrock_2, 50, 10, 0.1, 2, 2)
iter_number = 1000
populations = list()
bests = list()
for i in range(iter_number):
    bacterias.chemotaxis(1 / (i + 1))
    bacterias.reproduction()
    bacterias.elimination()
    current_p = list()
    for ag in bacterias.agents:
        current_p.append((ag[0],ag[1],ag[2]))
    populations.append(current_p)
    b = bacterias.get_best()
    bests.append((b[0],b[1],b[2]))



fig = plt.figure(num="Bacteria")
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('X-Axis')
font1 = {'family':'serif','color':'grey','size':16}
title = ax.set_title('3D Test',fontdict=font1)
x = np.linspace(0, 2, 10)
y = np.linspace(0, 2, 10)
X, Y = np.meshgrid(x, y)
Z = rosenbrock_2(X, Y)
ax.plot_surface(X, Y, Z, cmap='bone',alpha=0.65)

graph = ax.scatter([], [],[],color = 'red',depthshade=False,label='regular')
best = ax.scatter([],[],[],color = 'green',s=50,marker='*',label='best')
plt.legend(loc="lower right")

ani = matplotlib.animation.FuncAnimation(fig, update_graph, iter_number,
                               interval=0.5, blit=False)

plt.show()
plt.waitforbuttonpress()


# iter_number = 1000
# for i in range(iter_number):
#     print(i)
#     bacterias.chemotaxis(1 / (i + 1))
#     bacterias.reproduction()
#     bacterias.elimination()

#     # for bac in bacterias.agents:
#     #     print("X:"+str(bac[0]))
#     #     print("Y:"+str(bac[1]))
#     #     print("Z:"+str(bac[2]))
#     b = bacterias.get_best()
    # print("bX:" + str(b[0]))
    # print("bY:" + str(b[1]))
    # print("bZ:" + str(b[2]))

# for bac in bacterias.agents:
#     print("X:" + str(bac[0]))
#     print("Y:" + str(bac[1]))
#     print("Z:" + str(bac[2]))

# b = bacterias.get_best()
# print("bX:" + str(b[0]))
# print("bY:" + str(b[1]))
# print("bZ:" + str(b[2]))
