#!/usr/local/bin/python
# -*- encoding:utf-8 -*-

import sys
import numpy
import os.path
import time

from converter import saveload
from converter import fft
#from vocaloid import scale
from vocaloid import vsqx_lib
#from vocaloid import net_vocaloid_request_lib

WIN_SIZE = 256
SAMPLING_RATE = 44100

def get_notes(raw_data,scale):
	spectrums = fft.get_max_spectrums(raw_data,WIN_SIZE)
	notes = []
	length = 1
	prev_note = 0
	print spectrums
	for (i,spectrum) in enumerate(spectrums):
		note = scale.convert(spectrum)
		if prev_note == note:
			length = length + 1
		else:
			notes.append((i,length,prev_note))
			length = 1
			prev_note = note
	return notes

def create_note_xml(notes,note_xml_name):
	note_xmls = [] 
	for note in notes:
		note_xmls.append(vsqx_lib.VsqxLib.createNote(note[0],note[1],note[2]))
	notes_xml = VsqxLib.createVsqx(notes)
	f = open(note_xml_name, 'w')
	f.write(notes_xml)
	f.close()

def download_music(note_xml_name,output_name):
	id = NetVocaloidRequestLib.startCreateVocal(note_xml_name)
	while (NetVocaloidRequestLib.isDoneCreateVocal(id) is False):
		print 'createing'
		time.sleep(3)
	NetVocaloidRequestLib.downloadVocalFile(id, output_name)

def main():
	input_name  = sys.argv[1]
	input_path,ext   = os.path.splitext(input_name)
	note_xmlname = input_path + ".xml"
	output_name = sys.argv[2]
#	scale    = scale.InnocentScale()
	raw_data    = saveload.load(input_name)
#	notes = get_notes(raw_data,scale="hoge")
#	xml = create_note_xml(notes,note_xml_name)
#	download_music(note_xml_name,output_name)
	saveload.save(output_name,raw_data)

if __name__ == '__main__':
	main()
