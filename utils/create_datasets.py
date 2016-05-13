import sys

from plinkibdsupport import import_plink_ibd
from relationship_tree.population import Population
from relationship_tree.csvtojson import csv_to_json

if __name__ == '__main__':
  descriptive_csv_file = sys.argv[1]
  print 'Building population data structure.'
  pop = Population(csv_to_json(descriptive_csv_file))

  print 'Importing PLINK data.'
  plink_ibd_file = sys.argv[2]
  test_file = sys.argv[3]
  train_file = sys.argv[4]
  test_fids = sys.argv[5:]

  plink_ibd = import_plink_ibd(plink_ibd_file, test_fids)

  ###########################
  # Create the test dataset #
  ###########################
  test_data = []

  FIRST_DEGREE = ['sibling', 'parent', 'child']
  SECOND_DEGREE = ['niece/nephew', 'grandparent', 'aunt/uncle', 'half-sibling']

  print 'Populating test data.'
  for fid in test_fids: # Within-pedigree edges
    print 'FID: ' + fid
    family = pop.persons[fid]
    fid_ibd = plink_ibd[fid]
    for pair in fid_ibd:
      p0, p1 = pair
      if family[p0].datapresent and family[p1].datapresent:
        rel_type = family[p0].relationship_to(family[p1])

        if rel_type in SECOND_DEGREE:
          rel_type = 'second'
        elif rel_type not in FIRST_DEGREE and rel_type not in SECOND_DEGREE:
          rel_type = 'None'
        ibd1, ibd2 = fid_ibd[pair]
        test_data.append([p0, p1, rel_type, ibd1, ibd2])

  nonfamily_test_ibd = plink_ibd['test']
  for pair in nonfamily_test_ibd: # Cross-pedigree edges
    p0, p1 = pair
    ibd1, ibd2 = nonfamily_test_ibd[pair]
    test_data.append([p0, p1, 'None', ibd1, ibd2])

  with open(test_file, 'w') as ofile:
    test_data = map(lambda x: ','.join(x), test_data)
    ofile.write('\n'.join(test_data))

  ############################
  # Create the train dataset #
  ############################
  train_data = []

  print 'Populating test data.'
  for fid in filter(lambda f: f not in test_fids, pop.persons):
    print 'FID: ' + fid
    family = pop.persons[fid]
    fid_ibd = plink_ibd[fid]
    for pair in fid_ibd:
      p0, p1 = pair
      if family[p0].datapresent and family[p1].datapresent:
        rel_type = family[p0].relationship_to(family[p1])
        if rel_type in SECOND_DEGREE:
          rel_type = 'second'
        elif rel_type not in FIRST_DEGREE and rel_type not in SECOND_DEGREE:
          rel_type = 'None'
        ibd1, ibd2 = fid_ibd[pair]
        train_data.append([p0, p1, rel_type, ibd1, ibd2])

  # Note: this data will be all None edges and is likely not needed
  # nonfamily_train_ibd = plink_ibd['train']
  # for pair in nonfamily_train_ibd:
  #   p0, p1 = pair
  #   ibd1, ibd2 = nonfamily_train_ibd[pair]
  #   train_data.append([p0, p1, 'None', ibd1, ibd2])

  with open(train_file, 'w') as ofile:
    train_data = map(lambda x: ','.join(x), train_data)
    ofile.write('\n'.join(train_data))
