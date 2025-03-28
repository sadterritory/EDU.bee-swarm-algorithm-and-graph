from MyApp.Algorithm.Hive import Hive
from MyApp.Algorithm.CitiesData import CitiesData

import sys

def application():

    testCity = CitiesData()
    test = Hive(20, 2, 13, 5, 3, 80, testCity)
    test.start_solving()
    sys.exit(test.app.exec_())

if __name__ == "__main__":
    application()
