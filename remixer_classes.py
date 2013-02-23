# Copyright (C) 2013 Julian Metzler
# See the LICENSE file for the full license.

import numpy
import struct
import subprocess
import tempfile
import time
import wave
from remixer_utils import *

SHRT_MIN = -32768
SHRT_MAX = 32767

class Remixer:
	def __init__(self):
		pass
	
	def mix(self, beat, beat_speed, beat_pitch, beat_voice, text, text_speed, text_pitch, text_voice, output_file):
		beatfile = tempfile.NamedTemporaryFile(suffix = ".wav", prefix = "", delete = True)
		textfile = tempfile.NamedTemporaryFile(suffix = ".wav", prefix = "", delete = True)
		outfile = open(output_file, 'wb') if output_file is not None else tempfile.NamedTemporaryFile(suffix = ".wav", prefix = "", delete = True)
		subprocess.call(["espeak", "-w", beatfile.name, "-s", str(beat_speed), "-p", str(beat_pitch), "-v", beat_voice, beat])
		subprocess.call(["espeak", "-w", textfile.name, "-s", str(text_speed), "-p", str(text_pitch), "-v", text_voice, text])
		
		beatwave = wave.open(beatfile, 'rb')
		textwave = wave.open(textfile, 'rb')
		b_params = beatwave.getparams()
		t_params = textwave.getparams()
		b_framecount = b_params[3]
		t_framecount = t_params[3]
		b_frames = beatwave.readframes(b_framecount)
		t_frames = textwave.readframes(t_framecount)
		b_frames, t_frames = make_same_size(strip_seq(list(b_frames), empty = '\x00'), strip_seq(list(t_frames), empty = '\x00'), repeat = True, repeat_truncate = True)
		b_frames = "".join(b_frames)
		t_frames = "".join(t_frames)
		b_frames = b_frames[:-1] if divmod(len(b_frames), 2)[1] != 0 else b_frames
		t_frames = t_frames[:-1] if divmod(len(t_frames), 2)[1] != 0 else t_frames
		beatwave.close()
		textwave.close()
		beatfile.close()
		textfile.close()
		
		b_num = numpy.fromstring(b_frames, numpy.int16)
		t_num = numpy.fromstring(t_frames, numpy.int16)
		b_num_quiet = b_num / 2.0
		mixed_num = self.mix_frames_add(b_num_quiet, t_num)
		mixed_frames = struct.pack('h' * len(mixed_num), *self.normalize_frames(mixed_num))
		
		outwave = wave.open(outfile.name, 'wb')
		outwave.setparams(b_params)
		outwave.writeframes(mixed_frames)
		outwave.close()
		if output_file:
			outfile.close()
		return outfile
	
	def mix_frames_add(self, f1, f2):
		return f1 + f2
	
	def mix_frames_substract(self, f1, f2):
		return f1 - f2
	
	def mix_frames_multiply(self, f1, f2):
		return f1 * f2
	
	def mix_frames_divide(self, f1, f2):
		return f1 / f2
	
	def mix_frames_max(self, f1, f2):
		return [max(*item) for item in zip(f1, f2)]
	
	def mix_frames_min(self, f1, f2):
		return [min(*item) for item in zip(f1, f2)]
	
	def normalize_frames(self, frames, target_min = SHRT_MIN, target_max = SHRT_MAX):
		source_min = min(frames)
		source_max = max(frames)
		normalized_frames = [target_min + ((value - source_min) / (source_max - source_min)) * (target_max - target_min) for value in frames]
		return normalized_frames
	
	def play(self, mixfile):
		return subprocess.call(["aplay", "-q", mixfile.name])
