from structures.edges import EdgeTable
from structures.edges import intersection
from structures.nodes import NodeTable
from structures.triples import build_generator
from structures.triples import decompose_triple
from structures.triples import TRIPLE_REDUCTIONS
from structures.triples import TripleStack

from collections import defaultdict

import copy
import sys

class GraphException(Exception):
  def __init__(self, message):
    self.message = message

class PedigreeGraph:
  def __init__(self, nodes=[], emptyEdge='0000', fullEdge='1111', nullEdge='0001', edgeLimit=2, keepHistory=True): # Defaults are set to the existing triple reductions
    # This implementation uses the default ordering functions
    self.initial_nodes = nodes
    self.emptyEdge = emptyEdge
    self.nullEdge = nullEdge
    self.edges = EdgeTable(fullEdge)
    self.nodes = NodeTable(edgeLimit)

    self.tripleGenerator = build_generator(nodes)

    # Preloading edges should be moved to the constructor so that
    # triple generators are build in a single step.
    self.useComponents = False
    self.componentMap = None
    self.tripleGenerators = None

    self.keepHistory = keepHistory
    self.history = []


  def get(self, pair):
    return self.edges[pair]


  def revert(self):
    # Step the graph history back one step.
    # Pass the appropriate structures to edges and nodes.

    # history looks like:
    # ( pair, (edges, nodes))
    # where edges looks like {'revert': {}, 'del' []}
    # All keys in del should be deleted
    # All pair values in revert should be set to these old values

    if self.history:
      lastPair, edges, nodes = self.history.pop()

      self.edges.revert(edges)
      self.nodes.revert(nodes)

      return lastPair


  def find_components(self):
    nodes = list(self.initial_nodes)
    component = 0
    components = defaultdict(lambda: [])
    componentMap = {}

    # Breadth first search to find connected components.
    while nodes:
      neighbors = set()
      neighbors.add(nodes.pop())

      while neighbors:
        n1 = neighbors.pop()
        components[component].append(n1)
        componentMap[n1] = component

        for n2 in list(nodes): # Cannot iterate over nodes and simultaneous modify it
          pair = (n1, n2) if n1 < n2 else (n2, n1)
          if self.edges[pair] != self.nullEdge:
            neighbors.add(n2)
            nodes.remove(n2)

      # By definition, every new node popped yields a new component
      component += 1

    return components, componentMap


  def use_components(self):
    print 'Detecting components.'
    components, componentMap = self.find_components()
    print 'Found %d components.' % len(components)

    # Set the map for looking up a node's component
    self.componentMap = componentMap

    print 'Building triple generators.'
    # Create a triple generator for each component
    tripleGenerators = {}
    for component in components:
      nodes = components[component]
      tripleGenerators[component] = build_generator(nodes)
    self.tripleGenerators = tripleGenerators
    print 'Triple generators:'
    print self.tripleGenerators
    self.useComponents = True


  def _update_and_reduce_graph(self, edges, keepHistory):
    # Takes in a list of (pair, edge) tuples.
    # Insert the given edges into the graph and then reduce the graph,
    # returning True if the resulting graph is consistent and returning False
    # if the resulting graph is inconsistent. If the graph is inconsistent, its
    # state is reverted to before the edges were added and False is returned.

    # Store the state of the graph.
    oldEdges = copy.deepcopy(self.edges)
    oldNodes = copy.deepcopy(self.nodes)

    # WARNING: This logic assumes that all inserted edges are in the same component.
    # If attempting to batch preload edges, so this before setting the graph to
    # use components.
    tripleGenerator = self.tripleGenerator
    if self.useComponents and edges:
      first_pair = edges[0][0]
      first_node = first_pair[0]

      component = self.componentMap[first_node]
      print 'Pair in component: %d' % component
      tripleGenerator = self.tripleGenerators[component]

    try:
      # Add edges to the graph and collect the affected pairs
      pairs = []
      for pair, edge in edges:
        self.edges[pair] = edge
        pairs.append(pair)

      # Create the stack of triples to reduce.
      stack = TripleStack()

      # Populate the stack with all triples affected by the updated pairs
      map( lambda pair: map( lambda t: stack.add(t), tripleGenerator(*pair) ), pairs )

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
            map(lambda t: stack.add(t), tripleGenerator(*pair, c=excludedNode))

      if keepHistory:
        self.history.append((pair, self.edges.diff(oldEdges), self.nodes.diff(oldNodes)))

      # (3) Once the stack is empty, return True.
      return True
    except GraphException as e:
      # The graph state is illegal, so reject the edge.

      # Restore previous graph state.
      self.edges = oldEdges
      self.nodes = oldNodes

      return False


  def preload_graph(self, edges):
    # Insert all of the given edges and reduce the graph.
    return self._update_and_reduce_graph(edges, False)


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

      if self.keepHistory:
        self.history.append((pair, None, None))

      return True
    elif result == self.emptyEdge:
      print 'The added edge introduced a contradiction.'
      return False
    else:
      # These copies are restored if a contradiction is found when processing
      # the added edge.
      return self._update_and_reduce_graph([(pair, edge)], self.keepHistory)
