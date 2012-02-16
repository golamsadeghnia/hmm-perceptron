import sys
import re
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
    firstCaps = re.compile('[A-Z].+')
    AllCaps = re.compile('[A-Z]+$')
    startNumerals = re.compile('\d+')
    allCapsWithDot = re.compile('[A-Z]+\.[A-Z]+$')
    phoneNumber = re.compile('\d\d\d.\d\d\d.\d\d\d\d')
    location = re.compile('[A-Z][a-z][a-z][a-z][a-z][a-z][a-z]+$')
    while line:
        l = line.strip()
        if l:
            vals = l.split(' ')
            word = vals[0]
            if not words.get(word, False):
                if AllCaps.match(word):
                    word = "_AllCaps_"
                elif location.match(word):
                    word = "_location_"
                elif allCapsWithDot.match(word):
                    word = "_allCapsWithDot_"
                elif firstCaps.match(word):
                    word = "_firstCaps_"
                elif phoneNumber.match(word):
                    word = "_phoneNumber_"
                elif startNumerals.match(word):
                    word = "_startNumerals_"
                else:
                    word = "_RARE_"
            out.write('{0} '.format(word))
            for i in range(1,len(vals)-1):
                out.write('{0} '.format(vals[i]))
            if not len(vals) == 1:
                out.write('{0}'.format(vals[len(vals)-1]))
        out.write('\n')
        line = data.readline()

get_words()
convert()
