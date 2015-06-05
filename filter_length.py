import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('min_length', type=int)
parser.add_argument('max_length', type=int)
args = parser.parse_args()

line_num = 1
for line in sys.stdin:
	line = line.decode('utf-8').strip()
	words = [word.strip() for word in line.split() if word.split() != '']
	if len(words) >= args.min_length and len(words) <= args.max_length:
		print line.encode('utf-8')
	else:
		print >>sys.stderr, line_num
	line_num += 1
