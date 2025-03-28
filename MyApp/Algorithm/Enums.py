import enum


class TaskType(enum.Enum):
    OLD = 0
    NEW = 1


class MatrixType(enum.Enum):
    symmetrical = 1
    asymmetrical = 2


class BeeType(enum.Enum):
    active = 1
    inactive = 2
    scout = 3


class ExperimentType(enum.Enum):
    joint = 1
    beeColony = 2
    antColony = 3
    genetically = 4
