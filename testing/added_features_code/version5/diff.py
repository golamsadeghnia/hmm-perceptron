import sys
from collections import defaultdict

words = defaultdict(int)
tags = defaultdict(int)
word_tag = dict(defaultdict(int))
total_errors = 0
total_words = 0

def print_vals():
    global total_errors
    global total_words
    print 'TOTAL NUMBER OF WORDS:'
    print '---------------------- '
    print '{0}'.format(total_words)
    print
    print
    print 'TOTAL NUMBER OF ERRORS:'
    print '---------------------- '
    print '{0}'.format(total_errors)
    print
    print
    print 'INCORRECT LABELS: number of incorrect labelings by the data for each correct label'
    print '---------------- '
    for key,value in sorted(tags.iteritems(), key = lambda (k,v): (-v,k)):
        if len(key) < 8:
            print '{0}\t\t{1}'.format(key, value)
        else:
            print '{0}\t{1}'.format(key, value)
    print
    print
    print 'INCORRECT WORDS: number of incorrect labelings for a given word'
    print '--------------- '
    for key,value in sorted(words.iteritems(), key = lambda (k,v): (-v,k)):
        if len(key) < 8:
            print '{0}\t\t{1}'.format(key, value)
        else:
            print '{0}\t{1}'.format(key, value)
    print
    print
    for tag in word_tag:
        print '{0}: number of labelings that should be labeled {1}'.format(tag,tag)
        print '-----'
        for key,value in sorted(word_tag[tag].iteritems(), key = lambda (k,v): (-v,k)):
            if len(key) < 8:
                print '{0}\t\t{1}'.format(key, value)
            else:
                print '{0}\t{1}'.format(key, value)
        print
        print

def compare():
    global total_errors
    global total_words
    data = open(sys.argv[1], 'r')
    key = open(sys.argv[2], 'r')
    line_data = data.readline()
    line_key = key.readline()
    while line_data:
        l_d = line_data.strip()
        l_k = line_key.strip()
        if l_d:
            total_words += 1
            vals_data = l_d.split(' ')
            vals_key = l_k.split(' ')
            if not vals_data[1] == vals_key[1]:
                total_errors += 1
                words[vals_data[0]] += 1
                tags[vals_key[1]] += 1
                if not word_tag.get(vals_key[1], False):
                    word_tag[vals_key[1]] = defaultdict(int)
                word_tag[vals_key[1]][vals_key[0]] += 1
        line_data = data.readline()
        line_key = key.readline()
    print_vals()

compare()
