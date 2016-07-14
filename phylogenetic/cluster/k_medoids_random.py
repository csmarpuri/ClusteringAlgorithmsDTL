import sys

# Include the upper level directory in the import search path
sys.path.append('../')

import os
from multiprocessing import Pool
import DP
import Greedy
import KMeans
import newickFormatReader
import copy
import ReconGraph
import random

recon_threshold = 100 

# K medioids from random 
# processing 136 files 
# Start time:         2016-07-02:08:19:28
# End time: Mon Jul   4 22:08:06 PDT 2016


def run_test(fileName, max_k):
    cache_dir = './cache'
    D = 2.
    T = 3.
    L = 1.

    print >> sys.stderr, "FILE: ", fileName
    print fileName


    host, paras, phi = newickFormatReader.getInput(fileName)

    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
        f = open('%s/README' % cache_dir, 'w')
        f.write('This directory holds a cache of reconciliation graph for the TreeLife data set')
        f.close()

    cache_location = '%s/%s.graph' % (cache_dir, os.path.split(fileName)[1])
    recon_count_location = '%s/%s.count' % (cache_dir, os.path.split(fileName)[1])
    if not(os.path.isfile(cache_location)) or not(os.path.isfile(recon_count_location)):
        print >> sys.stderr, 'A reconciliation graph has not been built yet for this newick file'
        print >> sys.stderr, 'Doing so now and caching it in {%s}...' % cache_location

        DictGraph, numRecon = DP.DP(host, paras, phi, D, T, L)
        f = open(cache_location, 'w+')
        g = open(recon_count_location, 'w+')
        f.write(repr(DictGraph))
        g.write(str(numRecon))
        f.close()
        g.close()

    print >> sys.stderr, 'Loading reonciliation graph from cache'
    f = open(cache_location)
    g = open(recon_count_location)
    DictGraph = eval(f.read())
    numRecon = float(g.read())
    f.close()
    g.close()

    ## Only consider running algorithm for reconciliations with more than 
    # threshold MPRs
    if (numRecon < recon_threshold):
        print >> sys.stderr, 'Too few reconciliations: ', numRecon
        return 
    else:
        print >> sys.stderr, 'Reconciliation Count: ', numRecon



    scoresList, dictReps = Greedy.Greedy(DictGraph, paras)

    print >> sys.stderr, 'Found cluster representatives using point-collecting'

    graph = ReconGraph.ReconGraph(DictGraph)
    setReps = [ReconGraph.dictRecToSetRec(graph, dictRep) for dictRep in dictReps]
    random.seed(0)
    extra_reps = [KMeans.get_template(graph) for i in xrange(max_k)]

    representatives = setReps + extra_reps

    print >> sys.stderr, 'Starting K Means algorithm ... '
    print >> sys.stderr, 'Printing Average and Maximum cluster radius at each step'

    for seed in xrange(5):
        for i in xrange(1, max_k + 1):
            # print 'k = %d' % i
            # KMeans.k_means(graph, 10, i, 0, representatives[:i])
            KMeans.k_means(graph, 10, i, seed, None)
            print

def doFile(fileName):
    try:
        run_test(fileName, max_k)
    except:
        pass

fileNames = sys.argv[1]
max_k = int(sys.argv[2])
num_processors = 5
if num_processors > 1:
    p = Pool(num_processors)
    p.map(doFile, fileNames.split(','))
else:
    [run_test(fileName, max_k) for fileName in fileNames.split(',')]
