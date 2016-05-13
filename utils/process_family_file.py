import sys

if __name__ == '__main__':
  family_file = sys.argv[1]

  # If 'yes', PO edges have an unknown direction
  muddle_directionality = (sys.argv[2] == 'y' or sys.argv[2] == 'yes')

  edges = {}

  with open(family_file, 'r') as ifile:
    for line in ifile:
      line = line.strip()

      if line == '':
        continue

      x, y, relationship = line.split()

      # Use string ordering
      if relationship == 'PO':
        if muddle_directionality:
          if x < y:
            edges[(x, y)] = '1100'
          else:
            edges[(y, x)] = '1100'
        else:
          if x < y:
            edges[(x, y)] = '1000' # low to high
          else:
            edges[(y, x)] = '0100' # high to low

      if relationship == 'FS':
        if x < y:
          edges[(x, y)] = '0010'
        else:
          edges[(y, x)] = '0010'

  print edges
