import gzip
from collections import defaultdict

def import_plink_ibd(plink_ibd_file, test_fids):
  plink_ibd = defaultdict(lambda: {})

  with gzip.open(plink_ibd_file, 'r') as ifile:
    ifile.readline() # header line
    for line in ifile:
      FID1, IID1, FID2, IID2, RT, EZ, Z0, Z1, Z2, PI_HAT, PHE, DST, PPC, RATIO = line.strip().split()

      pair = (IID1, IID2) if (IID1 < IID2) else (IID2, IID1)
      ibd = [Z1, Z2]

      if FID1 == FID2:
        plink_ibd[FID1][pair] = ibd
      elif FID1 in test_fids and FID2 in test_fids: # Cross-pedigree edges for the test set
        plink_ibd['test'][pair] = ibd
      elif FID1 not in test_fids and FID2 not in test_fids: # Cross-pedigree edges for the training set
        # Note that external edges incident on the test set are dropped
        plink_ibd['train'][pair] = ibd

  return plink_ibd
