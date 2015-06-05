import sys

# Input is meant to be source and detokenized MT output that only needs recased.
# Input is expected to be mostly correctly cased, but with initial words, and
# a few other cases lower- or upper-cased as by truecase.py

for line in sys.stdin:
	line = line.decode('utf-8').strip()
	src, tgt = [[word.strip() for word in sentence.split()] for sentence in line.split('|||')]

	if len(src) > 0:
		n = 0 if src[0] not in ['(', '``', '"', '[', '\'', '-LRB-'] or len(src) == 1 else 1
		src_starts_with_upper = src[n][0].isupper() or True
	else:
		src_starts_with_upper = False

	if src_starts_with_upper:
		if len(tgt) > 0:
			n = 0 if tgt[0] not in ['(', '``', '"', '[', '\'', '-LRB-'] or len(tgt) == 1 else 1
			tgt[n] = tgt[n][0].upper() + tgt[n][1:]

	print u' '.join(tgt).encode('utf-8')
