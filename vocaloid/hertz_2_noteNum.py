# -*- coding: utf-8 -*-
import csv
import os

class BaseHertz2NoteNum(object):
    HERTZ_MIN = 8.2
    CUR_DIR = os.path.abspath(os.path.dirname(__file__))

    def __init__(self, csvFile):
        with open(csvFile, mode='r') as inputFile:
            reader = csv.reader(inputFile)
            self.hertzNoteNumMapList = []
            for rows in reader:
                self.hertzNoteNumMapList.append({rows[1]: float(rows[2])})

    def convert(self, hertz):
        for hertzNoteNumMap in self.hertzNoteNumMapList:
            if hertz < self.HERTZ_MIN:
                return '0'

            if hertz > hertzNoteNumMap.values()[0]:
                continue 
            else:
                return hertzNoteNumMap.keys()[0]

        ## for max
        return self.hertzNoteNumMapList[-1].keys()[0]

class CMajorHertz2NoteNum(BaseHertz2NoteNum):
    def __init__(self):
        BaseHertz2NoteNum.__init__(self, '{0}/{1}'.format(self.CUR_DIR, 'midi_note_cmajor.csv'))

class AMinorHertz2NoteNum(BaseHertz2NoteNum):
    def __init__(self):
        BaseHertz2NoteNum.__init__(self, '{0}/{1}'.format(self.CUR_DIR, 'midi_note_aminor.csv'))

