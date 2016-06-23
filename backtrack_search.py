class SearchException(Exception):
  def __init__(self, message):
    self.message = message

# Change assignments to candidates
def backtrack_search(graph, edge, remaining):
  # edge: (pair, [assignments])
  # remaining: [(pair, [assignments])]
  pair, assignments = edge
  result = graph.copy()

  print 'Remaining: %d' % len(remaining)

  while assignments:
    assignment = assignments.pop(0)

    print 'Pair: %s, Assignment: %s' % (str(pair), str(assignment))

    if result.add(pair, assignment):
      try:
        if remaining:
          result = backtrack_search(result, remaining[0], remaining[1:])
        return result
      except SearchException as se:
        # If we successfully added an edge but the deeper search failed,
        # then set the graph back to before we added that edge.
        # If result.add() is false, this does not need to be done as the
        # graph itself handles undoing the work of .add() when it fails.
        result = graph.copy()

  raise SearchException(str(pair))
