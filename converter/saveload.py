#!/usr/local/bin/python
# -*- encoding:utf-8

import sys
import subprocess as sp
import numpy

def load_mp3(filename):
	command = [ 'ffmpeg',
	'-i', sys.argv[1],
	'-f', 's16le',
	'-acodec', 'pcm_s16le',
	'-ar', '44100', # ouput will have 44100 Hz
	'-ac', '2', # stereo (set to '1' for mono)
	'-']
	pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10**8)
	raw_audio = pipe.proc.stdout.read(128000*6)
	# Reorganize raw_audio as a Numpy array with two-columns (1 per channel)

	audio_array = numpy.fromstring(raw_audio, dtype="int16")
	audio_array = audio_array.reshape(len(audio_array))
	return audio_array

def save_mp3(filename,audio_array):
	pipe2 = sp.Popen([ 'ffmpeg',
	'-y', # (optional) means overwrite the output file if it already exists.
	"-f", 's16le', # means 16bit input
	"-acodec", "pcm_s16le", # means raw 16bit input
	'-ar', "44100", # the input will have 44100 Hz
	'-ac','2', # the input will have 2 channels (stereo)
	'-i', '-', # means that the input will arrive from the pipe
	'-vn', # means "don't expect any video input"
	'-acodec', "libmp3lame", # output audio codec
#	'-b', "3000k", # output bitrate (=quality). Here, 3000kb/second
	filename],
	stdin=sp.PIPE,stdout=sp.PIPE, stderr=sp.PIPE)
	audio_array.astype("int16").tofile(self.proc.stdin)

def main():
	ary = load_mp3(sys.argv[1])
#	ary = ary.reshape((ary.shape[0]*2))
	save_mp3(sys.argv[2],ary)

if __name__ == '__main__':
	main()
