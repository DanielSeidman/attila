from sklearn.neighbors import KernelDensity
from collections import defaultdict

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
