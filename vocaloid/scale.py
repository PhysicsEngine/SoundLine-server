# -*- coding: utf-8 -*-
from abc import abstractmethod
from hertz_2_noteNum import CMajorHertz2NoteNum, AMinorHertz2NoteNum

class BaseScale(object):

    def __init__(self, hertz2NoteNum):
        self.hertz2NoteNum = hertz2NoteNum

    def convert(self, hertz):
        return self.hertz2NoteNum.convert(hertz)

    @classmethod
    def calcTick(cls, sec):
        return int(240 * sec)
    
class InocentScale(BaseScale):
    def __init__(self):
        BaseScale.__init__(self, CMajorHertz2NoteNum())
    
class CmajorScale(BaseScale):
    def __init__(self):
        BaseScale.__init__(self, CMajorHertz2NoteNum())
 
class AminorScale(BaseScale):
    def __init__(self):
        BaseScale.__init__(self, AMinorHertz2NoteNum())

if __name__ == "__main__":
    scale = InocentScale()
    print scale.convert(200)
