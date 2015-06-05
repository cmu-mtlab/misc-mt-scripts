import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('charset', type=str)
parser.add_argument('-t', '--threshold', type=float, default=0.75)
args = parser.parse_args()

def is_devanagari(line, threshold):
	exclude_chars = ' !"#$%&\'()*+,-./0123456789:;<=>?@[\]^_`{|}~'
	exclude_count = len([c for c in line if c in exclude_chars])
	devanagari_count =  len([c for c in line if ord(c) >= 2304 and ord(c) <= 2431])
	char_count = len(line) - exclude_count
	devanagari_ratio = 1.0 * devanagari_count / char_count if char_count > 0 else 0.0
	return devanagari_ratio >= threshold

def is_char_latin(c):
	c = ord(c)

	# Basic latin
	if c >= 0x0041 and c <= 0x007A:
		return true

	# Latin-1 Supplement
	if c >= 0x00C0 and c <= 0x0FF:
		return true

	# Latin Extended-A
	if c >= 0x0100 and c <= 0x017F:
		return true

	# Latin Extended-B
	if c >= 0x0180 and c <= 0x024F:
		return true

	# Latin Extended Additional
	if c >= 0x1E00 and c <= 0x1EFF:
		return true

	return False

def is_latin(line, threshold):
	exclude_chars = ' !"#$%&\'()*+,-./0123456789:;<=>?@[\]^_`{|}~'	
	exclude_count = len([c for c in line if c in exclude_chars])
	latin_count = len([c for c in line if is_char_latin(c)])
	char_count = len(line) - exclude_count
	latin_ratio = 1.0 * latin_count / char_count if char_count > 0 else 0.0
	return latin_ratio >= threshold

validation_functions = {'devanagari': is_devanagari, 'latin': is_latin}
if args.charset not in validation_functions:
	print >>sys.stderr, '%s is not a known character set.' % args.charset
	print >>sys.stderr, 'Valid options are:', ', '.join(sorted(validation_functions.keys()))
	sys.exit(1)
else:
	validation_function = validation_functions[args.charset]

line_num = 1
for line in sys.stdin:
	line = line.decode('utf-8').strip()
	if validation_function(line, args.threshold):
		print line.encode('utf-8')
	else:
		print >>sys.stderr, line_num
	line_num += 1
