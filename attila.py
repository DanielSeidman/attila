import classify_edges
import pedigreegraph
import backtrack_search

import sys
sys.setrecursionlimit(10000)


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

  print 'Incorrect pairs:'
  for pair in wrong_pairs:
    truth, result = wrong_pairs[pair]
    print '%s: Truth: %s, Result: %s' % (str(pair), truth, result)

#################
# Runner Logic: #
#################

TRAIN_FILE = '/Users/bodhi/Desktop/train_101.csv'
TEST_FILE = '/Users/bodhi/Desktop/test_101.csv'

## Classify edges
print 'Processing training data'
training_data = classify_edges.process_training_data(TRAIN_FILE)

print 'Processing test data'
nodes, test_data = classify_edges.process_test_data(TEST_FILE)

print 'Build classifiers'
classifiers = classify_edges.build_classifiers(training_data, 0.1)

print 'Classifying edges'
edges = classify_edges.classify_edges(classifiers, test_data)

## Convert the relationships into bitstrings
lookup = {'sibling': '0010', 'None': '0001', 'parent/child': '1100'}
convert = lambda x: lookup[x]
bit_edges = [(pair, map(convert, candidates)) for pair, candidates in edges]


## Build PedigreeGraph
graph = pedigreegraph.PedigreeGraph(nodes)

print 'Total number of edges: %d' % len(bit_edges)
## Run backtracking search
# if __name__ == '__main__':
result = backtrack_search.backtrack_search(graph, bit_edges[0], bit_edges[1:])

## Analyze the result
compute_accuracy(result, TEST_FILE)
