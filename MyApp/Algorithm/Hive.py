import random
import time

from MyApp.Algorithm.Enums import BeeType
from MyApp.Algorithm.Bee import Bee
from MyApp.GUI.Window import Window

from PyQt5.QtWidgets import QApplication

class Hive():
    rand = random.Random()
    rand.seed(0)

    def __init__(self, totalNumberBees, numberInactive, numberActive, numberScout,
                 maxNumberVisits, maxNumberCycles, citiesData):
        self.iter = 0
        self.cycle = 0
        self.totalNumberBees = totalNumberBees
        self.numberInactive = numberInactive
        self.numberActive = numberActive
        self.numberScout = numberScout
        self.maxNumberVisits = maxNumberVisits
        self.maxNumberCycles = maxNumberCycles
        self.probMistake = 0.01
        self.probPersuasion = 0.90
        self.x_cycles = []
        self.y_measure = []
        self.x_iterations = []
        self.y_measureBests = []

        self.citiesData = citiesData

        self.bees = []
        self.bestMemoryMatrix = self.generateRandomMemoryMatrix()
        self.bestMeasureOfQuality = self.measureOfQuality(self.bestMemoryMatrix)
        self.indexesOfInactiveBees = []

        for i in range(totalNumberBees):
            if i < numberInactive:
                currStatus = BeeType.inactive
                self.indexesOfInactiveBees.append(i)
            elif i < numberInactive + numberScout:
                currStatus = BeeType.scout
            else:
                currStatus = BeeType.active

            randomMemoryMatrix = self.generateRandomMemoryMatrix()
            mq = self.measureOfQuality(randomMemoryMatrix)
            numberVisits = 0
            bee = Bee(currStatus, randomMemoryMatrix, mq, numberVisits)
            self.bees.append(bee)
            if self.bees[i].measureOfQuality < self.bestMeasureOfQuality:
                self.bestMemoryMatrix = self.bees[i].memoryMatrix[:]
                self.bestMeasureOfQuality = self.bees[i].measureOfQuality

        self.app = QApplication([])
        self.window = Window()
        self.window.show()

    def generateRandomMemoryMatrix(self):
        result = self.citiesData.cities[:]
        for i in range(1, len(self.citiesData.cities) - 1):
            r = Hive.rand.randint(1, len(self.citiesData.cities) - 2)
            temp = result[r]
            result[r] = result[i]
            result[i] = temp
        return result

    def generateNeighborMemoryMatrix(self, memoryMatrix):
        result = memoryMatrix[:]
        if len(self.citiesData.cities) < 4:
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            print(len(self.citiesData.cities))
            #raise ValueError("Недостаточно городов для генерации случайного индекса.")
        randIndex = Hive.rand.randint(1, len(self.citiesData.cities) - 3)
        if randIndex == len(self.citiesData.cities) - 1:
            adjIndex = 0
        else:
            adjIndex = randIndex + 1

        temp = result[randIndex]
        result[randIndex] = result[adjIndex]
        result[adjIndex] = temp
        return result

    def measureOfQuality(self, memoryMatrix):
        answer = 0
        for i in range(len(self.citiesData.cities) - 1):
            c1 = memoryMatrix[i]
            c2 = memoryMatrix[i + 1]
            d = self.citiesData.Distance(c1, c2)
            answer += d
        return answer

    def start_solving(self):
        # Создание и запуск потока для решения задачи
        from threading import Thread
        self.thread = Thread(target=self.solve)
        self.thread.start()

    def solve(self):
        self.cycle = 0
        while self.cycle < self.maxNumberCycles:
            for i in range(self.totalNumberBees):
                self.iter = self.iter + 1
                self.x_iterations.append(self.getIter())
                if self.bees[i].status == BeeType.active:
                    self.processActiveBee(i)
                elif self.bees[i].status == BeeType.scout:
                    self.processScoutBee(i)
                elif self.bees[i].status == BeeType.inactive:
                    self.processInactiveBee(i)
                self.y_measureBests.append(self.getBesMeasureOfQuality())
                time.sleep(0.001)
                self.window.setPltParams (self.x_iterations, self.y_measureBests)

            self.x_cycles.append(self.cycle)
            self.y_measure.append(self.bestMeasureOfQuality)
            self.cycle += 1
        self.printResults()


    def processActiveBee(self, i):
        neighbor = self.generateNeighborMemoryMatrix(self.bees[i].memoryMatrix)
        neighborQuality = self.measureOfQuality(neighbor)
        prob = Hive.rand.random()
        memoryWasUpdated = False
        numberOfVisitsOverLimit = False

        if neighborQuality < self.bees[i].measureOfQuality:  # better
            if prob < self.probMistake:  # mistake
                self.bees[i].numberOfVisits += 1
                if self.bees[i].numberOfVisits > self.maxNumberVisits:
                    numberOfVisitsOverLimit = True
            else:  # No mistake
                self.bees[i].memoryMatrix = neighbor
                self.bees[i].measureOfQuality = neighborQuality
                self.bees[i].numberOfVisits = 0
                memoryWasUpdated = True
        else:  # Didn't find better neighbor
            if prob < self.probMistake:  # mistake
                self.bees[i].memoryMatrix = neighbor
                self.bees[i].measureOfQuality = neighborQuality
                self.bees[i].numberOfVisits = 0
            else:  # No mistake
                self.bees[i].numberOfVisits += 1
                if self.bees[i].numberOfVisits > self.maxNumberVisits:
                    numberOfVisitsOverLimit = True

        if numberOfVisitsOverLimit:
            self.bees[i].status = BeeType.inactive
            self.bees[i].numberOfVisits = 0
            x = Hive.rand.randint(0, self.numberInactive - 1)
            self.bees[self.indexesOfInactiveBees[x]].status = BeeType.active
            self.indexesOfInactiveBees[x] = i
        elif memoryWasUpdated:
            if self.bees[i].measureOfQuality < self.bestMeasureOfQuality:
                self.bestMemoryMatrix = self.bees[i].memoryMatrix[:]
                self.bestMeasureOfQuality = self.bees[i].measureOfQuality
            self.doWaggleDance(i)
        else:
            return

    def processScoutBee(self, i):
        randomFoodSource = self.generateRandomMemoryMatrix()
        randomFoodSourceQuality = self.measureOfQuality(randomFoodSource)
        if randomFoodSourceQuality < self.bees[i].measureOfQuality:
            self.bees[i].memoryMatrix = randomFoodSource
            self.bees[i].measureOfQuality = randomFoodSourceQuality
            if self.bees[i].measureOfQuality < self.bestMeasureOfQuality:
                self.bestMemoryMatrix = self.bees[i].memoryMatrix[:]
                self.bestMeasureOfQuality = self.bees[i].measureOfQuality
            self.doWaggleDance(i)

    def processInactiveBee(self, i):  # Возможно реализовать случайную мутацию в памяти пчелы
        return

    def doWaggleDance(self, i):
        for j in range(self.numberInactive):
            b = self.indexesOfInactiveBees[j]
            if self.bees[i].measureOfQuality < self.bees[b].measureOfQuality:
                p = Hive.rand.random()
                if self.probPersuasion > p:
                    self.bees[b].memoryMatrix = self.bees[i].memoryMatrix[:]
                    self.bees[b].measureOfQuality = self.bees[i].measureOfQuality

    def getResult(self):
        s = ""
        for i in range(len(self.bestMemoryMatrix) - 1):
            s += str(self.bestMemoryMatrix[i]) + "->"
        s += str(self.bestMemoryMatrix[len(self.bestMemoryMatrix) - 1])
        result = (s, self.bestMeasureOfQuality)
        return result

    def getIter(self):
        return self.iter

    def getBesMeasureOfQuality(self):
        return self.bestMeasureOfQuality

    def printResults(self):
        # Matrix
        print("----------------------------------------------")
        print("Матрица")
        print("Вид матрицы: симметричная")
        print("Размерность: 10x10")

        # Algorithm
        print("----------------------------------------------")
        print("Алгоритм")
        print(f"Активные пчелы: {self.numberActive}")
        print(f"Неактивные пчелы: {self.numberInactive}")
        print(f"Разведчики: {self.numberScout}")
        print(f"Количество циклов: {self.maxNumberCycles}")


        # Results
        print("----------------------------------------------")
        print("Результаты")
        print(f"Длина маршрута: {self.bestMeasureOfQuality}")
        print(f"Путь: {self.getResult()}")

