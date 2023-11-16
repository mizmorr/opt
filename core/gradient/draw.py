import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from logic import grad_desc

def func(x, y):
    return 2 * x * x + 3 * y * y + 4 * x * y - 6 * x - 3 * y

class MainApp(QMainWindow):
    def __init__(self,x1,y1,k1):
        self.x1 = x1
        self.y1 = y1
        self.k1 = k1
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 1100, 900)
        self.setWindowTitle('Градиентный спуск')

        self.canvas = PlotCanvas(self, width=10, height=8)
        self.canvas.move(0, 0)

        self.info_label = QLabel('', self)
        self.info_label.setGeometry(10,800,800,20)

        startButton = QPushButton('Старт', self)
        startButton.clicked.connect(self.startGradientDescent)
        startButton.move(10, 520)

    def startGradientDescent(self):
        for x, y, k, f in grad_desc(func, self.x1, self.y1, self.k1, 10000):
            print(x,y,f,k,sep=' ')
            if(k%100==0):
                self.canvas.plotPoint(x, y, f)
            info_text = f'x:{x:4f}, y:{y:.4f}, f:{f:.4f}, k:{k}'
            self.info_label.setText(info_text)
            plt.ion()#Динамика вертеть
            plt.pause(0.001)#Динамика(пауза потока)


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=10, height=8, dpi=100):
        fig = plt.figure(figsize=(width, height), dpi=dpi)#Доп график.
        #self.Figure = plt.figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111, projection='3d')
        super().__init__(fig)
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
            self.axes.scatter([x], [y], [z], c='r', marker='o')#В ОСНОВНОМ
        self.draw()#ТОРМОЗЯТ

    def clearPlot(self):
        self.axes.clear()
        self.draw()

    def plotFunction(self):
        x = np.linspace(0, 2, 10)
        y = np.linspace(0, 2, 10)
        X, Y = np.meshgrid(x, y)
        Z = func(X, Y)
        self.axes.plot_surface(X, Y, Z, cmap='viridis')


args = []
for i in sys.argv:
    args.append(i)

app = QApplication(sys.argv)
mainApp = MainApp(int(args[1]),int(args[2]),float(args[3])) # 2 2 0.5
mainApp.show()
sys.exit(app.exec_())
