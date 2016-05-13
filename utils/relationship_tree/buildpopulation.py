import famtojson
import csvtojson
import json
from population import Population
from itertools import combinations
from collections import defaultdict


if __name__ == '__main__':
  import sys

  # Using the complete data set to build the relationship tree
  # Need to account for individuals who are not typed
  # UPDATED: To use CSV file with an added column re: is the individual in the filtered data set
  # csv_file = '/Users/bodhi/williams_lab/relationship_classification/safs_data/safs_description.csv'
  csv_file = sys.argv[1]

  family_info = csvtojson.csv_to_json(csv_file)

  pop = Population(family_info)

  big_families = []
  for fid in pop.persons:
    # Filter out families with only 1 member
    if len(pop.persons[fid].keys()) > 1:
      big_families.append(fid)

  rel_counts = defaultdict(lambda: 0)
  md_counts = defaultdict(lambda: 0)

  for fid in big_families:
    family = pop.persons[fid]
    pairs = combinations(family.keys(), 2)
    print 'Processing family %s' % fid
    for pair in pairs:
      p0, p1 = pair
      if family[p0].datapresent and family[p1].datapresent: # Only consider pairs where we have genetic data for both persons
        rel = family[p0].relationship_to(family[p1])
        md = family[p0].meiotic_distance(family[p1])
        rel_counts[rel] += 1
        md_counts[md] += 1
  print ''

  print 'Standard relationship quantities:'
  for rel in rel_counts:
    print '%s: %d' % (rel, rel_counts[rel])
  print ''

  print 'Meiotic distance quantities:'
  for md in md_counts:
    print '%s: %d' % (str(md), md_counts[md])
