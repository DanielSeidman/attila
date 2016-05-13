from structures.edges import EdgeTable
from structures.edges import intersection
from structures.nodes import NodeTable
from structures.triples import build_generator
from structures.triples import decompose_triple
from structures.triples import TRIPLE_REDUCTIONS
from structures.triples import TripleStack
import copy

class GraphException(Exception):
  def __init__(self, message):
    self.message = message

class PedigreeGraph:
  def __init__(self, nodes=[], emptyEdge='0000', fullEdge='1111', edgeLimit=2): # Defaults are set to the existing triple reductions
    # This implementation uses the default ordering functions
    self.tripleGenerator = build_generator(nodes)
    self.emptyEdge = emptyEdge
    self.edges = EdgeTable(fullEdge)
    self.nodes = NodeTable(edgeLimit)

  def copy(self):
    new = PedigreeGraph()

    new.tripleGenerator = self.tripleGenerator
    new.emptyEdge = self.emptyEdge
    new.edges = copy.deepcopy(self.edges)
    new.nodes = copy.deepcopy(self.nodes)

    return new

  def get(self, pair):
    return self.edges[pair]

  def add(self, pair, edge):
    # (1) Take the intersection of the added edgeSet with the current edgeSet
    # match to this pair.
    # If the intersection is equal to the current edgeSet, then return True.
    # (The graph was not changed with the addition of this edge.)
    # If the intersection is equal to the empty set --> REJECT
    # Else update the edgeSet to be the submitted edge and continue.
    currentEdge = self.edges[pair]
    result = intersection(edge, currentEdge)

    if result == currentEdge:
      print 'The added edge changed nothing.'
      return True
    elif result == self.emptyEdge:
      print 'The added edge introduced a contradiction.'
      return False
    else:
      # These copies are restored if a contradiction is found when processing
      # the added edge.
      oldEdges = copy.deepcopy(self.edges)
      oldNodes = copy.deepcopy(self.nodes)

      try:
        # Introduce the candidate edge into the pedigree graph.
        self.edges[pair] = edge

        # (2) Generate all triples incident on the given edge and add these to the stack.
        stack = TripleStack()
        map(lambda t: stack.add(t), self.tripleGenerator(*pair))

        # (3) Recursively process modified triples until the stack is empty.
        while not stack.empty():
          # i. Pop a triple.
          triple = stack.pop()
          # Convert a triple into its edges
          tripleEdges = tuple(map(lambda t: self.edges[t[0]], decompose_triple(triple)))

          # ii. Reduce it.
          # If empty --> REJECT
          # Else continue.
          edges, counts = TRIPLE_REDUCTIONS[tripleEdges]

          if self.emptyEdge in edges: # Build this into TRIPLE_REDUCTIONS
            raise GraphException('Empty edge set.')

          # iii. Update/check the edge limit on all nodes.
          # If illegal --> REJECT
          # Else update the edges in the triple and add every edge modified by
          # the reduction to the stack.

          # NOTE: This is a temporary fix and will be changed to be
          # independent of the edge representations.
          # Edges go AB, AC, BC
          AB, AC, BC = (triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2])
          edgePairs = ( (AB, AC), (AB, BC), (AC, BC) )

          for node, pairs, counts in zip(triple, edgePairs, counts):
            pair1, pair2 = pairs
            count1, count2 = counts

            for pair, count in zip(pairs, counts):
              if count > 0:
                if not self.nodes.add(node, pair, count):
                  raise GraphException('Illegal edge count.')

          # Edges in order AB, AC, BC
          for pairWithExcluded, edge in zip(decompose_triple(triple), edges):
            pair, excludedNode = pairWithExcluded
            if self.edges[pair] != edge:
              # Update the edges data structure with the new edge
              self.edges[pair] = edge
              # Add all affected triples to the stack
              map(lambda t: stack.add(t), self.tripleGenerator(*pair, c=excludedNode))

        # (3) Once the stack is empty, return True.
        return True
      except GraphException as e:
        return False # The graph state is illegal, so reject the edge.
