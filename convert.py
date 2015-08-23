#!/usr/local/bin/python
# -*- encoding:utf-8 -*-

import sys
import numpy
import os.path
import time

from converter import saveload
from converter import fft
from vocaloid import scale
from vocaloid import vsqx_lib
from vocaloid import net_vocaloid_request_lib

WIN_SIZE = 1024 
SAMPLING_RATE = 44100

def get_notes(raw_data,scale):
	print "get_notes"
	spectrums = fft.get_max_spectrums(raw_data,WIN_SIZE)
	freqs = fft.get_max_freqs(spectrums,WIN_SIZE)
#	print spectrums
	notes = []
	length = 1 
	prev_note = scale.convert(0)
	pos_tick = 1
	for (i,spectrum) in enumerate(freqs):
		note = scale.convert(spectrum)
		if prev_note == note :
			length = length + 1
		else:
			dur_tick = scale.calcTick(length * 0.25)
			notes.append(vsqx_lib.VsqxLib.createNote(pos_tick,dur_tick,prev_note))
			pos_tick = pos_tick + int(dur_tick)
			length = 1
			prev_note = note
	print len(note),"note length"
	return notes

def create_note_xml(notes,note_xml_name):
	notes_xml = vsqx_lib.VsqxLib.createVsqx(notes)
	f = open(note_xml_name, 'w')
	f.write(notes_xml)
	f.close()

def download_music(note_xml_name,output_name):
	id = net_vocaloid_request_lib.NetVocaloidRequestLib.startCreateVocal(note_xml_name)
	while (net_vocaloid_request_lib.NetVocaloidRequestLib.isDoneCreateVocal(id) is False):
		print 'createing'
		time.sleep(3)
	net_vocaloid_request_lib.NetVocaloidRequestLib.downloadVocalFile(id, output_name)

def main():
	input_name  = sys.argv[1]
	input_path,ext   = os.path.splitext(input_name)
	note_xml_name = input_path + ".xml"
	output_name = sys.argv[2]
	scale_converter = scale.InocentScale()
	if len(sys.argv) > 4:
		if sys.argv[3] == "happy":
			scale_converter = scale.CMajorScale()
		elif sys.argv[3] == "sad":
			scale_converter = scale.AminorScale()
	raw_data    = saveload.load(input_name)
	notes = get_notes(raw_data,scale_converter)
	create_note_xml(notes,note_xml_name)
	download_music(note_xml_name,output_name)
#	saveload.save(output_name,raw_data)

if __name__ == '__main__':
	main()
