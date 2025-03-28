import os

import numpy as np
from MyApp.Algorithm.Enums import MatrixType
from random import random, randint
import datetime
import pickle


class Matrix():
    def __init__(self, N, type, a, b):
        # Размерность
        self.N = N
        self.a = a
        self.b = b
        self.type = type

        if type == MatrixType.symmetrical:
            # Генерируем НОВУЮ симметричную матрицу размера N
            self.matrix = self.generateSimmMatrix()
            # print(self.matrix)
            # self.exportToFile()

        elif type == MatrixType.asymmetrical:
            # Генерируем НОВУЮ асимметричную матрицу размера N
            self.matrix = self.generateAsimmMatrix()

    # Создание рандомной симметричной матрицы заданного размера N
    def generateSimmMatrix(self):
        mat = np.eye(self.N)
        for i in range(self.N):
            for j in range(i + 1, self.N):
                mat[i][j] = mat[j][i] = random() * randint(self.a, self.b)
        return mat

    # Создание рандомной несимметричной матрицы заданного размера N
    def generateAsimmMatrix(self):
        mat = np.eye(self.N)
        for i in range(self.N):
            for j in range(self.N):
                if i != j:
                    mat[i][j] = random() * randint(self.a, self.b)
        return mat

    def __getstate__(self) -> dict:
        state = {}
        state["type"] = self.type
        state["N"] = self.N
        state["a"] = self.a
        state["b"] = self.b
        state["matrix"] = self.matrix
        return state

    def __setstate__(self, state: dict):
        self.type = state["type"]
        self.N = state["N"]
        self.a = state["a"]
        self.b = state["b"]
        self.matrix = state["matrix"]

    # Сериализация матрицы в файл
    def exportToFile(self):
        directory = "matrices"
        if not os.path.exists(directory):
            os.makedirs(directory)
        cdt = datetime.datetime.now()
        current_date = cdt.date()
        current_Htime = cdt.time().hour
        current_Mtime = cdt.time().minute
        if self.type == MatrixType.symmetrical:
            t = "SIMM"
        else:
            t = "ASIM"
        name = t + "_" + str(self.N) + "_" + str(self.a) + "_" + str(self.b) + "_" + str(current_date) + "_" + str(
            current_Htime) + "_" + str(current_Mtime)

        pickle.dump(self, open("matrices/" + name + ".bin", "wb"))
        print("OK!!!!", name)

    # Десериализация матрицы из файла
    def importFromFile(self, path):
        matrix = pickle.load(open(path, "rb"))
        return matrix
