from collections import defaultdict
from edges import _naivePairOrderTest

#############
# NodeTable #
#############

# Track the number of incoming edges on each node in the graph.
class NodeTable:
  def __init__(self, limit, orderTest=_naivePairOrderTest):
    self._nodes = defaultdict(lambda: {})
    self._limit = limit
    # orderTest takes a pair and returns true iff the pair is in sorted order
    self._orderTest = orderTest

  def add(self, node, pair, count):
    assert self._orderTest(*pair)

    incoming_edges = self._nodes[node]
    incoming_edges[pair] = count

    if sum(incoming_edges.values()) > self._limit:
      return False

    self._nodes[node] = incoming_edges
    return True
