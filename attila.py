import classify_edges
import pedigreegraph
import backtrack_search
import numpy as np
from collections import defaultdict

import sys
sys.setrecursionlimit(10000000)

# WARNING: This script is arranged for testing purposes and is not intended for
# a production or research setting.


############################
# Handle train/test files: #
############################

def process_training_data(train_file):
  training_data = defaultdict(lambda: [])

  with open(train_file, 'r') as ifile:
    for line in ifile:
      IID1, IID2, REL_TYPE, IBD1, IBD2 = line.strip().split(',')
      if REL_TYPE in ['parent', 'child']:
        REL_TYPE = 'parent/child'
      training_data[REL_TYPE].append( (float(IBD1), float(IBD2)) )

    for category in training_data:
      training_data[category] = np.array(training_data[category])

  return training_data

def process_test_data(test_file):
  nodes = set()
  test_data = []

  with open(test_file, 'r') as ifile:
    for line in ifile:
      IID1, IID2, REL_TYPE, IBD1, IBD2 = line.strip().split(',')

      nodes.add(IID1)
      nodes.add(IID2)

      test_data.append( ((IID1, IID2), (float(IBD1), float(IBD2))) )

  nodes = list(nodes)
  nodes.sort()

  return nodes, test_data


###################################
# Compute accuracy on the output: #
###################################

def compute_accuracy(graph, test_file):
  truth = {}
  lookup = {'sibling': '0010', 'None': '0001', 'parent': '1000', 'child': '0100'}

  with open(test_file, 'r') as ifile:
    for line in ifile:
      IID1, IID2, REL_TYPE, IBD1, IBD2 = line.strip().split(',')
      if REL_TYPE == 'second':
        REL_TYPE = 'None'
      truth[(IID1, IID2)] = lookup[REL_TYPE]

  wrong_pairs = {}

  for pair in truth:
    if truth[pair] != graph.get(pair):
      wrong_pairs[pair] = (truth[pair], graph.get(pair)) # (truth, result)

  wrong = len(wrong_pairs.keys())
  total = len(truth.keys())
  print 'Total pairs = %d' % total
  print 'Number correct = %d' % (total - wrong)
  print 'Number wrong = %d' % wrong

  if wrong_pairs:
    print 'Incorrect pairs:'
    for pair in wrong_pairs:
      truth, result = wrong_pairs[pair]
      print '%s: Truth: %s, Result: %s' % (str(pair), truth, result)


#################
# Runner Logic: #
#################

if __name__ == '__main__':
  train_file = sys.argv[1]
  test_file = sys.argv[2]

  print 'Processing training data'
  training_data = process_training_data(train_file)
  print 'Processing test data'
  nodes, test_data = process_test_data(test_file)

  print 'Build classifiers'
  classifiers = classify_edges.build_classifiers(training_data, 0.1)

  print 'Classifying edges'
  edges = classify_edges.classify_edges(classifiers, test_data)

  # Convert the relationships into bitstrings
  lookup = {'sibling': '0010', 'None': '0001', 'parent/child': '1100'}
  convert = lambda x: lookup[x]
  bit_edges = [(pair, map(convert, candidates)) for pair, candidates in edges]

  # Build PedigreeGraph
  graph = pedigreegraph.PedigreeGraph(nodes)

  print 'Total number of edges: %d' % len(bit_edges)
  result = backtrack_search.backtrack_search(graph, bit_edges[0], bit_edges[1:])
  compute_accuracy(result, test_file)
