class SearchException(Exception):
  def __init__(self, message):
    self.message = message

def backtrack_search(graph, edge, remaining):
  # edge: (pair, [assignments])
  # remaining: [(pair, [assignments])]
  pair, assignments = edge

  print 'Remaining: %d' % len(remaining)

  while assignments:
    result = graph.copy()
    assignment = assignments.pop(0)

    print 'Pair: %s, Assignment: %s' % (str(pair), str(assignment))

    if result.add(pair, assignment):
      try:
        if remaining:
          result = backtrack_search(result, remaining[0], remaining[1:])
        return result
      except SearchException as se:
        pass

  raise SearchException(str(pair))
