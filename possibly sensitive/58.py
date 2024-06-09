parser.add_argument('-v', '--verbose', action='store_true', dest='verbosity', help='Verbose Output')
if len(sys.argv) < 2:
    parser.print_usage()
    sys.exit(1)
args = parser.parse_args()

vprint = print if args.verbosity else lambda *a, **k: None

def load_array(filename):


  gdf = cudf.read_csv(filename, sep='.', decimal=",",  header=None, encoding="utf-8-sig")
  original_frame = gdf

  new_cols = gdf["3"].str.split("/", n = 1, expand = True)
  gdf.drop(columns =["3"], inplace = True)
  gdf[3]=new_cols[0]
  gdf[4]=new_cols[1].fillna(32)

  gdf2=gdf.astype('int').as_matrix()

  rows = gdf.shape[0]
  return gdf2 , rows

@cuda.jit
def IP_array_to_ints(ips, net_dec, mask):
  thread_pos = cuda.grid(1)
  net_dec[thread_pos] = (256**3)*ips[thread_pos][0]+(256**2)*ips[thread_pos][1]+(256)*ips[thread_pos][2]+ips[thread_pos][3]
  mask[thread_pos] = ips[thread_pos][4]


@cuda.jit
def compare_IP_to_IP(input_net_dec, input_mask, target_net_dec, target_mask, res_array):
  target_iterator, input_iterator = cuda.grid(2)
  if input_iterator < input_net_dec.size and target_iterator < target_net_dec.size :
    lower_cap = operator.ge((target_net_dec[target_iterator] + ((2**(32-target_mask[target_iterator]))-1)), input_net_dec[input_iterator])
    upper_cap = operator.ge((input_net_dec[input_iterator] + ((2**(32-input_mask[input_iterator]))-1)), target_net_dec[target_iterator])
 
    if ( lower_cap and upper_cap):
      res_array[input_iterator] =  target_iterator + 1

def reconstructed_ip(ip_array):
  return(str(ip_array[0]) + '.' + str(ip_array[1]) + '.' + str(ip_array[2]) + '.' + str(ip_array[3]) + '/' + str(ip_array[4]))

vprint("### Device in use : ", cuda.get_current_device().name.decode())


target_ips, target_size = load_array(args.target_file)

#
input_net_dec = np.zeros(input_size, np.int64)
target_net_dec = np.zeros(target_size, np.int64)
input_mask = np.zeros(input_size, np.int64)
target_mask = np.zeros(target_size, np.int64)
res_array = np.zeros(input_size, np.int64)


blockdim = 1024  
griddim = (input_size + (blockdim - 1)) // blockdim
vprint("### Input Size : " , input_size, "; Target Size : " , target_size )
vprint("### Grid Dimensions of input init : (" , griddim, ":" , blockdim, ")")

net_dec = input_net_dec
mask = input_mask
IP_array_to_ints[griddim,blockdim](input_ips, net_dec, mask)
input_net_dec = net_dec
input_mask = mask


blockdim = 1024
griddim = (target_size + (blockdim - 1)) // blockdim
net_dec = target_net_dec
mask = target_mask
vprint("### Grid Dimensions of target init : (" , griddim, ":" , blockdim, ")")
IP_array_to_ints[griddim,blockdim](target_ips, net_dec, mask)


blockdim = (31, 31)
griddim = ( (target_size + (blockdim[1] - 1)) // blockdim[1], (input_size + (blockdim[0] - 1)) // blockdim[0])
vprint("### Grid Dimensions of comparison : (" , griddim, ":" , blockdim, ")")
compare_IP_to_IP[griddim, blockdim](input_net_dec, input_mask, net_dec, mask, res_array)


for i in  range(res_array.size) :
  if (res_array[i] != 0) :
    print(reconstructed_ip(input_ips[i]), '##Found in ', reconstructed_ip(target_ips[res_array[i]-1]), sep = '')
  else :
    print(reconstructed_ip(input_ips[i]), '##Not_Found', sep = '')

vprint("###--- %s seconds ---" % (time.time() - start_time))
