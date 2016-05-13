import edges
import itertools
from edges import _naivePairOrderTest

# ############ #
# Triple Union #
# ############ #

# Take the union of two triples
def union(a, b):
  assert len(a) == len(b)

  result = []
  for i in range(len(a)):
    result.append(edges.union(a[i], b[i]))

  return tuple(result)


#####################
# Triple Generation #
#####################

# Generate all triples off of a given pair of nodes, with the option to exclude a triple.
def build_generator(nodes, orderTest=_naivePairOrderTest):
  # Nodes should be in sorted order.
  def generator(a, b, c=''): # Use c to exclude a triple from the returned list
    assert orderTest(a, b)

    triples = []
    for n in nodes:
      if n != a and n != b and n != c:
        if orderTest(b, n):
          triple = (a, b, n)
        elif orderTest(n, a):
          triple = (n, a, b)
        else:
          triple = (a, n, b)
        triples.append(triple)

    return triples

  return generator


########################
# Triple Decomposition #
########################

# Return the three pairs composing the triple in order AB, AC, BC each with the excluded node.
def decompose_triple(triple):
  AB = ((triple[0], triple[1]), triple[2])
  AC = ((triple[0], triple[2]), triple[1])
  BC = ((triple[1], triple[2]), triple[0])

  return AB, AC, BC


####################
# Triple Reduction #
####################

# These are the base cases for all triple reductions. Edges are ordered AB, AC, BC.
SINGLETON_TRIPLE_REDUCTIONS = {
  ('1000', '1000', '1000'): ('0000', '0000', '0000'),
  ('1000', '1000', '0100'): ('0000', '0000', '0000'),
  ('1000', '1000', '0010'): ('1000', '1000', '0010'),
  ('1000', '1000', '0001'): ('1000', '1000', '0001'),
  ('1000', '0100', '1000'): ('0000', '0000', '0000'),
  ('1000', '0100', '0100'): ('0000', '0000', '0000'),
  ('1000', '0100', '0010'): ('0000', '0000', '0000'),
  ('1000', '0100', '0001'): ('1000', '0100', '0001'),
  ('1000', '0010', '1000'): ('0000', '0000', '0000'),
  ('1000', '0010', '0100'): ('0000', '0000', '0000'),
  ('1000', '0010', '0010'): ('0000', '0000', '0000'),
  ('1000', '0010', '0001'): ('1000', '0010', '0001'),
  ('1000', '0001', '1000'): ('1000', '0001', '1000'),
  ('1000', '0001', '0100'): ('1000', '0001', '0100'),
  ('1000', '0001', '0010'): ('0000', '0000', '0000'),
  ('1000', '0001', '0001'): ('1000', '0001', '0001'),
  ('0100', '1000', '1000'): ('0000', '0000', '0000'),
  ('0100', '1000', '0100'): ('0000', '0000', '0000'),
  ('0100', '1000', '0010'): ('0000', '0000', '0000'),
  ('0100', '1000', '0001'): ('0100', '1000', '0001'),
  ('0100', '0100', '1000'): ('0000', '0000', '0000'),
  ('0100', '0100', '0100'): ('0000', '0000', '0000'),
  ('0100', '0100', '0010'): ('0000', '0000', '0000'),
  ('0100', '0100', '0001'): ('0100', '0100', '0001'),
  ('0100', '0010', '1000'): ('0100', '0010', '1000'),
  ('0100', '0010', '0100'): ('0000', '0000', '0000'),
  ('0100', '0010', '0010'): ('0000', '0000', '0000'),
  ('0100', '0010', '0001'): ('0000', '0000', '0000'),
  ('0100', '0001', '1000'): ('0100', '0001', '1000'),
  ('0100', '0001', '0100'): ('0100', '0001', '0100'),
  ('0100', '0001', '0010'): ('0100', '0001', '0010'),
  ('0100', '0001', '0001'): ('0100', '0001', '0001'),
  ('0010', '1000', '1000'): ('0000', '0000', '0000'),
  ('0010', '1000', '0100'): ('0000', '0000', '0000'),
  ('0010', '1000', '0010'): ('0000', '0000', '0000'),
  ('0010', '1000', '0001'): ('0010', '1000', '0001'),
  ('0010', '0100', '1000'): ('0000', '0000', '0000'),
  ('0010', '0100', '0100'): ('0010', '0100', '0100'),
  ('0010', '0100', '0010'): ('0000', '0000', '0000'),
  ('0010', '0100', '0001'): ('0000', '0000', '0000'),
  ('0010', '0010', '1000'): ('0000', '0000', '0000'),
  ('0010', '0010', '0100'): ('0000', '0000', '0000'),
  ('0010', '0010', '0010'): ('0010', '0010', '0010'),
  ('0010', '0010', '0001'): ('0000', '0000', '0000'),
  ('0010', '0001', '1000'): ('0010', '0001', '1000'),
  ('0010', '0001', '0100'): ('0000', '0000', '0000'),
  ('0010', '0001', '0010'): ('0000', '0000', '0000'),
  ('0010', '0001', '0001'): ('0010', '0001', '0001'),
  ('0001', '1000', '1000'): ('0001', '1000', '1000'),
  ('0001', '1000', '0100'): ('0001', '1000', '0100'),
  ('0001', '1000', '0010'): ('0000', '0000', '0000'),
  ('0001', '1000', '0001'): ('0001', '1000', '0001'),
  ('0001', '0100', '1000'): ('0001', '0100', '1000'),
  ('0001', '0100', '0100'): ('0001', '0100', '0100'),
  ('0001', '0100', '0010'): ('0001', '0100', '0010'),
  ('0001', '0100', '0001'): ('0001', '0100', '0001'),
  ('0001', '0010', '1000'): ('0000', '0000', '0000'),
  ('0001', '0010', '0100'): ('0001', '0010', '0100'),
  ('0001', '0010', '0010'): ('0000', '0000', '0000'),
  ('0001', '0010', '0001'): ('0001', '0010', '0001'),
  ('0001', '0001', '1000'): ('0001', '0001', '1000'),
  ('0001', '0001', '0100'): ('0001', '0001', '0100'),
  ('0001', '0001', '0010'): ('0001', '0001', '0010'),
  ('0001', '0001', '0001'): ('0001', '0001', '0001')
}

