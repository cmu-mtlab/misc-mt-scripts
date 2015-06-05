import sys
import argparse

parser = argparse.ArgumentParser('Reads fully cased corpus on stdin. Writes truecased corpus to stdout')
parser.add_argument('-l', '--default-lower', action='store_true', help='Lowercase words that were only ever seen at the beginning of a sentence. Probably a good idea in German, but not in English.')
parser.add_argument('-m', '--moar', action='store_true', help='Truecase words after punctuation as well as at the beginning of lines')
parser.add_argument('-g', '--german', action='store_true', help='Adds a few special rules for German words that are actually ambiguous')
parser.add_argument('model', help='a truecaser model, as produced by build_truecase_model.py')
args = parser.parse_args()

def load_model(filename):
	model = {}
	with open(filename) as f:
		for line in f:
			line = line.decode('utf-8').strip()
			model[line.lower()] = line
	return model

def recase_word(word, model, start):
	if args.german and not start:
		if word in ['ehe', 'Ehe' 'sie', 'Sie']:
			return word
		if word.startswith('ihr') or word.startswith('Ihr'):
			return word

	if word.lower() in model:
		return model[word.lower()]
	else:
		return word.lower() if args.default_lower else word

model = load_model(args.model)

line_num = 1
print >>sys.stderr, 'Truecasing corpus...'
for line in sys.stdin:
	line = line.decode('utf-8').strip()
	words = line.split()
	if len(words) == 0:
		print
		continue

	# Skip opening punctuation
	n = 0 if words[0] not in ['(', '``', '"', '[', '\'', '-LRB-'] or len(words) == 1 else 1
	first_word = words[n]
	words[n] = recase_word(first_word, model, True)

	if args.moar:
		for i in range(1, len(words)):
				if words[i - 1] in ['.', ',', ':', '"', '(', '\'', '``', '[', '-LRB-', '|']:
					words[i] = recase_word(words[i], model, False)

	print ' '.join(words).encode('utf-8')
	if line_num % 10000 == 0:
		sys.stderr.write('.')
	if line_num % 200000 == 0:
		sys.stderr.write(' %d\n' % line_num)
	line_num += 1
sys.stderr.write('\n')
