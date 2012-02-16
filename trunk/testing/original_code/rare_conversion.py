import sys
from collections import defaultdict

words = defaultdict(bool)

def get_words():
    global possible_tags
    training = open(sys.argv[1], 'r')
    line = training.readline()
    while line:
        l = line.strip()
        if l:
            vals = l.split(' ')
            words[vals[0]] = True
        line = training.readline()

def convert():
    data = open(sys.argv[2], 'r')
    out = open(sys.argv[3], 'w')
    line = data.readline()
    while line:
        l = line.strip()
        if l:
            vals = l.split(' ')
            word = vals[0]
            if not words.get(word, False):
                word = '_RARE_'
            out.write('{} '.format(word))
            for i in range(1,len(vals)-1):
                out.write('{} '.format(vals[i]))
            if not len(vals) == 1:
                out.write('{}'.format(vals[len(vals)-1]))
        out.write('\n')
        line = data.readline()

get_words()
convert()
