from lab8 import *
from optfuncs import *
from matplotlib import pyplot as plt
import matplotlib.animation
matplotlib.rcParams['toolbar'] = 'None'

iterations=[]
def callback_func(epoch, iter_data):
    for iteration_data in iter_data:
        cur_list = []
        for x, y, z in iteration_data:
            cur_list.append((x,y,z))
        iterations.append(cur_list)

def update_graph(num):
    data = iterations[num]
    graph._offsets3d = ([t[0] for t in data], [t[1] for t in data], [t[2] for t in data])
    title.set_text('Hybrid, population={}'.format(num))
    if num==len(iterations)-1:
        #строку ниже можно закомменитить
        graph._offsets3d = ([], [], [])
        best._offsets3d = ([result[0]],[result[1]], [result[2]])
        title.set_text('Result - best dot')
        ani.event_source.stop()

hybrid_algo = HybridAlgorithm(
    func=hypersphere_2,
    population=20,
    position_x=5,
    position_y=5,
    fi_p=3.0,
    fi_g=2.0,
    target_fitness=0.000001,
    pso_to_ais_ratio=0.3,
    num_agents=10,
    num_clones=5,
    num_elite=2,
    num_elite_clones=3,
    x_range=5,
    y_range=5,
    mutation_coefficient=0.1,
    callback_func=callback_func
)


fig = plt.figure(num="Hybrid")
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('X-Axis')
font1 = {'family':'serif','color':'grey','size':16}
title = ax.set_title('3D Test',fontdict=font1)
x = np.linspace(-2, 2, 10)
y = np.linspace(-2, 2, 10)
X, Y = np.meshgrid(x, y)
Z = hypersphere_2(X, Y)
ax.plot_surface(X, Y, Z, cmap='bone',alpha=0.55)
graph = ax.scatter([], [],[],color ='red',depthshade=False,label='dots',s=50,alpha=0.25)
best = ax.scatter([],[],[],color = 'green',s=50,marker='D',label='best')

result = hybrid_algo.run(10000)
plt.legend(loc="lower right")
ani = matplotlib.animation.FuncAnimation(fig, update_graph, len(iterations),
                               interval=500, blit=False)
plt.show()
plt.waitforbuttonpress()

