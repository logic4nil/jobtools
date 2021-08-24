# -*- coding: utf-8 -*-
from enum import Enum, auto

class Status(Enum):
    INIT = auto()
    RUNNING = auto()
    FINISH = auto()
    ERROR = auto()

class ProjectEnum(Enum):
    @classmethod
    def from_str(cls, label):
        if label.upper() in dir(cls):
            return cls[label.upper()]
        else:
            raise NotImplementedError

class EnvScope(ProjectEnum):
    PRIVATE = auto()
    PUBLIC = auto()

class Exts(ProjectEnum):
    JSON = auto()
    TXT = auto()

if __name__ == '__main__':

    print(Exts.from_str("json"))
    # print("test" in Exts)
    # print(type(Exts["json".upper()]))
    pass

