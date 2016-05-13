from datetime import date

def parse_birthday(birthday):
  # 19580925
  if len(birthday) != 8:
    return None

  year = birthday[:4]
  month = birthday[4:6]
  day = birthday[6:]

  return date(int(year), int(month), int(day))


def csv_to_json(csv_file):
  individuals = {}

  with open(csv_file, 'r') as ifile:
    ifile.readline() # Skip header
    for line in ifile:
      fid, iid, father, mother, sex, MZTWIN,typed,batch,chip,gwas,WGS,birthday,datapresent = line.strip().split(',')
      if fid not in individuals:
        individuals[fid] = {}
      if iid not in individuals[fid]:
        individuals[fid][iid] = {'father_id': father,
                                 'mother_id': mother,
                                 'sex': sex,
                                 'datapresent': True if datapresent == 'y' else False,
                                 'birthday': parse_birthday(birthday)}

  return individuals


if __name__ == '__main__':
  import sys, json

  info = csv_to_json(sys.argv[1])
  # To do this properly, implement a conversion object in the style of the
  # json package
  for fid in info:
    for iid in info[fid]:
      info[fid][iid]['birthday'] = str(info[fid][iid]['birthday'])

  print json.dumps(info, sort_keys=True, indent=4)
