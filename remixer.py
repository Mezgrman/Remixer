#!/usr/bin/env python
# Copyright (C) 2013 Julian Metzler
# See the LICENSE file for the full license.

import argparse
import remixer_classes as classes

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-b', '--beat', default = "Wub!")
	parser.add_argument('-t', '--text', default = "This is the most awesome remix ever created!")
	parser.add_argument('-bs', '--beat-speed', type = int, default = 100)
	parser.add_argument('-ts', '--text-speed', type = int, default = 100)
	parser.add_argument('-bp', '--beat-pitch', type = int, default = 50)
	parser.add_argument('-tp', '--text-pitch', type = int, default = 50)
	parser.add_argument('-bv', '--beat-voice', default = 'en')
	parser.add_argument('-tv', '--text-voice', default = 'en')
	parser.add_argument('-o', '--outfile')
	args = parser.parse_args()
	
	mixer = classes.Remixer()
	remix = mixer.mix(beat = args.beat, beat_speed = args.beat_speed, beat_pitch = args.beat_pitch, beat_voice = args.beat_voice, text = args.text, text_speed = args.text_speed, text_pitch = args.text_pitch, text_voice = args.text_voice, output_file = args.outfile)
	if args.outfile is None:
		mixer.play(remix)
		remix.close()

main()
