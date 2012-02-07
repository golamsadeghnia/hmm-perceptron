import math
import copy
from string import Template
from collections import defaultdict

pi = defaultdict(int)
bp = defaultdict(tuple)

def get_alpha_indices(strings, phi, d, Words, regExp, abr):
    positions = []
    for s in strings:
        index = phi.get(s.substitute(d), -1)
        if index == -1:
            continue
        positions.append(index)
    if not abr:
        for i in regExp:
            if i.match(d['w_i']):
                phrase = 'w_i={},t={}'.format(regExp[i],d['t'])
                index = phi.get(phrase, -1)
                if index == -1:
                    continue
                positions.append(index)
        if Words[d['w_i']] < 6:
            phrase = 'w_i=_RARE_,t={}'.format(d['t'])
            index = phi.get(phrase, -1)
            if not index == -1:
                positions.append(index)        
    return copy.deepcopy(positions)

def viterbi(sentence, phi, tags, alpha, strings, strings_abr, Words, regExp):
    pi.clear()
    bp.clear()
    pi[(0, '*', '*')] = 1.0
    for k in range(1,len(sentence)+1):
        t1 = tags
        t2 = tags
        if k == 1:
            t1 = ['*']
            t2 = ['*']
        if k == 2:
            t2 = ['*']
        for u in t1:
            for v in tags:
                for w in t2:
                    pi_val = pi.get((k-1,w,u), 0.5)
                    if pi_val == 0.5:
                        continue
                    d = dict(w_i = sentence[k-1], t_2 = w, t_1 = u, t = v)
                    indices = get_alpha_indices(strings, phi, d, Words, regExp, False)
                    val = pi_val
                    for i in indices:
                        val += alpha[i]
                    test = pi.get((k,u,v), 0.5)
                    if test == 0.5 or val > test:
                        pi[(k,u,v)] = val
                        bp[(k,u,v)] = w
    result_tags = []
    result_val = 0
    got_first = False
    tags2 = tags
    if len(sentence) == 1:
        tags2 = ['*']
    for u in tags2:
        for v in tags:
            pi_val = pi.get((len(sentence),u,v), 0.5)
            if pi_val == 0.5:
                continue
            d = dict(t_2 = u, t_1 = v, t = 'STOP')
            indices = get_alpha_indices(strings_abr, phi, d, Words, regExp, True)
            val = pi_val
            for i in indices:
                val += alpha[i]
            if val > result_val or not got_first:
                got_first = True
                result_tags = [v,u]
                result_val = val
    for k in range(len(sentence)-2, 0, -1):
        t = bp[(k+2, result_tags[len(result_tags)-1], result_tags[len(result_tags)-2])]
        result_tags.append(t)
    result_tags.reverse()
    while result_tags[0] == '*':
        result_tags.reverse()
        result_tags.pop()
        result_tags.reverse()
    return copy.deepcopy(result_tags)
