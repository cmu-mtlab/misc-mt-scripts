import sys
import argparse
from collections import defaultdict, Counter

parser = argparse.ArgumentParser('Takes a monolingual corpus on stdin and builds a truecaser model, which is printed to stdout')
args = parser.parse_args()

tokens = defaultdict(lambda: Counter())
print >>sys.stderr, 'Estimating model..'
# build recasing model from all the words in the corpus
# except the first word of each line
line_num = 1
for line in sys.stdin:
	line = line.decode('utf-8').strip()
	words = line.split()
	if len(words) == 0:
		continue
	# Skip opening punctuation      
	n = 0 if words[0] not in ['(', '``', '"', '[', '\'', '-LRB-'] else 1
	for word in words[n + 1:]:
		tokens[word.lower()][word] += 1
	if line_num % 10000 == 0:
		sys.stderr.write('.')
	if line_num % 200000 == 0:
		sys.stderr.write(' %d\n' % line_num)
	line_num += 1
sys.stderr.write('\n')

for key, counter in tokens.iteritems():
	best_casing, count = counter.most_common(1)[0]
	print best_casing.encode('utf-8')
