import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from logic import *

class MainApp(QMainWindow):
    a = b = generations = 0
    def __init__(self,a,b,generations):
        super().__init__()
        self.a = a
        self.b = b
        self.generations = generations
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 1100, 900)
        self.setWindowTitle('Genetic')
        self.canvas = PlotCanvas(self, width=10, height=8)
        self.canvas.move(0, 0)

        self.info_label = QLabel('', self)
        self.info_label.setGeometry(20,800,800,40)

        startButton = QPushButton('Старт', self)
        # startButton.setGeometry(40,100)
        startButton.clicked.connect(self.startGeneticAlgorithm)
        startButton.move(10, 520)

    def startGeneticAlgorithm(self):
        self.genetic_algorithm = GeneticAlg(func=rosenbrock_2, generations=self.generations, min_value=True)
        self.genetic_algorithm.initialize_population(a=self.a, b=self.b)
        for generation in range(self.genetic_algorithm.generations):
            self.genetic_algorithm.choose_candidates()
            self.genetic_algorithm.make_mutations(generation)
            best, _ = self.genetic_algorithm.data_summary()
            x, y, f = best[1][:3]
            info_text = f'Generation: {generation}, x: {x:.4f}, y: {y:.4f}, f: {f:.4f}'
            self.info_label.setText(info_text)
            self.canvas.plotPoint(x, y, f)
            plt.ion()
            plt.pause(0.001)


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=10, height=8, dpi=100):
        # fig = plt.figure(figsize=(width, height), dpi=dpi)#Доп график.
        self.Figure = plt.figure(figsize=(width, height), dpi=dpi)
        self.axes = plt.axes(projection = '3d')
        super().__init__(self.Figure)
        self.setParent(parent)
        self.plotFunction()
        self.last_10_p = []

    def plotPoint(self, x, y, z):
        self.last_10_p.append((x,y,z))
        if len(self.last_10_p)>10:
            self.last_10_p.pop(0)
        self.clearPlot()#ВСЕ
        self.plotFunction()#ЭТИ
        for x,y,z in self.last_10_p:#СТРОКИ
            self.axes.scatter([x], [y], [z], c='magenta', marker='*')#В ОСНОВНОМ
        # self.draw()#ТОРМОЗЯТ
        # self.Figure.close("Figure1")

    def clearPlot(self):
        self.axes.clear()
        self.draw()

    def plotFunction(self):
        x = np.linspace(0, 2, 10)
        y = np.linspace(0, 2, 10)
        X, Y = np.meshgrid(x, y)
        Z = rosenbrock_2(X, Y)
        my_cmap = plt.get_cmap('cool')
        self.axes.plot_surface(X, Y, Z, cmap=my_cmap, edgecolor='white')

args = []
for i in sys.argv:
    args.append(i)

app = QApplication(sys.argv)
mainApp = MainApp(int(args[1]),int(args[2]),int(args[3]))
mainApp.show() # 5 5 100

##mainApp.startGradientDescent(int(args[1]),int(args[2]),float(args[3])) # 2 2 0.5
sys.exit(app.exec_())
