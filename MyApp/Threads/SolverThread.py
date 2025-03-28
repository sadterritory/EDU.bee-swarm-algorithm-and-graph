from PyQt5.QtCore import QThread, pyqtSignal

from MyApp.Algorithm.Enums import BeeType


class SolverThread(QThread):
    update_plot = pyqtSignal(list, list)

    def __init__(self, hive):
        super().__init__()
        self.hive = hive

    def run(self):
        while self.hive.cycle < self.hive.maxNumberCycles:
            for i in range(self.hive.totalNumberBees):
                self.hive.iter += 1
                if self.hive.bees[i].status == BeeType.active:
                    self.hive.processActiveBee(i)
                elif self.hive.bees[i].status == BeeType.scout:
                    self.hive.processScoutBee(i)
                elif self.hive.bees[i].status == BeeType.inactive:
                    self.hive.processInactiveBee(i)

            self.hive.x_iterations.append(self.hive.getIter())
            self.hive.y_measureBests.append(self.hive.getBesMeasureOfQuality())
            self.update_plot.emit(self.hive.x_iterations, self.hive.y_measureBests)

            self.hive.x_cycles.append(self.hive.cycle)
            self.hive.y_measure.append(self.hive.bestMeasureOfQuality)
            self.hive.cycle += 1
