import time

from core.gradient.optfuncs import rastrigin_2
from core.lab4 import PSO

px = 5.0
py = 5.0
particle_number = 30
fi_p = 3.0
fi_g = 3.0
iter_number = 1000
psa_obj = PSO(rastrigin_2, particle_number, px, py, fi_p, fi_g)
for particle in psa_obj.particles:
    print("X:" + str(particle[0]) + " Y:" + str(particle[1]) + " Z:" + str(particle[2]))

for i in range(iter_number):
    psa_obj.next_iteration()
    print("ITER:"+str(i))
    for particle in psa_obj.particles:
        print("X:" + str(particle[0])+" Y:" + str(particle[1])+" Z:" + str(particle[2]))