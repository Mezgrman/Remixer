# Copyright (C) 2013 Julian Metzler
# See the LICENSE file for the full license.

def make_same_size(seq1, seq2, filler = None, truncate = False, repeat = False, repeat_truncate = False):
	len1 = len(seq1)
	len2 = len(seq2)
	if len1 == len2:
		new_seq1 = seq1
		new_seq2 = seq2
	elif len1 < len2:
		if truncate:
			new_seq1 = seq1
			new_seq2 = seq2[:len1]
		else:
			if repeat:
				rep, fill = divmod((len2 - len1), len1)
				if repeat_truncate:
					new_seq1 = seq1 + seq1 * rep + seq1[:fill]
				else:
					new_seq1 = seq1 + seq1 * rep + [filler] * fill
				new_seq2 = seq2
			else:
				new_seq1 = seq1 + [filler] * (len2 - len1)
				new_seq2 = seq2
	elif len1 > len2:
		if truncate:
			new_seq1 = seq1[:len2]
			new_seq2 = seq2
		else:
			if repeat:
				rep, fill = divmod((len1 - len2), len2)
				new_seq1 = seq1
				if repeat_truncate:
					new_seq2 = seq2 + seq2 * rep + seq2[:fill]
				else:
					new_seq2 = seq2 + seq2 * rep + [filler] * fill
			else:
				new_seq1 = seq1
				new_seq2 = seq2 + [filler] * (len1 - len2)
	return new_seq1, new_seq2

def strip_seq(seq, empty = None):
	start = 0
	end = 0
	for i in range(len(seq)):
		item = seq[i]
		if empty is not None:
			if item != empty:
				start = i
				break
		else:
			if item:
				start = i
				break
	rseq = seq[:]
	rseq.reverse()
	for i in range(len(rseq)):
		item = rseq[i]
		if empty is not None:
			if item != empty:
				end = len(seq) - i
				break
		else:
			if item:
				end = len(seq) - i
				break
	stripped_seq = seq[start:end]
	return stripped_seq
