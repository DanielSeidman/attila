# Convert a .fam file into a JSON dump of individual information

def fam_to_json(fam_file):
  individuals = {}

  with open(fam_file, 'r') as ifile:
    for line in ifile:
      fid, iid, father, mother, sex, pheno = line.strip().split()
      if fid not in individuals:
        individuals[fid] = {}
      if iid not in individuals[fid]:
        individuals[fid][iid] = {'father_id': father,
                                 'mother_id': mother,
                                 'sex': sex}

  return individuals

if __name__ == '__main__':
  import sys, json

  print json.dumps(fam_to_json(sys.argv[1]), sort_keys=True, indent=4)
