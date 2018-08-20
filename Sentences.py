
# coding: utf-8


from __future__ import print_function

from timeit import default_timer as timer
from collections import defaultdict
import itertools as it
import argparse


def count_len(list_sentences):
    """
    Create a dictionary based on list_sentences, with key   = n and value = set
    of all sentences with n words.

    INPUT:  list_sentences      a list of sentences
    OUTPUT: dict_set_sentences  a dictionary as described above
    """
    dict_set_sentences = defaultdict(set)
    for sentence in list_sentences:
        dict_set_sentences[len(sentence.split())].add(sentence)
    return dict_set_sentences


def to_tuple(set_sentences):
    """
    Change each sentence to tuple of words.

    INPUT:  set_sentences    a set of sentences
    OUTPUT: set_tuples       a set of corresponding tuples
    """
    result = set()
    for s in set_sentences:
        result.add(tuple(s.split()))
    return result


def amam(set_tuples, nwords):
    """
    Given a set of sentences in the form of word tuples, remove all 'duplicate'
    tuples. One tuple is duplicate with another if they contain a same nwords
    subtuple.

    INPUT:  set_tuples  a set of tuples with same length
            nwords      length of subtuple to determine 'duplicativeness'
    OUTPUT: None
    """
    if set_tuples == set():
        return None
    if nwords <= 0:
        x = set_tuples.pop()
        set_tuples.clear()
        set_tuples.add(x)
        return None
    s = set()
    news = set()
    to_remove = set()
    for t in set_tuples:
        for st in it.combinations(t, nwords):
            if st in s:
                to_remove.add(t)
                news.clear()
                break
            news.add(st)
        s.update(news)
        news.clear()
    set_tuples -= to_remove
    return None


def form_subdict(set_tuples, nwords):
    """
    Given a set of tuples, for each tuple, generate subtuple with length
    nwords. Return a dictionary. Each key is a possible subtuple and the
    corresponding value is a list of all original tuples that contain subtuple.
    """
    d = defaultdict(list)
    for t in set_tuples:
        for st in it.combinations(t, nwords):
            d[st].append(t)
    return d


def form_subset(set_tuples, nwords):
    """
    Given a set of tuples, form a set of all possible subtuples with length
    nwords.
    """
    subset = set()
    for tpl in set_tuples:
        subset.update(set(it.combinations(tpl, nwords)))
    return subset


def ambn_new(longer_set, shorter_set, nwords):
    """
    Given a set of longer tuples (longer_set) and a set of shorter tuples
    (shorter_set). Delete all tuples in shorter_set which contains at least one
    nwords-subtuple that also is a subtuple of a sentence of longer_set.
    """
    if shorter_set == set() or nwords <= 0:
        shorter_set.clear()
        return None
    to_remove = set()
    ls = form_subset(longer_set, nwords)
    for tpl in shorter_set:
        for subtpl in it.combinations(tpl, nwords):
            if subtpl in ls:
                to_remove.add(tpl)
                break
    shorter_set -= to_remove
    return None


def ambn_legacy(longer_set, shorter_set, nwords):
    """
    Given a set of longer tuples (longer_set) and a set of shorter tuples
    (shorter_set). Delete all tuples in shorter_set which contains at least one
    nwords-subtuple that also is a subtuple of a sentence of longer_set.
    """
    if shorter_set == set() or nwords <= 0:
        shorter_set.clear()
        return None
    sd = form_subdict(shorter_set, nwords)
    for longer_tuple in longer_set:
        for sub_longer_string in it.combinations(longer_tuple, nwords):
            if sub_longer_string in sd:
                for shorter_tuple in sd[sub_longer_string]:
                    shorter_set.discard(shorter_tuple)
    return None


# Use ambn_new instead of ambn_legacy
ambn = ambn_new


def amb(longer_set, shorter_set, nwords):
    """
    Given a set of longer tuples (longer_set) and a set of shorter tuples
    (shorter_set). Delete all tuples in shorter_set which is a subtuple of a
    sentence of longer_set.
    """
    if shorter_set == set() or nwords <= 0 or longer_set is shorter_set:
        return None
    for longer_tuple in longer_set:
        for sub_longer_tuple in it.combinations(longer_tuple, nwords):
            shorter_set.discard(sub_longer_tuple)
    return None


def remove_dist_1(dict_set_tuple_words):
    """
    Not used.
    Given a dictionary of set of word tuples with key being length of each
    tuple. Filter out distance 1 tuples.
    """
    ls = sorted(dict_set_tuple_words.keys(), reverse=True)
    for l in ls:
        for t in dict_set_tuple_words[l]:
            dict_set_tuple_words[l-1] -= set(it.combinations(t, l-1))
    return None


def remove_dist_n(dict_set_sentences, n, outfile=None):
    """
    Given a dictionary (result of count_len), filter out distance n sentences.
    Write result to outfile if provided. Return number of lines in result.
    """
    nout = 0
    if(n % 2 == 0):
        k = divmod(n, 2)[0]
        j = k-1
    else:
        k = divmod(n-1, 2)[0]
        j = k
    # sk = sorted(dict_set_sentences.keys(), reverse=True)
    max_n_words = max(dict_set_sentences.keys())
    dict_set_tuple_words = defaultdict(set)
    for l in range(max_n_words, max_n_words-n, -1):
        dict_set_tuple_words[l] = to_tuple(dict_set_sentences[l])
    for l in range(max_n_words, 0, -1):
        dict_set_tuple_words[l-n] = to_tuple(dict_set_sentences[l-n])

        ls = dict_set_tuple_words[l]

        if ls != set():
            amam(dict_set_tuple_words[l], l-k)
            amb(ls, dict_set_tuple_words[l-n], l-n)
            amb(ls, dict_set_tuple_words[l-n+1], l-n+1)
            for i in range(1, k):
                ambn(ls, dict_set_tuple_words[l-2*i], l-k-i)
            for i in range(1, j+1):
                ambn(ls, dict_set_tuple_words[l-2*i+1], l-j-i)
            nout += len(dict_set_tuple_words[l])
            if outfile is not None:
                for tw in dict_set_tuple_words[l]:
                    outfile.write(' '.join(tw)+'\n')
        del dict_set_tuple_words[l]
        del dict_set_sentences[l]
    return nout


def main(infile, outfile, distance):
    tic = timer()
    lines = infile.readlines()
    nin = len(lines)

    print(nin, "input lines.")

    if distance == 0:
        lines = set(lines)
        nout = len(lines)
        if outfile is not None:
            for line in lines:
                outfile.write(line)
    else:
        dict_set_tuple_words = count_len(lines)
        nout = remove_dist_n(dict_set_tuple_words, distance, outfile)

    dur = timer() - tic
    print(nout, "output lines.")
    print("Wallclock time: {}seconds\n".format(dur))
    return (nin, nout, dur)


def get_num_lines(file_name):
    with open(file_name, 'r') as F:
        return len(F.readlines())


# parse input arguments
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Solve Big Sentences Problem.')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                        help='input file')
    parser.add_argument('-d', '--dist', nargs='?', type=int, default=0,
                        metavar='K', help='Distance k, default: 0')
    parser.add_argument('-o', '--outfile', nargs='?', metavar='filename',
                        type=argparse.FileType('w'),
                        help=('Output filename. No output file will be '
                              'generated if not provided.'))
    args = parser.parse_args()
    main(args.infile, args.outfile, args.dist)
