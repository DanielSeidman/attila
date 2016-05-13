import numpy as np
from sklearn.neighbors import KernelDensity
from collections import defaultdict

### Warning: this code is implemented for testing purposes.
### This should not be used in a production/research relese.

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


##############################
# Construct KDE classifiers: #
##############################

def build_classifiers(training_data, bandwidth):
  classifiers = {}
  for category in training_data:
    print 'Classifier category: ' + category
    print 'Number of samples: ' + str(len(training_data[category]))
    kde = KernelDensity(bandwidth=bandwidth)
    classifiers[category] = kde.fit(training_data[category])

  return classifiers


##################################################
# Classify edges and create a sorted edge stack: #
##################################################

NONE_CATEGORIES = ['None', 'second', 'third']

def confidence_vector(classifiers, data):
  confidences = []
  none_scores = []

  for category in classifiers.keys():
    if category in NONE_CATEGORIES:
      none_scores.append(classifiers[category].score_samples(data)[0])
    else:
      confidences.append( (category, classifiers[category].score_samples(data)[0]) )

  # Group classifiers into a single None category
  confidences.append( ('None', max(none_scores)) )

  confidences = sorted(confidences, key=lambda t: t[1])
  confidences.reverse()

  return confidences


def classify_edges(classifiers, test_data):
  import warnings
  warnings.filterwarnings("ignore")

  edges = []

  for pair, data in test_data:
    # Sort classifications here
    confidences = confidence_vector(classifiers, data)
    edges.append((pair, confidences))

  # Globally sort the edges by the highest confidence candidate for the edge
  edges = sorted(edges, key=lambda t: t[1][0][1])
  edges.reverse()

  # Drop confidence information once the edges are sorted
  filtered = []
  for pair, candidates in edges:
    filtered.append((pair, map(lambda t: t[0], candidates)))

  return filtered