def edge_expansion(e):
  # Explode an edge into its constituent singleton edges.
  length = len(e)
  singleton_edges = []
  for i in range(len(e)):
    if e[i] == '1':
      edge = ('0' * i) + '1' + ('0' * (length - 1 - i))
      singleton_edges.append(edge)
  return singleton_edges

def triple_expansion(t):
  # Explode a triple into its constituent singleton triples.
  e0_exp = edge_expansion(t[0])
  e1_exp = edge_expansion(t[1])
  e2_exp = edge_expansion(t[2])

  return itertools.product(e0_exp, e1_exp, e2_exp)

# Return the incoming edge counts on each node in a triple. An edge set counts
# as an incoming edge iff every edge in the set is incident on the node. That is,
# if in every possible arrangement the node has an incoming edge.
def build_count_tuple(triple):
  if '0000' in triple:
    return None

  AB, AC, BC = triple

  A = [0, 0]
  if AB == '0100':
    A[0] = 1
  if AC == '0100':
    A[1] = 1
  A = tuple(A)

  B = [0, 0]
  if AB == '1000':
    B[0] = 1
  if BC == '0100':
    B[1] = 1
  B = tuple(B)

  C = [0, 0]
  if AC == '1000':
    C[0] = 1
  if BC == '1000':
    C[1] = 1
  C = tuple(C)

  return (A, B, C)


##############################
# Populate TRIPLE_REDUCTIONS #
##############################

ALL_EDGES = ['1000', '0100', '0010', '0001', '1100', '1010', '1001', '0110', '0101', '0011', '1110', '1101', '1011', '0111', '1111']
ALL_TRIPLES = itertools.product(ALL_EDGES, ALL_EDGES, ALL_EDGES)
TRIPLE_REDUCTIONS = {}

lookup = lambda t: SINGLETON_TRIPLE_REDUCTIONS[t]
for triple in ALL_TRIPLES:
  expansion = triple_expansion(triple)
  reductions = map(lookup, expansion)
  result = reduce(union, reductions)
  TRIPLE_REDUCTIONS[triple] = (result, build_count_tuple(result))


################
# Triple Stack #
################

def _naiveTripleOrderTest(triple):
  return triple[0] < triple[1] < triple[2]

class TripleStack:
  def __init__(self, orderTest=_naiveTripleOrderTest):
    self._stack = set()
    # orderTest takes a triple and returns true if the triple is in sorted order
    self._orderTest = orderTest

  def add(self, triple):
    assert self._orderTest(triple)
    self._stack.add(triple)

  def pop(self):
    return self._stack.pop()

  def empty(self):
    return not bool(len(self._stack))
