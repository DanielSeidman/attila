from collections import defaultdict

##############
# Edge logic #
##############

# Take the intersection of two edge sets represented as strings.
def intersection(a, b):
  assert len(a) == len(b)

  result = ['0'] * len(a)
  for i in range(len(a)):
    if a[i] == '1' and b[i] == '1':
      result[i] = '1'

  return ''.join(result)

# Take the union of two edge sets represented as strings.
def union(a, b):
  assert len(a) == len(b)

  result = ['0'] * len(a)
  for i in range(len(a)):
    if a[i] == '1' or b[i] == '1':
      result[i] = '1'

  return ''.join(result)


#############
# EdgeTable #
#############

def _naivePairOrderTest(a, b):
  return a < b

# Track the edge sets
class EdgeTable:
  def __init__(self, startingValue, orderTest=_naivePairOrderTest):
    # startingValue gives the default value for every pair in the table
    self._table = defaultdict(lambda: startingValue)
    # orderTest takes a pair and returns true iff the pair is in sorted order
    self._orderTest = orderTest

  def __getitem__(self, pair):
    assert self._orderTest(*pair)
    return self._table[pair]

  def __setitem__(self, pair, value):
    assert self._orderTest(*pair)
    self._table[pair] = value
