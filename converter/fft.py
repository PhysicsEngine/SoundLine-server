#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import numpy as np 
import math
from collections import Counter

WINSIZE=256
SAMPLING_RATE=44100

def make_hanning(win_size):
	hanning= np.zeros(win_size)
	for i in xrange(win_size):
		hanning[i] = 0.5 - math.cos(2.0*math.pi*i/win_size)
	return hanning

def get_frame(signal, winsize, no):
	shift=winsize/2
	start=no*shift
	end = start+winsize
	return signal[start:end]

def add_signal(signal, frame, winsize, no, dt = 0.25 ):
	shift=winsize/2
	start=no*shift
	end=start+winsize
	signal[start:end] = signal[start:end] + frame

def get_max_freq(freq):
	return np.argmax(abs(freq))

def get_max_spectrums(signal,winsize):
	nf = len(signal)/(winsize/2) - 1
	max_spectrum = []
	hanning = make_hanning(winsize)
	for no in xrange(nf):
		y = get_frame(signal, winsize, no)
		Y = np.fft.fft(y*hanning)
		Y[winsize/2:] = 0
		freq_max = np.argmax(abs(Y))*44100.0/(winsize**2)
		print freq_max
		max_spectrum.append(freq_max)
	return max_spectrum

def get_max_hertz(spectrums):
	data = Counter(spectrums)
	return data.most_common(1)

def get_max_freqs(spectrums,winsize,sampling_rate=44100,dt=0.25):
	result = []
	step = sampling_rate*dt/(winsize/2)
	tmp = []
	for (i,spectrum) in enumerate(spectrums):
		if i % step == 0 and i > 0 :
			result.append(get_max_hertz(tmp))
			tmp = []
		else:
			tmp.append(spectrum)
	return result

def main():
	import saveload
	ary = saveload.load("test.m4a")
	ary = ary.reshape(len(ary)/2,2)[:,0]
	spectrums = get_max_spectrums(ary,256)
	print spectrums

if __name__ == '__main__':
	main()
