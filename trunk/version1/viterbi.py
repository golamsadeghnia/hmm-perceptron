import math
import copy
from string import Template
from collections import defaultdict

pi = defaultdict(int)
bp = defaultdict(tuple)

def get_alpha_indices(strings, phi, d):
    positions = []
    for s in strings:
        index = phi.get(s.substitute(d), -1)
        if index == -1:
            return -0.5
        positions.append(phi[s.substitute(d)])
    return copy.deepcopy(positions)

def viterbi(sentence, phi, tags, alpha, strings, strings_abr, mult):
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
                    pi_val = pi.get((k-1,w,u), -0.5)
                    if pi_val == -0.5:
                        continue
                    d = dict(w_i = sentence[k-1], t_2 = w, t_1 = u, t = v)
                    indices = get_alpha_indices(strings, phi, d)
                    if indices == -0.5:
                        continue
                    val = pi_val
                    if mult:
                        for i in indices:
                            val = float(val)*float(alpha[i])                        
                    else:
                        for i in indices:
                            val += alpha[i]
                    if val >= pi[(k,u,v)]:
                        pi[(k,u,v)] = val
                        bp[(k,u,v)] = (w, copy.deepcopy(indices))
    result_tags = []
    result_val = -1
    result_indices = []
    for u in tags:
        for v in tags:
            pi_val = pi.get((len(sentence),u,v), -0.5)
            if pi_val == -0.5:
                continue
            d = dict(t_2 = u, t_1 = v, t = 'STOP')
            indices = get_alpha_indices(strings_abr, phi, d)
            if indices == -0.5:
                continue
            val = pi_val
            if mult:
                for i in indices:
                    val = float(val)*float(alpha[i])
            else:
                for i in indices:
                    val += alpha[i]
            if val > result_val:
                result_tags = [v,u]
                result_val = val
                result_indices = copy.deepcopy(indices)
    for k in range(len(sentence)-2, 0, -1):
        vals = bp[(k+2, result_tags[len(result_tags)-1], result_tags[len(result_tags)-2])]
        result_tags.append(vals[0])
        result_indices += vals[1]
    result_tags.reverse()
    return (copy.deepcopy(result_tags), copy.deepcopy(result_indices))
