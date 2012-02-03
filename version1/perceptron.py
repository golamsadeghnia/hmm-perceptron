import sys
import math
import copy
from string import Template
from collections import defaultdict
import viterbi
from time import time

phi = defaultdict(int)
words = defaultdict(bool)
alpha = []
alpha_average = []
possible_tags = []
strings = []
strings_abr = []

T_DEFAULT = 10

add_factor = 1
mult_factor = 2.0

def init_phi_alpha(mult):
    global alpha
    global possible_tags
    counts = open(sys.argv[1], 'r')
    line = counts.readline()
    while line:
        l = line.strip()
        if l:
            vals = l.split(' ')
            if vals[1] == 'WORDTAG':
                string = 'w_i={0},t={1}'.format(vals[3], vals[2])
                words[vals[3]] = 1
            elif vals[1] == '3-GRAM':
                string = 't_-2={0},t_-1={1},t={2}'.format(vals[2], vals[3], vals[4])
            elif vals[1] == '2-GRAM':
                string = 't_-1={0},t={1}'.format(vals[2], vals[3])
            elif vals[1] == '1-GRAM':
                string = 't={0}'.format(vals[2])
                possible_tags.append(vals[2])
            phi[string] = len(phi)
        line = counts.readline()
    if mult:
        alpha = [1]*len(phi)
    else:
        alpha = [0]*len(phi)

def read_alpha():
    global alpha
    alpha_vals = open(sys.argv[4], 'r')
    line = alpha_vals.readline()
    i = 0
    while line:
        l = line.strip()
        if l:
            val = int(l)
            alpha[i] = val
        i += 1
        line = alpha_vals.readline()

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

def get_sentence_and_tags(data):
    sentence = []
    tags = []
    line = data.readline()
    l = line.strip()
    if not line:
        return 0
    while l:
        vals = l.split(' ')
        sentence.append(vals[0])
        tags.append(vals[1])
        line = data.readline()
        l = line.strip()
    return (copy.deepcopy(sentence), copy.deepcopy(tags))

def get_indices(sentence, tags):
    global strings
    global strings_abr
    result = []
    for i in range(len(sentence)):
        if i == 0:
            d = dict(w_i = sentence[0], t_2 = '*', t_1 = '*', t = tags[0])
            result += viterbi.get_alpha_indices(strings, phi, d)
        elif i == 1:
            d = dict(w_i = sentence[1], t_2 = '*', t_1 = tags[0], t = tags[1])
            result += viterbi.get_alpha_indices(strings, phi, d)
        else:
            d = dict(w_i = sentence[i], t_2 = tags[i-2], t_1 = tags[i-1], t = tags[i])
            result += viterbi.get_alpha_indices(strings, phi, d)
    if len(sentence) == 1:
        d = dict(t_2 = '*', t_1 = tags[len(tags)-1], t = 'STOP')
    else:
        d = dict(t_2 = tags[len(tags)-2], t_1 = tags[len(tags)-1], t = 'STOP')
    result += viterbi.get_alpha_indices(strings_abr, phi, d)
    return copy.deepcopy(result)

def perceptron(print_alpha = 0, mult = 0, import_alpha = 0):
    global alpha
    global alpha_average
    global possible_tags
    global strings
    global strings_abr
    global add_factor
    global mult_factor
    init_phi_alpha(mult)
    get_strings()
    if import_alpha:
        read_alpha()
    alpha_average = copy.deepcopy(alpha)
    for t in range(T_DEFAULT):
        print '---{0}---'.format(t)
        sys.stdout.flush()
        dont_repeat = True
        data = open(sys.argv[2], 'r')
        vals = get_sentence_and_tags(data)
        j = 0
        while vals:
            sentence = vals[0]
            correct_tags = vals[1]
            result = viterbi.viterbi(sentence, phi, possible_tags, alpha, strings, strings_abr, mult)
            z = result[0]
            indices = result[1]
            if not z == correct_tags:
                dont_repeat = False
                correct_indices = get_indices(sentence, correct_tags)
                if mult:
                    for i in indices:
                        alpha[i] = float(alpha[i])/mult_factor
                    for i in correct_indices:
                        alpha[i] = float(alpha[i])*mult_factor
                else:
                    for i in indices:
                        alpha[i] += -1*add_factor
                    for i in correct_indices:
                        alpha[i] += add_factor
            else:
                j += 1
            for i in range(len(alpha)):
                alpha_average[i] += alpha[i]
            vals = get_sentence_and_tags(data)
        data.close()
        if dont_repeat:
            print 'SUCCESS!!!'
            break
#        print 'number correct: {0}'.format(j)
        if print_alpha:
            write_alpha(t)

def write_alpha(t):
    string = 'outputs_average/alpha_{}.txt'.format(t)
    out = open(string, 'w')
    global alpha_average
    for i in alpha_average:
        out.write('{0}\n'.format(i))

perceptron(1)
