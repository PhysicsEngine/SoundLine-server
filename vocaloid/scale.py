# -*- coding: utf-8 -*-
from abc import abstractmethod
from hertz_2_noteNum import Hertz2NoteNumConverter

class BaseScale(object):
    converter = Hertz2NoteNumConverter()

    def __init__(self):
        pass

    @abstractmethod
    def convert(self, hertz):
        pass

    @classmethod
    def calcTick(cls, sec):
        return 960
    
class InocentScale(BaseScale):
    @classmethod
    def convert(cls, hertz):
        return cls.converter.execute(hertz)

class CmajorScale(BaseScale):
    usableNoteNums = []

class AminorScale(BaseScale):
    pass

if __name__ == "__main__":
    scale = InocentScale()
    print scale.convert(200)
