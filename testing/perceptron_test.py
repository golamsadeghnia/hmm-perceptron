import math
import copy
from collections import defaultdict
import viterbi
import sys
from string import Template

words = defaultdict(bool)
phi = defaultdict(int)
alpha = []
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
            words[vals[0]] = True
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

def get_alpha():
    global alpha
    al = open(sys.argv[2], 'r')
    line = al.readline()
    while line:
        l = line.strip()
        alpha.append(int(l))
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
        if not words.get(word, False):
            word = '_RARE_'
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
    global alpha
    global possible_tags
    global strings
    global strings_abr
    get_words()
    get_strings()
    get_alpha()
    get_phi()
    data = open(sys.argv[4], 'r')
    output = open(sys.argv[5], 'w')
    sentence = get_sentence(data)
    while sentence:
        result = viterbi.viterbi(sentence, phi, possible_tags, alpha, strings, strings_abr, 0)
        tags = result[0]
        for i in range(len(sentence)):
            output.write('{} {}\n'.format(sentence[i], tags[i]))
        output.write('\n')
        sentence = get_sentence(data)

evaluate()
