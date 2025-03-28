from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("Graph")
        self.setGeometry(500, 200, 1000, 600)

        # Создание графика Matplotlib
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        # Расположение графика в окне PyQt
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)


    def setPltParams(self, Xs, Ys):
        if hasattr(self, 'line'):
            self.line.set_xdata(Xs)
            self.line.set_ydata(Ys)
        else:
            # Если графика еще нет, создаем его
            self.line, = self.ax.plot(Xs, Ys)
        self.ax.set_xlabel('Итерации')
        self.ax.set_ylabel('Длина пути')
        self.ax.set_title('Длина пути vs Итерации')
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()  # Обновляем график на канвасе



