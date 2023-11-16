import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from optfuncs import *
from logic import sqMethod

def func(num):
    if num == 0:
        return rosenbrock_2
    elif num == 1:
        return himmelblau_2
    elif num == 2:
        return hypersphere_2
    else:
        return rastrigin_2

class MainApp(QMainWindow):
    x1 = y1 = num = 0
    def __init__(self,x1,y1,num):
        super().__init__()
        self.x1 = x1
        self.y1 = y1
        self.num = num
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 1100, 900)
        self.setWindowTitle('Квадрат')
        self.canvas = PlotCanvas(self, width=10, height=8,num=self.num)
        self.canvas.move(0, 0)
        self.info_label = QLabel(f'x1 = {self.x1}, y1 = {self.y1} ', self)
        self.info_label.setGeometry(20,800,800,40)
        startButton = QPushButton('Старт', self)
        startButton.clicked.connect(self.start)
        startButton.resize(150,50)
        startButton.move(940, 840)
    def start(self):
        res_x = self.x1
        res_y = self.y1
        x_cs = []
        y_cs = []
        z_cs = []
        for i, point in sqMethod(res_x, res_y,self.num):
            x_cs.append(point[0])
            y_cs.append(point[1])
            z_cs.append(point[2])
        for i in range(len(x_cs)):
            if i < (len(x_cs) - 1):
                self.canvas.plotPoint(x_cs[i - 1], y_cs[i - 1], z_cs[i - 1],"black")
            else:
                self.canvas.plotPoint(x_cs[i - 1], y_cs[i - 1], z_cs[i - 1],"red")
            plt.ion()#Динамика вертеть
            plt.pause(0.001)#Динамика(пауза потока)


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=10, height=8, dpi=100,num=4):
        fig = plt.figure(figsize=(width, height), dpi=dpi)#Доп график.
        self.axes = fig.add_subplot(111, projection='3d')
        super().__init__(fig)
        self.setParent(parent)
        self.num = num
        self.plotFunction()
        self.last_10_p = []

    def plotPoint(self, x, y, z,color):
        self.last_10_p.append((x,y,z))
        if len(self.last_10_p)>10:
            self.last_10_p.pop(0)
        self.clearPlot()#ВСЕ
        self.plotFunction()#ЭТИ
        for x,y,z in self.last_10_p:#СТРОКИ
            self.axes.scatter([x], [y], [z], c=color, marker='*')#В ОСНОВНОМ
        self.draw()#ТОРМОЗЯТ

    def clearPlot(self):
        self.axes.clear()
        self.draw()

    def plotFunction(self):
        x = np.linspace(0, 2, 10)
        y = np.linspace(0, 2, 10)
        X, Y = np.meshgrid(x, y)
        Z = himmelblau_2(X,Y)
        # if  self.num == 0:
        #     Z = rosenbrock_2(X,Y)
        # elif self.num == 1:
        #     Z = himmelblau_2(X,Y)
        # elif self.num == 2:
        #     Z = hypersphere_2(X,Y)
        # else:
        #     Z = rastrigin_2(X,Y)
        my_cmap = plt.get_cmap('cool')
        self.axes.plot_surface(X, Y, Z, cmap=my_cmap, edgecolor='none')

args = []
for i in sys.argv:
    args.append(i)

app = QApplication(sys.argv)
mainApp = MainApp(int(args[1]),int(args[2]),float(args[3])) # x1 y1 func_num // example 2 2 1
mainApp.show()
sys.exit(app.exec_())
