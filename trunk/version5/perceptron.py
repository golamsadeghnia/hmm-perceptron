import sys
import math
import copy
import re
from string import Template
from collections import defaultdict
from viterbi import viterbi
from time import time


Words = defaultdict(int)
phi = defaultdict(int)
alpha = defaultdict(int)
alpha_average = defaultdict(tuple) #(total sum, example number of last update, value of last update)
possible_tags = []
strings = []
strings_abr = []
regExp = defaultdict(str)

T_DEFAULT = 100
add_factor = 1

def get_tags():
    global possible_tags
    tags = defaultdict(bool)
    data = open(sys.argv[1], 'r')
    line = data.readline()
    while line:
        l = line.strip()
        if l:
            vals = l.split(' ')
            tags[vals[1]]
            Words[vals[0]] += 1
        line = data.readline()
    for t in tags:
        possible_tags.append(t)
    data.close()

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

def get_alpha_indices(strings, d, examp_num):
    positions = []
    for s in strings:
        index = phi.get(s.substitute(d), -1)
        if index == -1:
            index = len(phi)
            phi[s.substitute(d)] = index
            alpha[index]
            alpha_average[index] = (0, examp_num, 0)
        positions.append(index)
    return copy.deepcopy(positions)

def get_indices(sentence, tags, examp_num):
    global strings
    global strings_abr
    result = []
    for i in range(len(sentence)):
##########Strings, trigram model############
        if i == 0:
            d = dict(w_i = sentence[0], t_2 = '*', t_1 = '*', t = tags[0])
            result += get_alpha_indices(strings, d, examp_num)
        elif i == 1:
            d = dict(w_i = sentence[1], t_2 = '*', t_1 = tags[0], t = tags[1])
            result += get_alpha_indices(strings, d, examp_num)
        else:
            d = dict(w_i = sentence[i], t_2 = tags[i-2], t_1 = tags[i-1], t = tags[i])
            result += get_alpha_indices(strings, d, examp_num)
##############regular Expressions############
        for j in regExp:
            if j.match(sentence[i]):
                phrase = 'w_i={},t={}'.format(regExp[j],tags[i])
                index = phi.get(phrase, -1)
                if index == -1:
                    index = len(phi)
                    phi[phrase] = index
                    alpha[index]
                    alpha_average[index] = (0, examp_num, 0)
                result.append(index)
        if Words[sentence[i]] < 6:
            phrase = 'w_i=_RARE_,t={}'.format(tags[i])
            index = phi.get(phrase, -1)
            if index == -1:
                index = len(phi)
                phi[phrase] = index
                alpha[index]
                alpha_average[index] = (0, examp_num, 0)
            result.append(index)            
    if len(sentence) == 1:
        d = dict(t_2 = '*', t_1 = tags[len(tags)-1], t = 'STOP')
    else:
        d = dict(t_2 = tags[len(tags)-2], t_1 = tags[len(tags)-1], t = 'STOP')
    result += get_alpha_indices(strings_abr, d, examp_num)
    return copy.deepcopy(result)

def get_phi():
    data = open(sys.argv[1], 'r')
    vals = get_sentence_and_tags(data)
    while vals:
        get_indices(vals[0], vals[1], 1)
        vals = get_sentence_and_tags(data)
    data.close()

def perceptron(print_alpha = 0):
    global possible_tags
    global strings
    global strings_abr
    global add_factor
    get_regExp()
    get_strings()
    get_tags()
    get_phi()
    for t in range(T_DEFAULT):
        print '---{0}---'.format(t)
        sys.stdout.flush()
        dont_repeat = True
        data = open(sys.argv[1], 'r')
        vals = get_sentence_and_tags(data)
        j = 0
        examp_num = 0
        while vals:
            examp_num += 1
            sentence = vals[0]
            correct_tags = vals[1]
            tags = viterbi(sentence, phi, possible_tags, alpha, strings, strings_abr, Words, regExp)
            indices = get_indices(sentence, tags, examp_num)
            correct_indices = get_indices(sentence, correct_tags, examp_num)
            if not tags == correct_tags:
                dont_repeat = False
                for i in indices:
                    alpha[i] += -1*add_factor
                for i in correct_indices:
                    alpha[i] += add_factor
            else:
                j += 1
            for i in set(indices) | set(correct_indices):
                val1 = alpha_average[i][0]+(examp_num - alpha_average[i][1])*alpha_average[i][2]
                val2 = examp_num
                val3 = alpha[i]
                alpha_average[i] = (val1,val2,val3)
            vals = get_sentence_and_tags(data)
        data.close()
        if dont_repeat:
            print 'SUCCESS!!!'
            break
        print 'number correct: {0}'.format(j)
        for i in alpha:
            val1 = alpha_average[i][0]+(examp_num+1 - alpha_average[i][1])*alpha_average[i][2]
            val2 = 1
            val3 = alpha[i]
            alpha_average[i] = (val1,val2,val3)
        if print_alpha:
            write_alpha(t)

def write_alpha(t):
    global alpha_average
    string = 'outputs/alpha_{}.txt'.format(t)
    out = open(string, 'w')
    for i in alpha_average:
        out.write('{} {}\n'.format(i, alpha_average[i][0]))
    out.close()
    string = 'outputs/phi_dictionary_{}.txt'.format(t)
    out = open(string, 'w')
    for i in phi:
        out.write('{} {}\n'.format(i, phi[i]))
    out.close()

perceptron(1)
