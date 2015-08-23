#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import numpy as np 
import math

WINSIZE=256

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

def add_signal(signal, frame, winsize, no ):
	shift=winsize/2
	start=no*shift
	end=start+winsize
	signal[start:end] = signal[start:end] + frame

def get_max_spectrums(signal,winsize):
	nf = len(signal)/(winsize/2) - 1
	max_spectrum = []
	hanning = make_hanning(winsize)
	for no in xrange(nf):
		y = get_frame(signal, winsize, no)
		Y = np.fft.fft(y*hanning)
		freq_max = np.argmax(abs(Y))
		max_spectrum.append(freq_max)
	return max_spectrum

#signal = read_signal(wave_array,WINSIZE)
#nf = len(signal)/(WINSIZE/2) - 1
#sig_out=sp.zeros(len(signal),sp.float32)
#window = sp.hanning(WINSIZE)

#for no in xrange(nf):
#    y = get_frame(signal, WINSIZE, no)
#    Y = sp.fft(y*window)
#    # Y = G * Y # 何らかのフィルタ処理
#    y_o = sp.real(sp.ifft(Y))
#    add_signal(sig_out, y_o, WINSIZE, no)

def main():
	import saveload
	ary = saveload.load("test.m4a")
	ary = ary.reshape(len(ary)/2,2)[:,0]
	spectrums = get_max_spectrums(ary,256)
	print spectrums

if __name__ == '__main__':
	main()
