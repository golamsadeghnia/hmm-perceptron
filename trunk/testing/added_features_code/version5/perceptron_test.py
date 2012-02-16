import math
import copy
from collections import defaultdict
import viterbi
import sys
import re
from string import Template

Words = defaultdict(int)
phi = defaultdict(int)
alpha = defaultdict(int)
regExp = defaultdict(str)
possible_tags = []
strings = []
strings_abr = []


def get_words():
    global possible_tags
    training = open(sys.argv[1], 'r')
    line = training.readline()
    while line:
        l = line.strip()
        if l:
            vals = l.split(' ')
            Words[vals[0]] += 1
            not_in = True
            for i in possible_tags:
                if i == vals[1]:
                    not_in = False
            if not_in:
                possible_tags.append(vals[1])
        line = training.readline()

def get_strings():
    global strings
    global strings_abr
    string = Template('w_i=$w_i,t=$t')
    strings.append(copy.deepcopy(string))
    string = Template('t_-2=$t_2,t_-1=$t_1,t=$t')
    strings.append(copy.deepcopy(string))
    strings_abr.append(copy.deepcopy(string))
    string = Template('t_-1=$t_1,t=$t')
    strings.append(copy.deepcopy(string))
    strings_abr.append(copy.deepcopy(string))
    string = Template('t=$t')
    strings.append(copy.deepcopy(string))

def get_regExp():
    firstCaps = re.compile('[A-Z].+')
    AllCaps = re.compile('[A-Z]+$')
    startNumerals = re.compile('\d+')
    allCapsWithDot = re.compile('[A-Z]+\.[A-Z]+$')
    phoneNumber = re.compile('\d\d\d.\d\d\d.\d\d\d\d')
    locationPlace = re.compile('[A-Z][a-z][a-z][a-z][a-z][a-z][a-z]+$')
    regExp[firstCaps] = 'firstCaps'
    regExp[AllCaps] = 'AllCaps'
    regExp[startNumerals] = 'startNumerals'
    regExp[allCapsWithDot] = 'allCapsWithDot'
    regExp[phoneNumber] = 'phoneNumber'
    regExp[locationPlace] = 'locationPlace' 

def get_alpha():
    al = open(sys.argv[2], 'r')
    line = al.readline()
    while line:
        l = line.strip()
        if l:
            vals = l.split(' ')
            alpha[int(vals[0])] = int(vals[1])
        line = al.readline()

def get_sentence(data):
    sentence = []
    line = data.readline()
    l = line.strip()
    if not line:
        return 0
    while l:
        vals = l.split(' ')
        word = vals[0]
        sentence.append(word)
        line = data.readline()
        l = line.strip()
    return copy.deepcopy(sentence)

def get_phi():
    data = open(sys.argv[3], 'r')
    line = data.readline()
    while line:
        l = line.strip()
        vals = l.split(' ')
        phi[vals[0]] = int(vals[1])
        line = data.readline()

def evaluate():
    global possible_tags
    global strings
    global strings_abr
    get_words()
    get_strings()
    get_alpha()
    get_phi()
    get_regExp()
    data = open(sys.argv[4], 'r')
    output = open(sys.argv[5], 'w')
    sentence = get_sentence(data)
    while sentence:
        tags = viterbi.viterbi(sentence, phi, possible_tags, alpha, strings, strings_abr, Words, regExp)
        for i in range(len(sentence)):
            output.write('{0} {1}\n'.format(sentence[i], tags[i]))
        output.write('\n')
        sentence = get_sentence(data)

evaluate()
