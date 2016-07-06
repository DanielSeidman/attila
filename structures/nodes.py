from collections import defaultdict
from edges import _naivePairOrderTest

#############
# NodeTable #
#############

# Track the number of incoming edges on each node in the graph.
class NodeTable:
  def __init__(self, limit, orderTest=_naivePairOrderTest):
    self._table = defaultdict(lambda: {})
    self._limit = limit
    # orderTest takes a pair and returns true iff the pair is in sorted order
    self._orderTest = orderTest

  def add(self, node, pair, count):
    assert self._orderTest(*pair)

    incoming_edges = self._table[node]
    incoming_edges[pair] = count

    if sum(incoming_edges.values()) > self._limit:
      return False

    self._table[node] = incoming_edges
    return True

  def diff(self, other):
    pairs = {}

    # Untouched keys, these are the keys with the starting value in et
    untouched = set(self._table.keys()).difference(set(other._table.keys()))
    pairs['del'] = untouched
    pairs['revert'] = {}

    for key in other._table.keys():
      if other._table[key] != self._table[key]:
        pairs['revert'][key] = other._table[key]

    if pairs['del'] or pairs['revert']:
      return pairs
    return None

  def revert(self, nodes):
    if nodes:
      for node in nodes['del']:
        del self._table[node]
      for node in nodes['revert']:
        self._table[pair] = nodes['revert'][pair]
