
from numba import cuda
import numpy as np
import time, sys
import operator
import argparse
import cudf

start_time= time.time()
parser = argparse.ArgumentParser(description='A Cuda Python based program to check if a list of input IPs is within a list of target networks \n python ips_in_sel_check.py -i input_ips.txt -t sel.txt')
parser.add_argument('-i', '--input', action='store', dest='input_file', help='Specify Input list file')
parser.add_argument('-t', '--target', action='store', dest='target_file', help='Specify Target list file')
parser.add_argument('-v', '--verbose', action='store_true', dest='verbosity', help='Verbose Output')
if len(sys.argv) < 2:
    parser.print_usage()
    sys.exit(1)
args = parser.parse_args()

vprint = print if args.verbosity else lambda *a, **k: None

def load_array_v6(filename):
  df= cudf.read_csv(filename,  header=None, encoding="utf-8-sig", dtype="str")

  for x in range(7):
   df.loc[((df["0"].str.contains("::") == True)  & (df["0"].str.count(':') < 8)), "0"] = df["0"].str.replace('::', ':0000::')
  df.loc[((df["0"].str.contains("::") == True)  & (df["0"].str.count(':') == 8)), "0"] = df["0"].str.replace('::', ':')

  original_frame = df["0"].to_pandas()

  gdf = cudf.DataFrame()
  new_cols = df["0"].str.split("/", n = 1, expand = True)
  df=new_cols[0].str.split(":", n = 8, expand = True)
  gdf[0]=new_cols[1].fillna(128)

  for x in range(8):
   df[x] = df[x].str.htoi()
  gdf_ips=df.astype('int').as_matrix()
  gdf_mask=gdf.astype('int').as_matrix()
  rows = gdf.shape[0]
  return original_frame, gdf_ips, gdf_mask, rows

@cuda.jit
def compare_net_to_net_v6(input_net_dec, input_mask, target_net_dec, target_mask, res_array):
  target_iterator, input_iterator = cuda.grid(2)
  if input_iterator < (input_net_dec.size/8) and target_iterator < (target_net_dec.size/8) :
    lower_cap = 0
    upper_cap = 0
    overlap_octet = 0
    for x in range(8):
      lower_cap =  operator.ge((target_net_dec[target_iterator][x] + target_mask[target_iterator][x]), input_net_dec[input_iterator][x])
      upper_cap = operator.ge((input_net_dec[input_iterator][x] + input_mask[input_iterator][x]), target_net_dec[target_iterator][x])
      if (lower_cap  and upper_cap) :
        overlap_octet += 1
      else :
        break
    if (overlap_octet == 8):
      res_array[input_iterator] = target_iterator + 1

@cuda.jit
def mask_split_v6(input_array, generic_mask_split):
  thread_pos = cuda.grid(1)
  prev = 0
  for x in range(8):
    i = 16*(x+1) - input_array[thread_pos][0]
    if operator.gt(i, 0):
      generic_mask_split[thread_pos][x] = 2**(i - prev)-1
      prev += (i - prev)

vprint("### Device in use : ", cuda.get_current_device().name.decode())


input_initial, input_ips, input_mask, input_size =  load_array_v6(args.input_file)
target_initial, target_ips, target_mask, target_size =  load_array_v6(args.target_file)


res_array = np.zeros(input_size, np.int64)
input_mask_split = np.zeros((input_size,8), np.int64)
target_mask_split = np.zeros((target_size,8), np.int64)


blockdim = 1024 
griddim = (input_size + (blockdim - 1)) // blockdim
vprint("### Number Input IPs : " , input_size, "; Target Size : " , target_size )
