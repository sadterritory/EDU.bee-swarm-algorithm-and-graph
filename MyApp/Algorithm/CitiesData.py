from MyApp.Algorithm.GenerateMatrix import Matrix
from MyApp.Algorithm.Enums import MatrixType


class CitiesData():

    def __init__(self):
        self.N = 10
        self.cities = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.citiesMatrix = Matrix(10, MatrixType.symmetrical, 1, 10)

    # def initializationNEW(self, N, type, a, b):
    #     self.N = N  # количество городов
    #     self.citiesMatrix = Matrix(N, type, a, b)
    #     self.cities = []
    #     for i in range(N):
    #         self.cities.append(i)
    #     self.cities.append(self.cities[0])
    #
    # def initializationOLD(self, path):
    #     dmatrix = self.citiesMatrix.importFromFile(path)
    #     self.N = dmatrix.N
    #     self.citiesMatrix = dmatrix
    #     self.cities = []
    #     for i in range(self.N):
    #         self.cities.append(i)
    #     self.cities.append(self.cities[0])

    # Дистанция между двумя городами
    def Distance(self, firstCity, secondCity):
        return self.citiesMatrix.matrix[firstCity][secondCity]
