import sys

class SearchException(Exception):
  def __init__(self, message):
    self.message = message

def backtrack_search(graph, edge, remaining):
  # edge: (pair, [assignments])
  # remaining: [(pair, [assignments])]
  pair, assignments = edge
  # result = graph.copy()

  print 'Remaining: %d' % len(remaining)
  print 'Graph size: %d' % (sys.getsizeof(graph) + sys.getsizeof(graph.edges._table) + sys.getsizeof(graph.nodes._table) + sys.getsizeof(graph.history))

  while assignments:
    assignment = assignments.pop(0)

    print 'Pair: %s, Assignment: %s' % (str(pair), str(assignment))

    if graph.add(pair, assignment):
      try:
        if remaining:
          return backtrack_search(graph, remaining[0], remaining[1:])
        else:
          return graph
      except SearchException as se:
        # If we successfully added an edge but the deeper search failed,
        # then set the graph back to before we added that edge.
        # If result.add() is false, this does not need to be done as the
        # graph itself handles undoing the work of .add() when it fails.
        graph.revert()

  raise SearchException(str(pair))
