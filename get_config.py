#!/usr/bin/python

import sys
from config import *
from estimator import *
from cacti import *

print '\n#########################################################'
print '# UPDATING CONFIGURATION FILE PARAMETERS'
print '#########################################################\n'

config = Config()

# Check configuration file name
if len(sys.argv) != 2:
  print 'Configuration file name not provided...'
  print 'Usage: python create_config.py <config_name>'
else:
  config.set_name(sys.argv[1])
print 'Created configuration file:',config.get_name()+'.config\n'

# Helper function to calculate Number of Sets given cache size, block size, and associativity
def getCacheSets(size,block,assoc):
  return size / (block * assoc)

# Helper function to calculate Number of Tag Bits from a 42-bit address given number of sets and block size
def getTagBits(sets,block):
  return int(42 - math.log(sets,2) - math.log(block,2))

# Updated CPU Parameters
UNIFORM_WIDTH = 2
RUU_SIZE = 64
LSQ_SIZE = 32
B2LEV_HIST_SIZE = 10 
B2LEV_L2SIZE = 16384
RES_IALU = 1
RES_FPALU = 1
BTB_NSETS = 256
BTB_ASSOC = 8

# Updated DL1 Cache Parameters
DL1_SIZE = 262144
DL1_BSIZE = 32
DL1_ASSOC = 4
DL1_NSETS = getCacheSets(DL1_SIZE,DL1_BSIZE,DL1_ASSOC)
DL1_TAG_BITS = getTagBits(DL1_NSETS,DL1_BSIZE)

# Updated DL2 Cache Parameters
DL2_SIZE = 2097152
DL2_BSIZE = 64
DL2_ASSOC = 4
DL2_NSETS = getCacheSets(DL2_SIZE,DL2_BSIZE,DL2_ASSOC)
DL2_TAG_BITS = getTagBits(DL2_NSETS,DL2_BSIZE)

# Updated IL1 Cache Parameters
IL1_SIZE = 32768
IL1_BSIZE = 64
IL1_ASSOC = 4
IL1_NSETS = getCacheSets(IL1_SIZE,IL1_BSIZE,IL1_ASSOC)
IL1_TAG_BITS = getTagBits(IL1_NSETS,IL1_BSIZE)

# Update Config Parameters
config.set_param('fetch_ifqsize',UNIFORM_WIDTH)
config.set_param('decode_width',UNIFORM_WIDTH)
config.set_param('issue_width',UNIFORM_WIDTH)
config.set_param('commit_width',UNIFORM_WIDTH)
config.set_param('bpred_2lev_l2size',B2LEV_L2SIZE)
config.set_param('bpred_2lev_hist_size',B2LEV_HIST_SIZE)
config.set_param('bpred_btb_num_sets',BTB_NSETS)
config.set_param('bpred_btb_associativity',BTB_ASSOC)
config.set_param('ruu_size',RUU_SIZE)
config.set_param('lsq_size',LSQ_SIZE)
config.set_param('res_ialu',RES_IALU)
config.set_param('res_fpalu',RES_FPALU)
config.set_param('cache_dl1_nsets',DL1_NSETS)
config.set_param('cache_dl1_bsize',DL1_BSIZE)
config.set_param('cache_dl1_assoc',DL1_ASSOC)
config.set_param('cache_dl2_nsets',DL2_NSETS)
config.set_param('cache_dl2_bsize',DL2_BSIZE)
config.set_param('cache_dl2_assoc',DL2_ASSOC)
config.set_param('cache_il1_nsets',IL1_NSETS)
config.set_param('cache_il1_bsize',IL1_BSIZE)
config.set_param('cache_il1_assoc',IL1_ASSOC)

print '\n#########################################################'
print '# MODIFY EXCEL REAL ESTIMATOR TOOL AND READ RESULTS'
print '#########################################################\n'

estimator = Estimator()

# Configure required real estimator parameters
estimator.configure_estimator_params(config)

# Read real estimator outputs
RUU_RPORTS,RUU_WPORTS = estimator.get_ruu_port_params()
TOT_RUU_BITS,RUU_ENTRY_BITS,NUM_READOUT_BITS = estimator.get_ruu_bit_params()
DL1_RPORTS,DL1_WPORTS = estimator.get_dl1_port_params()
TOT_DL1_BITS = estimator.get_dl1_bit_params()
DL2_RPORTS,DL2_WPORTS = estimator.get_dl2_port_params()
TOT_DL2_BITS = estimator.get_dl2_bit_params()
IL1_RPORTS,IL1_WPORTS = estimator.get_il1_port_params()
TOT_IL1_BITS = estimator.get_il1_bit_params()
# IL2_RPORTS,IL2_WPORTS = estimator.get_il2_port_params()
# TOT_IL2_BITS = estimator.get_il2_bit_params()

# Check transistor count
TOT_TRANSISTOR_COUNT = estimator.get_transistor_count()
if not estimator.is_transistor_count_valid(TOT_TRANSISTOR_COUNT):
  print 'Configuration file not created due to errors...'
  sys.exit()

# Check area
TOT_AREA = estimator.get_area()
if not estimator.is_area_valid(TOT_AREA):
  print 'Configuration file not created due to errors...'
  sys.exit()

print '\n#########################################################'
print '# ACCESS ONLINE CACTI TOOL AND COMPUTE CACHE LATENCIES'
print '#########################################################\n'

cacti = Cacti()

# Access cacti tool and get ruu/cache access times
RUU_ACCESS_TIME = cacti.get_ruu_access_time([TOT_RUU_BITS,RUU_RPORTS,RUU_WPORTS,NUM_READOUT_BITS])
IL1_ACCESS_TIME = cacti.get_cache_access_time(['IL1',TOT_IL1_BITS,IL1_BSIZE,IL1_ASSOC,IL1_RPORTS,IL1_WPORTS,IL1_TAG_BITS])
DL1_ACCESS_TIME = cacti.get_cache_access_time(['DL1',TOT_DL1_BITS,DL1_BSIZE,DL1_ASSOC,DL1_RPORTS,DL1_WPORTS,DL1_TAG_BITS])
DL2_ACCESS_TIME = cacti.get_cache_access_time(['DL2',TOT_DL2_BITS,DL2_BSIZE,DL2_ASSOC,DL2_RPORTS,DL2_WPORTS,DL2_TAG_BITS])

# Compute cache latencies
IL1_LATENCY = cacti.cache_latency('IL1',IL1_ACCESS_TIME,RUU_ACCESS_TIME)
IL2_LATENCY = cacti.cache_latency('IL2',DL2_ACCESS_TIME,RUU_ACCESS_TIME)
DL1_LATENCY = cacti.cache_latency('DL1',DL1_ACCESS_TIME,RUU_ACCESS_TIME)
DL2_LATENCY = cacti.cache_latency('DL2',DL2_ACCESS_TIME,RUU_ACCESS_TIME)

# Update config parameters with new cache latencies
config.set_param('cache_il1lat',IL1_LATENCY)
config.set_param('cache_il2lat',IL2_LATENCY)
config.set_param('cache_dl1lat',DL1_LATENCY)
config.set_param('cache_dl2lat',DL2_LATENCY)

print '\n#########################################################'
print '# GENERATE SIMLESCALAR CONFIGURATION FILE'
print '#########################################################\n'

# Create configuration file
config.create_config_file()
