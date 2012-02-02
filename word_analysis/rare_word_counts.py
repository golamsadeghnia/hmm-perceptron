import sys
from collections import defaultdict

max_rare_word_count = 5

words = defaultdict(int)
rare_words = defaultdict(bool)
result = dict(defaultdict(int))

def get_counts():
    global max_rare_word_count
    data = open(sys.argv[1], 'r')
    line = data.readline()
    while line:
        l = line.strip()
        if l:
            vals = l.split(' ')
            words[vals[0]] += 1
        line = data.readline()
    for key,value in sorted(words.iteritems(), key = lambda (k,v): (-v,k)):
        if value > max_rare_word_count:
            continue
        rare_words[key] = True
    data.close()

def execute():
    get_counts()
    data = open(sys.argv[1])
    line = data.readline()
    while line:
        l = line.strip()
        if l:
            vals = l.split(' ')
            if rare_words.get(vals[0], False): 
                if not result.get(vals[1], False):
                    result[vals[1]] = defaultdict(int)
                result[vals[1]][vals[0]] += 1
        line = data.readline()
    for i in result:
        print 'TAG = {}:'.format(i)
        print '-----------'
        for key,value in sorted(result[i].iteritems(), key = lambda (k,v): (-v,k)):
            if len(key) < 8:
                print '{}\t\t{}'.format(key,value)
            else:
                print '{}\t{}'.format(key,value)
        print
        print '******************************************************************'
        print '******************************************************************'
        print '******************************************************************'
        print

execute()
