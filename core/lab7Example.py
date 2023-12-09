from core.lab7 import Bacteria
from quadratic.optfuncs import *
bacterias = Bacteria(rosenbrock_2, 50, 10, 0.1, 2, 2)
iter_number = 1000
for i in range(iter_number):

    bacterias.chemotaxis(1 / (i + 1))
    bacterias.reproduction()
    bacterias.elimination()

    for bac in bacterias.agents:
        print("X:"+str(bac[0]))
        print("Y:"+str(bac[1]))
        print("Z:"+str(bac[2]))

    b = bacterias.get_best()
    print("bX:" + str(b[0]))
    print("bY:" + str(b[1]))
    print("bZ:" + str(b[2]))

for bac in bacterias.agents:
    print("X:" + str(bac[0]))
    print("Y:" + str(bac[1]))
    print("Z:" + str(bac[2]))

b = bacterias.get_best()
print("bX:" + str(b[0]))
print("bY:" + str(b[1]))
print("bZ:" + str(b[2]))