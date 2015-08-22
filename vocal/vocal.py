# -*- coding: utf-8 -*-
import csv

class Vocaloid(object):
    HERTZ_MIN = 8.2
    def __init__(self):
        with open('noteNum_hertz.csv', mode='r') as input_file:
            reader = csv.reader(input_file)
            self.noteNumList = []
            for rows in reader:
                self.noteNumList.append(float(rows[1]))
            
    def hertz2noteNum(self, hertz):
        for k, v in enumerate(self.noteNumList):
            if hertz < self.HERTZ_MIN:
                return '0'

            if hertz > v:
                continue 
            else:
                return str(k)


